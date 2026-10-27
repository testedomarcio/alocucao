import {ImageMagick,initializeImageMagick,MagickFormat} from 'npm:@imagemagick/magick-wasm@0.0.30';
import {review,slug,token,text,imageInfo} from './validation.mjs';
const url=Deno.env.get('SUPABASE_URL')!, key=Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const origin=Deno.env.get('REVIEWS_ORIGIN')||'https://alocucao.com.br';
const turnstileSecret=Deno.env.get('TURNSTILE_SECRET_KEY');
const headers={'Access-Control-Allow-Origin':origin,'Access-Control-Allow-Headers':'authorization,apikey,content-type','Access-Control-Allow-Methods':'GET,POST,OPTIONS','Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer'};
let initialized:Promise<void>|undefined;
const hash=async(value:string)=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(value)))).map(v=>v.toString(16).padStart(2,'0')).join('');
async function db(path:string,options:RequestInit={}){
 const response=await fetch(url+'/rest/v1/'+path,{...options,headers:{apikey:key,Authorization:'Bearer '+key,'Content-Type':'application/json',...options.headers}});
 if(!response.ok)throw Error('Não foi possível concluir a operação. Verifique os dados ou solicite um novo convite.');
 return response.status===204?null:await response.json();
}
const rpc=(name:string,args={})=>db('rpc/'+name,{method:'POST',body:JSON.stringify(args)});
async function admin(request:Request){
 const bearer=request.headers.get('Authorization')||'';
 if(!bearer.startsWith('Bearer '))throw Error('Acesso restrito. Entre novamente.');
 const response=await fetch(url+'/auth/v1/user',{headers:{apikey:key,Authorization:bearer}});
 if(!response.ok)throw Error('Sessão expirada. Entre novamente.');const user=await response.json();
 if(!user.id||!(await db('review_admins?user_id=eq.'+encodeURIComponent(user.id)+'&select=user_id')).length)throw Error('Acesso não autorizado.');return user.id;
}
async function storage(path:string,options:RequestInit={}){return await fetch(url+'/storage/v1/object/review-images/'+path,{...options,headers:{apikey:key,Authorization:'Bearer '+key,...options.headers}});}
async function image(bytes:Uint8Array){
 imageInfo(bytes);
 initialized??=Deno.readFile(new URL('./magick.wasm',import.meta.url)).then(initializeImageMagick);await initialized;
 return ImageMagick.read(bytes,img=>{
  if(img.width>4000||img.height>4000||img.width*img.height>12000000)throw Error('Dimensões inválidas.');
  const scale=Math.min(1,512/Math.max(img.width,img.height));img.resize(Math.max(1,Math.round(img.width*scale)),Math.max(1,Math.round(img.height*scale)));img.strip();img.quality=82;
  return img.write(MagickFormat.WebP,data=>new Uint8Array(data));
 });
}
Deno.serve(async request=>{
 if(request.method==='OPTIONS')return new Response(null,{headers});
 const json=(data:unknown,status=200)=>Response.json(data,{status,headers});
 try{
  if(request.headers.get('Origin')&&request.headers.get('Origin')!==origin)return json({error:'Origem não autorizada.'},403);
  if(request.method==='GET'){
   const id=new URL(request.url).searchParams.get('image');if(!id||! /^[0-9a-f-]{36}$/.test(id))return json({error:'Imagem inválida.'},400);
   const rows=await db('customer_reviews?id=eq.'+id+'&select=status,image_path');const row=rows[0];
   if(!row?.image_path)return json({error:'Imagem não encontrada.'},404);
   if(row.status!=='approved')await admin(request);
   const response=await storage(row.image_path);if(!response.ok)return json({error:'Imagem indisponível.'},404);
   return new Response(response.body,{headers:{...headers,'Content-Type':'image/webp'}});
  }
  if(request.method!=='POST')return json({error:'Método não permitido.'},405);
  // Bound streamed body even when the client omits Content-Length.
  const reader=request.body?.getReader();if(!reader)throw Error('Pedido vazio.');let size=0;const chunks:Uint8Array[]=[];
  while(true){const {done,value}=await reader.read();if(done)break;size+=value.length;if(size>2900000){await reader.cancel();return json({error:'Arquivo muito grande.'},413);}chunks.push(value);}
  const bytes=new Uint8Array(size);let start=0;for(const chunk of chunks){bytes.set(chunk,start);start+=chunk.length;}
  const data=JSON.parse(new TextDecoder().decode(bytes)), action=data.action;
  if(action==='summary')return json(await rpc('review_summary'));
  if(action==='list'){
   const voice=slug(data.voice),offset=Math.max(0,Math.min(100000,Number(data.offset)||0));
   const rows=await db(`customer_reviews?voice=eq.${voice}&status=eq.approved&select=id,name,rating,comment,published_at,image_path&order=published_at.desc,id.desc&limit=10&offset=${Math.floor(offset)}`);
   return json(rows.map(({image_path,...r}:any)=>({...r,has_image:!!image_path})));
  }
  if(action==='validate'||action==='submit'){
   const voice=slug(data.voice),t=token(data.token),digest=await hash(t);
   if(!await rpc('review_rate',{p_key:digest,p_max:30}))return json({error:'Muitas tentativas. Tente mais tarde.'},429);
   const rows=await db(`review_invites?token_hash=eq.${digest}&voice=eq.${voice}&used_at=is.null&expires_at=gt.${encodeURIComponent(new Date().toISOString())}&select=id`);
   if(!rows.length)return json({error:'Convite inválido, expirado ou utilizado.'},400);
   if(action==='validate')return json({valid:true});
   const v=review(data);if(!turnstileSecret)throw Error('Recebimento temporariamente indisponível.');
   const captchaResponse=await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify',{method:'POST',body:new URLSearchParams({secret:turnstileSecret,response:text(data.captcha,1,2048)})});const captcha=await captchaResponse.json();
   if(!captcha.success||captcha.hostname!==new URL(origin).hostname||captcha.action!=='review')throw Error('Proteção não validada. Tente novamente.');
   let path:string|null=null;
   try{
    if(data.image){if(typeof data.image!=='string'||data.image.length>2796204||! /^[A-Za-z0-9+/]*={0,2}$/.test(data.image))throw Error('Imagem inválida.');
     const raw=Uint8Array.from(atob(data.image),c=>c.charCodeAt(0)),optimized=await image(raw);path=crypto.randomUUID()+'.webp';
     const uploaded=await storage(path,{method:'POST',headers:{'Content-Type':'image/webp','x-upsert':'false'},body:optimized});if(!uploaded.ok)throw Error('Não foi possível armazenar a imagem.');}
    await rpc('review_submit',{p_hash:digest,p_voice:v.voice,p_name:v.name,p_rating:v.rating,p_comment:v.comment,p_image:path});
   }catch(error){
    // A network failure can occur after PostgreSQL committed. Never delete a referenced image.
    if(path){try{const linked=await db('customer_reviews?image_path=eq.'+path+'&select=id');if(!linked.length)await storage(path,{method:'DELETE'});}catch{/* Keep private object for operator reconciliation if the DB is unavailable. */}}throw error;}
   return json({received:true});
  }
  const actor=await admin(request);
  if(!await rpc('review_rate',{p_key:'admin:'+actor,p_max:500}))return json({error:'Limite de operações atingido.'},429);
  if(action==='cleanup'){
   await rpc('review_cleanup');
   const paths=await db('review_image_deletions?select=path&limit=100');
   for(const row of paths){const result=await storage(row.path,{method:'DELETE'});if(result.ok||result.status===404)await db('review_image_deletions?path=eq.'+encodeURIComponent(row.path),{method:'DELETE'});}
   return json({processed:paths.length});
  }
  if(action==='invite'){
   const voice=slug(data.voice),order=text(data.order,1,100),days=Number(data.days);if(!Number.isInteger(days)||days<1||days>90)throw Error('Validade deve ser entre 1 e 90 dias.');
   const t=Array.from(crypto.getRandomValues(new Uint8Array(32))).map(n=>n.toString(16).padStart(2,'0')).join('');
   await rpc('review_invite',{p_voice:voice,p_order:order,p_hash:await hash(t),p_days:days});return json({url:`${origin}/locutores/${voice}/?convite=${t}#avalie`});
  }
  if(action==='admin_list'){
   let query='customer_reviews?select=*,review_invites(order_ref)&order=created_at.desc,id.desc&limit=20&offset='+Math.floor(Math.max(0,Number(data.offset)||0));
   if(data.voice)query+='&voice=eq.'+slug(data.voice);
   if(data.status){if(!['pending','approved','rejected','hidden'].includes(data.status))throw Error('Status inválido.');query+='&status=eq.'+data.status;}
   if(data.rating){if(!Number.isInteger(data.rating)||data.rating<1||data.rating>5)throw Error('Nota inválida.');query+='&rating=eq.'+data.rating;}
   if(data.since){if(! /^\d{4}-\d{2}-\d{2}$/.test(data.since))throw Error('Data inválida.');query+='&created_at=gte.'+data.since;}
   const rows=await db(query);return json(rows.map(({review_invites,...row}:any)=>({...row,order_ref:review_invites.order_ref})));
  }
  if(! /^[0-9a-f-]{36}$/.test(data.id))throw Error('Avaliação inválida.');
  if(action==='erase'){await rpc('review_erase',{p_id:data.id,p_actor:actor});return json({erased:true});}
  if(action==='moderate'){await rpc('review_moderate',{p_id:data.id,p_status:data.status,p_reason:text(data.reason,3,500),p_actor:actor});return json({saved:true});}
  if(action==='history')return json(await db('review_decisions?review_id=eq.'+data.id+'&select=created_at,status,reason&order=created_at.desc'));
  return json({error:'Operação inválida.'},400);
 }catch(error){return json({error:error instanceof Error?error.message:'Serviço indisponível.'},400);}
});
