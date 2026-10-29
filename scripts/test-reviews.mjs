import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {review,imageInfo} from '../supabase/functions/reviews/validation.mjs';
const valid={voice:'aline-mota',token:'a'.repeat(64),rating:5,name:'Cliente',comment:'Excelente interpretação e entrega do áudio.',consent:true};
assert.equal(review(valid).rating,5);
for(const change of [{rating:0},{rating:6},{rating:1.2},{consent:false},{name:'x'},{comment:'curto'},{voice:'x&status=eq.approved'},{token:'x'}])assert.throws(()=>review({...valid,...change}));
assert.throws(()=>imageInfo(new TextEncoder().encode('<svg><script>alert(1)</script></svg>')));
const png=new Uint8Array(24);png.set([137,80,78,71,13,10,26,10]);const d=new DataView(png.buffer);d.setUint32(16,100);d.setUint32(20,100);assert.equal(imageInfo(png).format,'png');d.setUint32(16,100000);assert.throws(()=>imageInfo(png));
const voices=JSON.parse(fs.readFileSync('data/new-voices.json'));
for(const v of voices){const html=fs.readFileSync(`locutores/${v.slug}/index.html`,'utf8');assert.ok(html.includes('id="avalie"'));assert.ok(html.includes('id="avaliacoes-clientes"'));assert.ok(!html.includes('class="review-form"'));assert.ok(!html.includes('Enviar minha avaliação'));assert.ok(!html.includes('/assets/reviews.js'));assert.ok(!html.includes('/assets/reviews-config.js'));const expected={aida:'5,0/5 · 1 avaliação','aline-mota':'5,0/5 · 1 avaliação',diego:'5,0/5 · 1 avaliação',enzo:'5,0/5 · 1 avaliação',fernanda:'3,0/5 · 1 avaliação',david:'5,0/5 · 1 avaliação',christine:'5,0/5 · 1 avaliação'}[v.slug]||'0 avaliações';assert.ok(html.includes(expected),v.slug+' rating mismatch');assert.ok(!html.includes('AggregateRating'));}
const catalog=fs.readFileSync('vozes/index.html','utf8');assert.equal((catalog.match(/data-rating-voice=/g)||[]).length,voices.length);
const entries=JSON.parse(fs.readFileSync('data/customer-reviews.json'));assert.equal(entries.length,7);assert.equal(entries.find(r=>r.voice==='fernanda').rating,3);
const cfg=fs.readFileSync('assets/reviews-config.js','utf8');assert.ok(cfg.includes('enabled:false'));
let fetched=false;const location={pathname:'/locutores/aline-mota/',search:'?convite='+valid.token,hash:'#avalie'};const window={ALOCUCAO_REVIEWS:{enabled:false}};
vm.runInNewContext(fs.readFileSync('assets/reviews.js','utf8'),{window,location,history:{replaceState:(a,b,path)=>{assert.equal(path,'/locutores/aline-mota/#avalie');}},URLSearchParams,document:{querySelector:()=>null,querySelectorAll:()=>[]},fetch:()=>{fetched=true;}});assert.equal(fetched,false);
console.log('PASS: all voice templates, zero state, disabled network, token scrubbing, no public forms or automatic review integration, input validation for archived backend.');

for(const slug of ['aida','aline-mota','enzo']){const row=entries.find(r=>r.voice===slug);const html=fs.readFileSync(`locutores/${slug}/index.html`,'utf8');assert.equal(row.links.length,2);for(const link of row.links){assert.ok(html.includes(`href="${link.url}" target="_blank" rel="noopener noreferrer"`));assert.ok(html.includes(link.label));}}
