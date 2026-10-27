// Requires Playwright and a Chromium installation. CHROMIUM_HELPER optionally points to a launch adapter.
const {chromium}=require('playwright'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
(async()=>{
const root=process.cwd(),voices=JSON.parse(fs.readFileSync('data/new-voices.json'));
const server=http.createServer((req,res)=>{let file=path.join(root,decodeURIComponent(new URL(req.url,'http://localhost').pathname));if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}try{if(fs.statSync(file).isDirectory())file=path.join(file,'index.html');res.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':file.endsWith('.css')?'text/css':file.endsWith('.html')?'text/html':file.endsWith('.webp')?'image/webp':file.endsWith('.mp3')?'audio/mpeg':'application/octet-stream');res.end(fs.readFileSync(file));}catch{res.writeHead(404).end();}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port;let browser;
try{
for(const width of [360,820,1440]){
 const options={headless:true};if(process.env.CHROMIUM_HELPER){const helper=require(process.env.CHROMIUM_HELPER).default;options.executablePath=await helper.executablePath();options.args=helper.args;}
 browser=await chromium.launch(options);const page=await browser.newPage({viewport:{width,height:1000}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'/vozes/');await page.locator('#alocucao-cookie-banner button').first().click({timeout:500}).catch(()=>{});
 // Rejection of optional cookies does not affect the catalog.
 const cookie=page.getByRole('button',{name:'Recusar opcionais'});if(await cookie.count())await cookie.click();
 assert.equal(await page.locator('.voice-card').count(),27);assert.equal(await page.locator('.voice-card .recent-work-link').count(),27);assert.equal(await page.locator('.voice-card a.recent-work-link').count(),4);assert.equal(await page.locator('.voice-card .review-count').evaluateAll(nodes=>nodes.every(n=>n.textContent==='0 avaliações')),true);assert.equal(await page.locator('.delivered-orders').count(),0);
 assert.equal(await page.locator('.voice-grid').evaluate(n=>getComputedStyle(n).gridTemplateColumns.split(' ').length),width===360?1:width===820?2:3);
 for(const [rank,slug] of [[1,'aida'],[2,'aline-mota'],[3,'fernanda']]){const badge=page.locator('.top-rank-'+rank);assert.equal(await badge.count(),1);assert.ok((await badge.locator('..').innerHTML()).includes('/locutores/'+slug+'/'));assert.ok(await badge.evaluate(n=>n.getBoundingClientRect().width<n.parentElement.getBoundingClientRect().width));}
 assert.equal(new Set(await page.locator('.top-voice-badge').evaluateAll(nodes=>nodes.map(n=>getComputedStyle(n).backgroundColor))).size,3);
 const empty=page.locator('[data-work-empty]').first(),voice=await empty.getAttribute('data-work-empty');await empty.click();await page.locator('dialog[open]').waitFor();await page.keyboard.press('Escape');assert.equal(await empty.evaluate(n=>document.activeElement===n),true);
 await empty.click();await page.getByRole('button',{name:'Ouvir demonstrações',exact:true}).click();assert.equal(await page.locator('dialog[open]').count(),0);await page.waitForFunction(voice=>document.activeElement.id.includes(voice),voice);
 assert.equal(await page.locator('body').evaluate(n=>n.scrollWidth<=innerWidth),true);
 await page.goto(base+'/locutores/aline-mota/#avalie');await page.waitForFunction(()=>{const y=document.querySelector('#avalie').getBoundingClientRect().top;return y>=0&&y<250;});
 const form=page.locator('.review-form');assert.equal(await form.count(),1);assert.equal(await form.locator('input[type=radio]').count(),5);assert.equal(await form.locator('button[type=submit]').isDisabled(),true);await form.locator('.review-choice label').nth(3).click();assert.equal(await form.locator('.selected').count(),4);await form.locator('input[name=name]').fill('Cliente de teste');await form.locator('textarea').fill('Avaliação visual de teste sem envio ou armazenamento.');
 assert.ok(await page.locator('[data-review-notice]').isVisible());assert.equal(await page.locator('body').evaluate(n=>n.scrollWidth<=innerWidth),true);
 await page.screenshot({path:'/tmp/voice-form-'+width+'.png'});
 await page.goto(base+'/vozes/');await page.screenshot({path:'/tmp/voice-catalog-'+width+'.png',fullPage:false});
 if(width===1440){
 let sent=null;
 await page.route('**/assets/reviews-config.js*',route=>route.fulfill({contentType:'text/javascript',body:"window.ALOCUCAO_REVIEWS={enabled:true,url:'https://review-test.supabase.co',anonKey:'public-test-key',turnstileSiteKey:'test-key'};"}));
 await page.route('https://review-test.supabase.co/functions/v1/reviews',route=>{const d=route.request().postDataJSON();let body=d.action==='summary'?[{voice:'aline-mota',average:4.8,count:12}]:d.action==='list'?[]:d.action==='validate'?{valid:true}:{received:true};if(d.action==='submit')sent=d;return route.fulfill({contentType:'application/json',body:JSON.stringify(body)});});
 await page.route('https://challenges.cloudflare.com/turnstile/v0/api.js*',route=>route.fulfill({contentType:'text/javascript',body:"window.turnstile={render:(node,options)=>{setTimeout(()=>options.callback('captcha-test'),0);return 1},reset:()=>{}};"}));
 await page.goto(base+'/locutores/aline-mota/?convite='+'a'.repeat(64)+'#avalie');
 assert.equal(await page.locator('.review-form').count(),1);assert.equal(new URL(page.url()).search,'');
 await page.waitForFunction(()=>!document.querySelector('.review-form button[type=submit]').disabled);
 assert.ok((await page.locator('.reviews-section .review-count').textContent()).includes('4,8/5 · 12 avaliações'));
 await page.locator('.review-form .review-choice label').nth(4).click();await page.locator('.review-form input[name=name]').fill('Cliente de teste');await page.locator('.review-form textarea').fill('Teste local com servidor simulado, sem avaliação publicada.');await page.locator('.review-form input[name=consent]').check();await page.locator('.review-form button[type=submit]').click();await page.getByText('Obrigado por compartilhar sua experiência!',{exact:false}).waitFor();assert.equal(sent.voice,'aline-mota');assert.equal(sent.rating,5);assert.equal(sent.token,'a'.repeat(64));
 }
 assert.deepEqual(errors,[]);await browser.close();browser=null;
}
// Every generated profile contains a real form, correct work behavior, and both original demos.
for(const v of voices){const html=fs.readFileSync(`locutores/${v.slug}/index.html`,'utf8');assert.ok(html.includes('class="review-form"'));assert.ok(html.includes('id="avalie"'));assert.ok(html.includes('Ver últimos trabalhos'));for(const kind of ['off','producao'])if(v[kind])assert.ok(html.includes(v[kind]));}
console.log('PASS: 27 cards and forms, 4 real portfolio links, 23 empty-state controls, responsive 1/2/3 columns, three badge colors, keyboard modal/focus, correct demo targeting, visible disabled form and star selection, no JS errors or horizontal overflow.');
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
})().catch(e=>{console.error(e);process.exit(1)});
