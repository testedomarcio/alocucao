// npm install --no-save @electric-sql/pglite@0.5.12, then node scripts/test-reviews-db.cjs
const {PGlite}=require(process.env.PGLITE_MODULE||'@electric-sql/pglite');
const fs=require('node:fs'),assert=require('node:assert/strict');
(async()=>{
const db=new PGlite();
await db.exec(`create role anon;create role authenticated;create role service_role bypassrls;create schema auth;create table auth.users(id uuid primary key);create schema storage;create table storage.buckets(id text primary key,name text,public boolean,file_size_limit bigint,allowed_mime_types text[]);`);
for(const file of ['supabase/migrations/202610270001_reviews.sql','supabase/migrations/202610270002_retention.sql','supabase/seed-review-voices.sql'])await db.exec(fs.readFileSync(file,'utf8'));
const actor='11111111-1111-4111-8111-111111111111';await db.exec(`insert into auth.users values('${actor}');insert into review_admins values('${actor}');`);
const call=async(sql,args=[])=>db.query(sql,args);
const invite=async(hash,order,voice='aline-mota')=>call('select review_invite($1,$2,$3,30)',[voice,order,hash]);
const submit=async(hash,voice='aline-mota',rating=5)=>call('select review_submit($1,$2,$3,$4::smallint,$5,$6)',[hash,voice,'Cliente real',rating,'Excelente interpretação e qualidade na entrega.',null]);
await invite('a','P-1');await assert.rejects(()=>submit('a','david'));await assert.rejects(()=>submit('missing'));await assert.rejects(()=>submit('a','aline-mota',6));
const rid=(await submit('a')).rows[0].review_submit;await assert.rejects(()=>submit('a'));await assert.rejects(()=>invite('b','P-1'));
assert.equal((await call('select * from review_summary()')).rows.length,0);
await assert.rejects(()=>call("select review_moderate($1,'approved','publicar',$2)",[rid,'22222222-2222-4222-8222-222222222222']));
await call("select review_moderate($1,'approved','Experiência verificada',$2)",[rid,actor]);
let sum=(await call('select * from review_summary()')).rows[0];assert.equal(Number(sum.average),5);assert.equal(Number(sum.count),1);
await invite('c','P-2');const rid2=(await submit('c','aline-mota',1)).rows[0].review_submit;
await call("select review_moderate($1,'rejected','Dados pessoais indevidos',$2)",[rid2,actor]);assert.equal(Number((await call('select * from review_summary()')).rows[0].count),1);
await call("select review_moderate($1,'approved','Dados revisados sem alteração da nota',$2)",[rid2,actor]);assert.equal(Number((await call('select * from review_summary()')).rows[0].average),3);
await call("select review_moderate($1,'hidden','Remoção solicitada pelo titular',$2)",[rid,actor]);assert.equal(Number((await call('select * from review_summary()')).rows[0].average),1);
assert.equal((await call('select * from review_decisions')).rows.length,4);
await invite('d','P-expired');await call("update review_invites set expires_at=now()-interval '1 second' where token_hash='d'");await assert.rejects(()=>submit('d'));
await invite('old','P-old');await invite('new','P-old');await assert.rejects(()=>submit('old'));await submit('new');
for(let i=0;i<3;i++)assert.equal((await call("select review_rate('limited',3) as allowed")).rows[0].allowed,true);assert.equal((await call("select review_rate('limited',3) as allowed")).rows[0].allowed,false);
for(const role of ['anon','authenticated']){
await db.exec('set role '+role);await assert.rejects(()=>call('select * from customer_reviews'));await assert.rejects(()=>call('select * from review_summary()'));await assert.rejects(()=>call("select review_invite('david','forged','forged',30)"));await assert.rejects(()=>call("update customer_reviews set rating=5"));await db.exec('reset role');}
await call('select review_erase($1,$2)',[rid2,actor]);assert.equal((await call('select * from review_summary()')).rows.length,0);
await call("update customer_reviews set created_at=now()-interval '91 days',image_path='delete.webp' where status='pending'");await call('select review_cleanup()');assert.equal((await call('select * from customer_reviews where status=\'pending\'')).rows.length,0);assert.equal((await call('select * from review_image_deletions')).rows[0].path,'delete.webp');
await db.close();console.log('PASS: PostgreSQL migrations, zero public grants, expiry, wrong voice, one submission/order, token replacement, moderation audit, real averages, hiding, erasure, retention, rate limits.');
})().catch(e=>{console.error(e);process.exit(1)});
