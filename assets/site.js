(() => {
  const pageType = location.pathname === "/" ? "home" : location.pathname.replace(/^\/+|\/+$/g, "").replaceAll("/", "_") || "home";
  const menuButton = document.querySelector(".mobile-toggle");
  const menu = document.querySelector(".menu");
  if (menuButton && menu) {
    const setMenu = open => { menu.classList.toggle("open", open); menuButton.setAttribute("aria-expanded", String(open)); menuButton.setAttribute("aria-label", open ? "Fechar menu" : "Abrir menu"); };
    menuButton.addEventListener("click", () => setMenu(!menu.classList.contains("open")));
    menu.querySelectorAll("a").forEach(link => link.addEventListener("click", () => setMenu(false)));
  }
  const year = document.getElementById("year"); if (year) year.textContent = new Date().getFullYear();
  const params = new URLSearchParams(location.search); const tracking = {};
  ["utm_source","utm_medium","utm_campaign","utm_term","utm_content","gclid"].forEach(key => { const value=params.get(key); if(value){tracking[key]=value;sessionStorage.setItem("alocucao_"+key,value)}else{const saved=sessionStorage.getItem("alocucao_"+key);if(saved)tracking[key]=saved}});
  window.dataLayer=window.dataLayer||[]; window.dataLayer.push({event:"page_view_context",page_type:pageType,...tracking});
  document.addEventListener("click",event=>{const link=event.target.closest('a[href^="https://wa.me/"]');if(!link)return;const ctaLocation=link.dataset.cta||link.textContent.trim().toLowerCase().replace(/\s+/g,"_").slice(0,60);window.dataLayer.push({event:"whatsapp_click",page_type:pageType,cta_location:ctaLocation,cta_text:link.textContent.trim(),...tracking});window.dataLayer.push({event:"generate_lead",method:"whatsapp",page_type:pageType,cta_location:ctaLocation,...tracking});if(typeof window.gtag==="function")window.gtag("event","conversion",{send_to:"AW-18420702149/U2s-CMSAyOscEMW31s9E"})});
  document.querySelectorAll("audio").forEach(audio=>{const countedVoices=new Set();audio.addEventListener("play",()=>{const voiceName=audio.dataset.voice||audio.getAttribute("aria-label")||"unknown";if(countedVoices.has(voiceName))return;countedVoices.add(voiceName);window.dataLayer.push({event:"voice_sample_play",page_type:pageType,voice_name:voiceName,...tracking})})});
  document.querySelectorAll("[data-cta]:not([href^='https://wa.me/'])").forEach(link=>link.addEventListener("click",()=>window.dataLayer.push({event:"cta_click",page_type:pageType,cta_location:link.dataset.cta,...tracking})));
  const briefForm=document.getElementById("brief-form"); if(briefForm)briefForm.addEventListener("submit",event=>{event.preventDefault();const data=new FormData(briefForm);const message=["Olá! Vim pelo briefing inicial do site A Locução.","",`Serviço: ${data.get("service")}`,`Prazo: ${data.get("deadline")}`,`Texto: ${data.get("text_ready")}`,"","Pode confirmar o valor, a disponibilidade e me orientar sobre a voz?"].join("\n");window.dataLayer.push({event:"brief_completed",page_type:pageType,service:data.get("service"),deadline:data.get("deadline"),...tracking});window.open(`https://wa.me/5527996529832?text=${encodeURIComponent(message)}`,"_blank","noopener")});

  const path=location.pathname.replace(/\/+$/,"")||"/";
  const replaceText=(root,pairs)=>{const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);const nodes=[];while(walker.nextNode())nodes.push(walker.currentNode);nodes.forEach(node=>{let text=node.nodeValue;pairs.forEach(([from,to])=>text=text.split(from).join(to));node.nodeValue=text})};

  if(path==="/locucao-off"){
    document.title="Locução Off Profissional a partir de R$ 12 | A Locução";
    const desc=document.querySelector('meta[name="description"]');if(desc)desc.content="Locução off profissional com mais de 150 vozes humanas. A partir de R$ 12. Pacotes de 10, 25 e 50 offs. Pedidos por WhatsApp ou Área de Pedidos 24h.";
  }
  if(path==="/spot-comercial"){
    document.title="Produção de Spot Comercial a partir de R$ 25 | A Locução";
    const desc=document.querySelector('meta[name="description"]');if(desc)desc.content="Produção completa de spot comercial a partir de R$ 25. Pacotes de 5, 15 e 30 produções. Atendimento humano e pedidos online.";
  }

  // Faixa comercial global: reforça os principais diferenciais nas páginas que usam o JS comum do site.
  if(!document.querySelector('.al-global-sales') && !['/','/locucao-off','/spot-comercial'].includes(path)){
    const style=document.createElement('style');
    style.textContent='.al-global-sales{background:#0b1726;color:#fff;padding:16px 18px;font-family:Inter,system-ui,sans-serif}.al-global-sales .inner{max-width:1160px;margin:auto;display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap}.al-global-sales strong{font-size:1rem}.al-global-sales span{color:#d5e0ea;font-size:.88rem}.al-global-sales .links{display:flex;gap:9px;flex-wrap:wrap}.al-global-sales a{display:inline-flex;align-items:center;min-height:40px;padding:0 13px;border-radius:10px;text-decoration:none;font-weight:850}.al-global-sales .wa{background:#25d366;color:#052911}.al-global-sales .area{background:#fff;color:#0b1726}@media(max-width:650px){.al-global-sales .inner{display:grid}.al-global-sales .links a{flex:1;justify-content:center}}';
    document.head.appendChild(style);
    const bar=document.createElement('div');
    bar.className='al-global-sales';
    bar.innerHTML='<div class="inner"><div><strong>Mais de 150 vozes humanas • gravações até 23h</strong><br><span>Opções a partir de 10 e 30 min • finais de semana e feriados • pacotes em até 12x com juros</span></div><div class="links"><a class="wa" href="https://wa.me/5527996529832?text=Ol%C3%A1%21%20Quero%20fazer%20um%20pedido%20na%20A%20Locu%C3%A7%C3%A3o." target="_blank" rel="noopener">Pedir pelo WhatsApp</a><a class="area" href="https://painel.audio.net.br/cliente/alocucao" target="_blank" rel="noopener">Área de Pedidos 24h</a></div></div>';
    const header=document.querySelector('header');
    if(header) header.insertAdjacentElement('afterend',bar); else document.body.insertAdjacentElement('afterbegin',bar);
  }
})();
