(() => {
  'use strict';
  const cfg=window.ALOCUCAO_REVIEWS;
  const enabled=cfg?.enabled && /^https:\/\/[a-z0-9-]+\.supabase\.co$/.test(cfg.url) && cfg.anonKey && cfg.turnstileSiteKey;
  // Invitation URLs must never reach analytics, referrers or browser storage.
  const params=new URLSearchParams(location.search), token=window.__reviewInvite||params.get('convite');delete window.__reviewInvite;
  if(token){params.delete('convite');history.replaceState(null,'',location.pathname+(params.size?'?'+params:'')+location.hash);}
  const section=document.querySelector('[data-review-voice]');
  const admin=document.querySelector('[data-review-admin]');
  const el=(tag,text,cls)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;};
  const stars=(root,mean,count)=>{
    const label=count?`${Number(mean).toFixed(1).replace('.',',')}/5 · ${count} ${count===1?'avaliação':'avaliações'}`:'0 avaliações';
    root.querySelector('.review-count').textContent=label;
    root.querySelector('.review-stars-fill').style.width=`${count?Math.max(0,Math.min(100,mean*20)):0}%`;
    root.setAttribute('aria-label',count?label:'Ainda sem avaliações');
  };
  if(!enabled)return;
  const endpoint=cfg.url+'/functions/v1/reviews';
  async function api(action,body={},access=''){
    const response=await fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json','apikey':cfg.anonKey,...(access?{Authorization:'Bearer '+access}:{})},body:JSON.stringify({action,...body}),cache:'no-store',referrerPolicy:'no-referrer'});
    const result=await response.json();if(!response.ok)throw Error(result.error||'Serviço indisponível. Tente novamente.');return result;
  }
  async function summaries(){
    try{const rows=await api('summary');document.querySelectorAll('[data-rating-voice]').forEach(root=>{const row=rows.find(r=>r.voice===root.dataset.ratingVoice);stars(root,row?.average||0,row?.count||0);});}
    catch{document.querySelectorAll('[data-rating-voice]').forEach(root=>{root.querySelector('.review-count').textContent='Avaliações indisponíveis';root.setAttribute('aria-label','Avaliações temporariamente indisponíveis');});}
  }
  summaries();window.addEventListener('pageshow',event=>{if(event.persisted)summaries();});
  if(section){
    const voice=section.dataset.reviewVoice,notice=section.querySelector('[data-review-notice]'),list=section.querySelector('[data-review-list]'),more=section.querySelector('[data-review-more]');let offset=0;
    const card=row=>{const a=el('article',undefined,'review-card');
      if(row.has_image){const img=el('img');img.src=endpoint+'?image='+encodeURIComponent(row.id);img.alt='Imagem autorizada de '+row.name;img.loading='lazy';img.referrerPolicy='no-referrer';a.append(img);}
      a.append(el('strong',row.name),el('p',`${row.rating}/5 · Avaliação verificada`),el('blockquote',row.comment),el('small',new Date(row.published_at).toLocaleDateString('pt-BR')));list.append(a);
    };
    async function load(){try{const rows=await api('list',{voice,offset});rows.forEach(card);offset+=rows.length;more.hidden=rows.length<10;section.querySelector('[data-review-empty]').hidden=offset>0;}
      catch{section.querySelector('[data-review-empty]').textContent='As avaliações estão temporariamente indisponíveis. Tente novamente mais tarde.';}}
    more.addEventListener('click',()=>{more.disabled=true;load().finally(()=>more.disabled=false);});load();
    notice.textContent='Para enviar sua avaliação, utilize o convite individual recebido após a conclusão do trabalho.';
    // The simple anchor shows the form, but submitting requires a server-validated invitation.
    const form=el('form',undefined,'review-form');
    form.innerHTML='<fieldset class="review-choice"><legend>Sua avaliação (obrigatória)</legend>'+[1,2,3,4,5].map(n=>`<label><input type="radio" name="rating" value="${n}" required><span aria-hidden="true">★</span><span class="sr-only">${n} ${n===1?'estrela':'estrelas'}</span></label>`).join('')+'</fieldset><label>Nome do cliente ou empresa<input name="name" required minlength="2" maxlength="80" autocomplete="organization"></label><label>Comentário<textarea name="comment" required minlength="20" maxlength="2000" placeholder="Conte como foi a qualidade da locução, a interpretação, a entrega e sua experiência."></textarea></label><label>Fotografia ou logotipo (opcional)<input type="file" name="image" accept="image/jpeg,image/png,image/webp"><small>JPG, PNG ou WebP. Até 2 MB e 4000 × 4000 pixels.</small></label><label class="review-consent"><input type="checkbox" name="consent" required><span>Autorizo a publicação desta avaliação, do nome informado e da imagem, se enviada. Li a <a href="/politica-de-privacidade/#avaliacoes">Política de Privacidade</a>.</span></label><div data-captcha></div><button class="btn" type="submit" disabled>Enviar minha avaliação</button><p class="review-status" role="status" aria-live="polite"></p>';
    section.querySelector('[data-review-form-host]').append(form);
    form.addEventListener('change',()=>{const value=Number(new FormData(form).get('rating'));form.querySelectorAll('.review-choice label').forEach((label,i)=>label.classList.toggle('selected',i<value));});
    let widget, captcha='',valid=false;
    const status=form.querySelector('[role=status]'),button=form.querySelector('button');
    async function init(){
      if(!token)return;
      try{await api('validate',{voice,token});valid=true;notice.textContent='Convite confirmado. Sua avaliação será analisada antes da publicação.';
        const script=el('script');script.src='https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit';script.onload=()=>{widget=window.turnstile.render(form.querySelector('[data-captcha]'),{sitekey:cfg.turnstileSiteKey,action:'review',callback:value=>{captcha=value;button.disabled=false;},'expired-callback':()=>{captcha='';button.disabled=true;},'error-callback':()=>{status.textContent='Não foi possível verificar a proteção. Atualize a página.';}});};script.onerror=()=>{status.textContent='Proteção indisponível. Reabra seu convite mais tarde.';};document.head.append(script);
      }catch{notice.textContent='Este convite é inválido, expirou ou já foi utilizado. Solicite outro à equipe.';}}
    init();
    form.addEventListener('submit',async event=>{event.preventDefault();if(!valid||!captcha||!form.reportValidity())return;button.disabled=true;status.textContent='Enviando…';
      try{const data=new FormData(form),image=data.get('image');let imageData=null;
        if(image?.size){if(image.size>2*1024*1024||!['image/jpeg','image/png','image/webp'].includes(image.type))throw Error('Envie JPG, PNG ou WebP de até 2 MB.');
          imageData=await new Promise((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(reader.result.split(',')[1]);reader.onerror=reject;reader.readAsDataURL(image);});}
        await api('submit',{voice,token,rating:Number(data.get('rating')),name:data.get('name'),comment:data.get('comment'),consent:data.get('consent')==='on',captcha,image:imageData});
        valid=false;form.replaceChildren(el('p','Obrigado por compartilhar sua experiência! Sua avaliação foi recebida e será analisada antes da publicação.'));notice.textContent='Convite utilizado.';
      }catch(error){status.textContent=error.message;captcha='';window.turnstile?.reset(widget);}
    });
  }
  if(admin){
    admin.classList.add('review-admin');admin.replaceChildren();let session=null;
    const status=el('p','','review-status');status.setAttribute('role','status');
    const login=el('form');login.innerHTML='<label>E-mail administrativo<input type="email" name="email" autocomplete="username" required></label><label>Senha<input type="password" name="password" autocomplete="current-password" required></label><button class="btn">Entrar</button>';
    admin.append(login,status);
    login.addEventListener('submit',async e=>{e.preventDefault();const d=new FormData(login);try{const response=await fetch(cfg.url+'/auth/v1/token?grant_type=password',{method:'POST',headers:{apikey:cfg.anonKey,'Content-Type':'application/json'},body:JSON.stringify({email:d.get('email'),password:d.get('password')}),referrerPolicy:'no-referrer'});const result=await response.json();login.reset();if(!response.ok)throw Error('Não foi possível entrar. Confira os dados.');session=result.access_token;await api('admin_list',{offset:0},session);login.remove();dashboard();}catch(error){session=null;status.textContent=error.message;}});
    function dashboard(){
      status.textContent='';const box=el('div');admin.append(box);const cleanup=el('button','Executar retenção e excluir imagens pendentes','btn secondary');cleanup.onclick=async()=>{try{await api('cleanup',{},session);status.textContent='Retenção executada.';}catch(error){status.textContent=error.message;}};box.append(cleanup);const logout=el('button','Sair','btn secondary');box.append(logout);logout.onclick=()=>{session=null;location.reload();};
      const invite=el('form');invite.innerHTML='<h2>Gerar convite de avaliação</h2><label>Locutor<select name="voice" required></select></label><label>Identificador privado do pedido<input name="order" maxlength="100" required></label><label>Validade em dias<input name="days" type="number" min="1" max="90" value="30" required></label><button class="btn">Gerar convite</button>';
      const result=el('div');result.dataset.adminResult='';box.append(invite,result);
      fetch('/data/new-voices.json').then(r=>r.json()).then(voices=>voices.forEach(v=>{const option=el('option',v.name);option.value=v.slug;invite.elements.voice.append(option);})).catch(()=>status.textContent='Não foi possível carregar o catálogo.');
      invite.onsubmit=async e=>{e.preventDefault();try{const data=new FormData(invite),row=await api('invite',{voice:data.get('voice'),order:data.get('order'),days:Number(data.get('days'))},session);const message='Olá! Agradecemos por escolher a A Locução!\n\nSeu trabalho foi concluído e gostaríamos muito de conhecer sua experiência com nosso locutor.\n\nVocê pode avaliar o serviço com estrelas e deixar um comentário. É rápido e sua opinião é muito importante para nós!\n\nAvalie aqui: '+row.url+'\n\nMuito obrigado pela confiança!';
        result.replaceChildren(el('pre',message));const copy=el('button','Copiar mensagem','btn secondary');copy.type='button';copy.onclick=()=>navigator.clipboard.writeText(message).then(()=>status.textContent='Mensagem copiada.').catch(()=>status.textContent='Selecione e copie a mensagem acima.');result.append(copy);
      }catch(error){status.textContent=error.message;}};
      const filters=el('form');filters.innerHTML='<h2>Avaliações recebidas</h2><label>Status<select name="status"><option value="">Todos</option><option value="pending">Pendente</option><option value="approved">Aprovada</option><option value="rejected">Rejeitada</option><option value="hidden">Ocultada</option></select></label><label>Slug do locutor<input name="voice"></label><label>Nota<select name="rating"><option value="">Todas</option>'+[1,2,3,4,5].map(n=>`<option>${n}</option>`).join('')+'</select></label><label>Desde<input type="date" name="since"></label><button class="btn secondary">Filtrar</button>';
      const rows=el('div'),next=el('button','Ver mais avaliações','btn secondary');let offset=0;box.append(filters,rows,next);
      const refresh=async(reset=true)=>{try{if(reset){offset=0;rows.replaceChildren();}const d=new FormData(filters),items=await api('admin_list',{offset,status:d.get('status'),voice:d.get('voice'),rating:Number(d.get('rating'))||null,since:d.get('since')||null},session);offset+=items.length;next.hidden=items.length<20;
        for(const row of items){const card=el('article',undefined,'review-card');card.append(el('h3',row.name+' · '+row.voice),el('p',`${row.rating}/5 · ${row.status} · Pedido ${row.order_ref} · ${new Date(row.created_at).toLocaleString('pt-BR')}`),el('blockquote',row.comment));
          if(row.image_path){const imageButton=el('button','Ver imagem');imageButton.onclick=async()=>{try{const response=await fetch(endpoint+'?image='+row.id,{headers:{Authorization:'Bearer '+session},referrerPolicy:'no-referrer'});if(!response.ok)throw Error('Imagem indisponível');const url=URL.createObjectURL(await response.blob()),img=el('img');img.src=url;img.alt='Imagem enviada';img.onload=()=>URL.revokeObjectURL(url);card.append(img);}catch(error){status.textContent=error.message;}};card.append(imageButton);}
          const reason=el('input');reason.placeholder='Justificativa da decisão (obrigatória)';reason.maxLength=500;reason.setAttribute('aria-label','Justificativa para '+row.name);card.append(reason);
          for(const [value,label] of [['approved','Aprovar'],['rejected','Rejeitar'],['hidden','Ocultar']]){const button=el('button',label);button.type='button';button.onclick=async()=>{try{await api('moderate',{id:row.id,status:value,reason:reason.value},session);status.textContent='Decisão registrada.';refresh();summaries();}catch(error){status.textContent=error.message;}};card.append(button);}
          const erase=el('button','Excluir dados por solicitação');erase.onclick=async()=>{if(!confirm('Excluir definitivamente os dados públicos e o histórico desta avaliação?'))return;try{await api('erase',{id:row.id},session);await api('cleanup',{},session);refresh();summaries();}catch(error){status.textContent=error.message;}};card.append(erase);const historyButton=el('button','Histórico');historyButton.onclick=async()=>{try{const history=await api('history',{id:row.id},session);card.append(el('pre',history.map(h=>`${h.created_at} · ${h.status} · ${h.reason}`).join('\n')));}catch(error){status.textContent=error.message;}};card.append(historyButton);rows.append(card);}
      }catch(error){status.textContent=error.message;}};
      filters.onsubmit=e=>{e.preventDefault();refresh();};next.onclick=()=>refresh(false);refresh();
      const summary=el('pre');box.append(el('h2','Classificação por locutor'),summary);api('summary').then(data=>summary.textContent=data.map(r=>`${r.voice}: ${r.average.toFixed(1)}/5 · ${r.count} avaliações`).join('\n')||'Nenhuma avaliação aprovada.');
    }
  }
})();
