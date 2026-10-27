// Requires Playwright and a Chromium installation. CHROMIUM_HELPER optionally points to a launch adapter.
const {chromium}=require('playwright'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
(async()=>{
const root=process.cwd(),voices=JSON.parse(fs.readFileSync('data/new-voices.json'));const expectedRatings={diego:'5,0/5 · 1 avaliação',enzo:'5,0/5 · 1 avaliação',fernanda:'3,0/5 · 1 avaliação'};
const server=http.createServer((req,res)=>{let file=path.join(root,decodeURIComponent(new URL(req.url,'http://localhost').pathname));if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}try{if(fs.statSync(file).isDirectory())file=path.join(file,'index.html');res.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':file.endsWith('.css')?'text/css':file.endsWith('.html')?'text/html':file.endsWith('.webp')?'image/webp':file.endsWith('.mp3')?'audio/mpeg':'application/octet-stream');res.end(fs.readFileSync(file));}catch{res.writeHead(404).end();}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port;let browser;
try{
for(const width of [360,820,1440]){
 const options={headless:true};if(process.env.CHROMIUM_HELPER){const helper=require(process.env.CHROMIUM_HELPER).default;options.executablePath=await helper.executablePath();options.args=helper.args;}
 browser=await chromium.launch(options);const page=await browser.newPage({viewport:{width,height:1000}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'/vozes/');await page.locator('#alocucao-cookie-banner button').first().click({timeout:500}).catch(()=>{});
 // Rejection of optional cookies does not affect the catalog.
 const cookie=page.getByRole('button',{name:'Recusar opcionais'});if(await cookie.count())await cookie.click();
 assert.equal(await page.locator('.voice-card').count(),27);assert.equal(await page.locator('.voice-card .recent-work-link').count(),27);assert.equal(await page.locator('.voice-card a.recent-work-link').count(),5);for(const voice of voices){const rating=page.locator('.voice-card [data-rating-voice="'+voice.slug+'"]');assert.equal(await rating.locator('.review-count').textContent(),expectedRatings[voice.slug]||'0 avaliações');assert.equal(await rating.locator('.review-stars-fill').getAttribute('style'),'width:'+(expectedRatings[voice.slug]?(voice.slug==='fernanda'?60:100):0)+'%');}assert.equal(await page.locator('.delivered-orders').count(),0);
 assert.equal(await page.locator('.voice-grid').evaluate(n=>getComputedStyle(n).gridTemplateColumns.split(' ').length),width===360?1:width===820?2:3);
 for(const [rank,slug] of [[1,'aida'],[2,'aline-mota'],[3,'fernanda']]){const badge=page.locator('.top-rank-'+rank);assert.equal(await badge.count(),1);assert.ok((await badge.locator('..').innerHTML()).includes('/locutores/'+slug+'/'));assert.ok(await badge.evaluate(n=>n.getBoundingClientRect().width<n.parentElement.getBoundingClientRect().width));}
 assert.equal(new Set(await page.locator('.top-voice-badge').evaluateAll(nodes=>nodes.map(n=>getComputedStyle(n).backgroundColor))).size,3);
 const empty=page.locator('[data-work-empty]').first(),voice=await empty.getAttribute('data-work-empty');await empty.click();await page.locator('dialog[open]').waitFor();await page.keyboard.press('Escape');assert.equal(await empty.evaluate(n=>document.activeElement===n),true);
 await empty.click();await page.getByRole('button',{name:'Ouvir demonstrações',exact:true}).click();assert.equal(await page.locator('dialog[open]').count(),0);await page.waitForFunction(voice=>document.activeElement.id.includes(voice),voice);
 assert.equal(await page.locator('body').evaluate(n=>n.scrollWidth<=innerWidth),true);
 await page.goto(base+'/locutores/aline-mota/#avalie');await page.waitForFunction(()=>{const y=document.querySelector('#avalie').getBoundingClientRect().top;return y>=0&&y<250;});
 assert.equal(await page.locator('.review-form').count(),0);assert.equal(await page.getByRole('button',{name:'Enviar minha avaliação'}).count(),0);assert.equal(await page.locator('body').evaluate(n=>n.scrollWidth<=innerWidth),true);
 await page.screenshot({path:'/tmp/voice-form-'+width+'.png'});
 await page.goto(base+'/vozes/');await page.screenshot({path:'/tmp/voice-catalog-'+width+'.png',fullPage:false});
 for(const slug of ['diego','enzo','fernanda']){
 await page.goto(base+'/locutores/'+slug+'/#avaliacoes-clientes');await page.waitForFunction(()=>{const y=document.querySelector('#avaliacoes-clientes').getBoundingClientRect().top;return y>=0&&y<250;});
 assert.equal(await page.locator('.review-card').count(),1);assert.equal(await page.locator('.reviews-section .review-count').textContent(),expectedRatings[slug]);
 assert.equal(await page.locator('.review-card img').count(),slug==='fernanda'?0:1);
 if(slug!=='fernanda')await page.waitForFunction(()=>document.querySelector('.review-card img').naturalWidth>0);
 if(slug==='diego')assert.equal(await page.locator('#ultimos-trabalhos audio').count(),1);
 if(width===360||width===1440)await page.screenshot({path:'/tmp/manual-review-'+slug+'-'+width+'.png'});
 assert.equal(await page.locator('body').evaluate(n=>n.scrollWidth<=innerWidth),true);
 }
 assert.deepEqual(errors,[]);await browser.close();browser=null;
}
// Every generated profile contains a real form, correct work behavior, and both original demos.
for(const v of voices){const html=fs.readFileSync(`locutores/${v.slug}/index.html`,'utf8');assert.ok(!html.includes('class="review-form"'));assert.ok(html.includes('id="avalie"'));assert.ok(html.includes('Ver últimos trabalhos'));for(const kind of ['off','producao'])if(v[kind])assert.ok(html.includes(v[kind]));}
console.log('PASS: 27 cards without forms and 3 authentic manual ratings, 5 real portfolio links, 22 empty-state controls, responsive 1/2/3 columns, three badge colors, keyboard modal/focus, correct demo targeting, no submission controls or automatic review scripts, no JS errors or horizontal overflow.');
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
})().catch(e=>{console.error(e);process.exit(1)});
