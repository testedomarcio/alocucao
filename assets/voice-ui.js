(() => {
  'use strict';
  const buttons=document.querySelectorAll('[data-work-empty]');
  if(!buttons.length)return;
  const dialog=document.createElement('dialog');dialog.className='work-dialog';dialog.setAttribute('aria-labelledby','work-dialog-title');dialog.setAttribute('aria-describedby','work-dialog-description');
  dialog.innerHTML='<button type="button" class="work-dialog-close" aria-label="Fechar mensagem">×</button><svg viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 14v-3a8 8 0 0 1 16 0v3M4 13h3v8H4a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2Zm16 0h-3v8h3a2 2 0 0 0 2-2v-4a2 2 0 0 0-2-2Z"/></svg><h2 id="work-dialog-title">Novidades em breve!</h2><p id="work-dialog-description">Ops! Ainda não temos trabalhos recentes publicados deste locutor. Enquanto isso, você pode ouvir as demonstrações disponíveis.</p><button type="button" class="btn" data-work-listen>Ouvir demonstrações</button>';
  document.body.append(dialog);let opener=null,followPlayer=null;
  buttons.forEach(button=>button.addEventListener('click',()=>{opener=button;dialog.showModal();dialog.querySelector('.work-dialog-close').focus();}));
  dialog.querySelector('.work-dialog-close').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',event=>{if(event.target!==dialog)return;const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();});
  dialog.addEventListener('close',()=>{const player=followPlayer;followPlayer=null;if(player){player.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'center'});player.focus({preventScroll:true});}else opener?.focus();});
  dialog.querySelector('[data-work-listen]').addEventListener('click',()=>{
    const source=opener,card=source?.closest('.voice-card'),player=card?.querySelector('audio')||document.querySelector('.profile-copy audio');
    followPlayer=player;dialog.close();
  });
})();
