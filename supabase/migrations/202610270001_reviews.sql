-- No table or RPC below is accessible with a browser's anon/authenticated key.
create table public.review_admins (user_id uuid primary key references auth.users(id) on delete cascade);
create table public.review_voices (slug text primary key check(slug ~ '^[a-z0-9-]+$'));
create table public.review_invites (
 id uuid primary key default gen_random_uuid(), voice text not null references public.review_voices(slug),
 order_ref text not null check(length(order_ref) between 1 and 100), token_hash text unique not null,
 expires_at timestamptz not null, used_at timestamptz, created_at timestamptz not null default now(),
 unique(voice,order_ref)
);
create table public.customer_reviews (
 id uuid primary key default gen_random_uuid(), invite_id uuid unique not null references public.review_invites(id),
 voice text not null references public.review_voices(slug), name text not null check(length(name) between 2 and 80),
 rating smallint not null check(rating between 1 and 5), comment text not null check(length(comment) between 20 and 2000),
 image_path text unique, consent_at timestamptz not null default now(), consent_version text not null default '2026-10-27',
 status text not null default 'pending' check(status in ('pending','approved','rejected','hidden')),
 created_at timestamptz not null default now(), published_at timestamptz
);
create index reviews_public_order on public.customer_reviews(voice,published_at desc,id) where status='approved';
create table public.review_decisions (
 id bigint generated always as identity primary key, review_id uuid not null references public.customer_reviews(id) on delete cascade,
 actor uuid references auth.users(id) on delete set null, status text not null, reason text not null check(length(reason) between 3 and 500),
 created_at timestamptz not null default now()
);
create table public.review_limits (key text primary key, hits int not null, expires_at timestamptz not null);
-- RLS with zero policies denies all browser reads and writes. Edge uses service_role only.
alter table public.review_admins enable row level security;
alter table public.review_voices enable row level security;
alter table public.review_invites enable row level security;
alter table public.customer_reviews enable row level security;
alter table public.review_decisions enable row level security;
alter table public.review_limits enable row level security;
revoke all on public.review_admins,public.review_voices,public.review_invites,public.customer_reviews,public.review_decisions,public.review_limits from anon,authenticated;
grant all on public.review_admins,public.review_voices,public.review_invites,public.customer_reviews,public.review_decisions,public.review_limits to service_role;
grant usage,select on sequence public.review_decisions_id_seq to service_role;

create function public.review_rate(p_key text,p_max int) returns boolean language plpgsql security invoker set search_path='' as $$
declare n int;
begin
 insert into public.review_limits as l values(p_key,1,now()+interval '1 hour')
 on conflict(key) do update set hits=case when l.expires_at<now() then 1 else l.hits+1 end,
 expires_at=case when l.expires_at<now() then now()+interval '1 hour' else l.expires_at end returning hits into n;
 return n<=p_max;
end $$;

create function public.review_submit(p_hash text,p_voice text,p_name text,p_rating smallint,p_comment text,p_image text) returns uuid
language plpgsql security invoker set search_path='' as $$
declare invitation public.review_invites; rid uuid;
begin
 select * into invitation from public.review_invites where token_hash=p_hash and voice=p_voice for update;
 if invitation.id is null or invitation.used_at is not null or invitation.expires_at<=now() then raise exception 'invalid_invitation'; end if;
 insert into public.customer_reviews(invite_id,voice,name,rating,comment,image_path)
 values(invitation.id,p_voice,p_name,p_rating,p_comment,p_image) returning id into rid;
 update public.review_invites set used_at=now() where id=invitation.id;
 return rid;
end $$;

create function public.review_invite(p_voice text,p_order text,p_hash text,p_days int) returns void
language plpgsql security invoker set search_path='' as $$
begin
 if p_days<1 or p_days>90 then raise exception 'invalid_expiry';end if;
 insert into public.review_invites as i(voice,order_ref,token_hash,expires_at)
 values(p_voice,p_order,p_hash,now()+make_interval(days=>p_days))
 on conflict(voice,order_ref) do update set token_hash=excluded.token_hash,expires_at=excluded.expires_at
 where i.used_at is null;
 if not found then raise exception 'order_already_reviewed';end if;
end $$;

create function public.review_moderate(p_id uuid,p_status text,p_reason text,p_actor uuid) returns void
language plpgsql security invoker set search_path='' as $$
begin
 if not exists(select 1 from public.review_admins where user_id=p_actor) then raise exception 'forbidden';end if;
 if p_status not in ('approved','rejected','hidden') or length(trim(p_reason))<3 or length(p_reason)>500 then raise exception 'invalid_decision';end if;
 perform 1 from public.customer_reviews where id=p_id for update;
 if not found then raise exception 'not_found';end if;
 update public.customer_reviews set status=p_status,published_at=case when p_status='approved' then coalesce(published_at,now()) else null end where id=p_id;
 insert into public.review_decisions(review_id,actor,status,reason) values(p_id,p_actor,p_status,trim(p_reason));
end $$;

create function public.review_summary() returns table(voice text,average double precision,count bigint)
language sql stable security invoker set search_path='' as $$
 select voice,avg(rating)::double precision,count(*) from public.customer_reviews where status='approved' group by voice;
$$;

revoke all on function public.review_rate(text,int),public.review_submit(text,text,text,smallint,text,text),public.review_invite(text,text,text,int),public.review_moderate(uuid,text,text,uuid),public.review_summary() from public,anon,authenticated;
grant execute on function public.review_rate(text,int),public.review_submit(text,text,text,smallint,text,text),public.review_invite(text,text,text,int),public.review_moderate(uuid,text,text,uuid),public.review_summary() to service_role;
insert into storage.buckets(id,name,public,file_size_limit,allowed_mime_types)
values('review-images','review-images',false,2097152,array['image/webp']) on conflict(id) do nothing;
-- No storage policies: uploads and downloads only through the authorized Edge function.
