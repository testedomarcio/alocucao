-- Garbage collection queue survives failed Storage deletes. Run cleanup daily after activation.
create table public.review_image_deletions(path text primary key);
alter table public.review_image_deletions enable row level security;
revoke all on public.review_image_deletions from public,anon,authenticated;
grant all on public.review_image_deletions to service_role;
create function public.review_cleanup() returns void language plpgsql security invoker set search_path='' as $$
begin
 insert into public.review_image_deletions(path)
 select image_path from public.customer_reviews where image_path is not null and
 ((status<>'approved' and created_at<now()-interval '90 days') or created_at<now()-interval '24 months') on conflict do nothing;
 delete from public.customer_reviews where (status<>'approved' and created_at<now()-interval '90 days') or created_at<now()-interval '24 months';
 -- Preserve consumed invitations as private order receipts for the 24-month retention window.
 delete from public.review_invites where created_at<now()-interval '24 months' and not exists(select 1 from public.customer_reviews where invite_id=review_invites.id);
 delete from public.review_limits where expires_at<now();
end $$;
create function public.review_erase(p_id uuid,p_actor uuid) returns void language plpgsql security invoker set search_path='' as $$
begin
 if not exists(select 1 from public.review_admins where user_id=p_actor) then raise exception 'forbidden';end if;
 insert into public.review_image_deletions(path) select image_path from public.customer_reviews where id=p_id and image_path is not null on conflict do nothing;
 delete from public.customer_reviews where id=p_id;
end $$;
revoke all on function public.review_cleanup(),public.review_erase(uuid,uuid) from public,anon,authenticated;
grant execute on function public.review_cleanup(),public.review_erase(uuid,uuid) to service_role;
