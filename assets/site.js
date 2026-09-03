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
  const wa="https://wa.me/5527996529832?text=";
  const pkg=(qty,price,per,msg,best=false)=>`<article class="package${best?" best":""}"><div class="qty">${qty}</div><div class="price">${price}</div><div class="per">${per}</div><a class="btn btn-dark" href="${wa+encodeURIComponent(msg)}" target="_blank" rel="noopener">Quero este pacote</a></article>`;

  if(path==="/locucao-off"){
    document.title="Locução Off Profissional a partir de R$ 12 | A Locução";
    const desc=document.querySelector('meta[name="description"]');if(desc)desc.content="Locução off profissional com mais de 150 vozes humanas. A partir de R$ 12. Pacotes de 10, 25 e 50 offs. Pedidos por WhatsApp ou Área de Pedidos 24h.";
    replaceText(document.body,[["R$ 15,00","R$ 12,00"],["R$ 15","R$ 12"]]);
    const grid=document.querySelector(".package-grid");if(grid){grid.innerHTML=[pkg("01 Off","R$ 12,00","R$ 12,00 por off","Olá! Quero comprar 1 Off por R$ 12,00."),pkg("10 Offs","R$ 100,00","R$ 10,00 por off","Olá! Quero comprar o pacote de 10 Offs por R$ 100,00."),pkg("25 Offs","R$ 150,00","R$ 6,00 por off","Olá! Quero comprar o pacote de 25 Offs por R$ 150,00."),pkg("50 Offs","R$ 250,00","R$ 5,00 por off","Olá! Quero comprar o pacote de 50 Offs por R$ 250,00.",true)].join("");grid.style.gridTemplateColumns="repeat(4,1fr)"}
  }
  if(path==="/spot-comercial"){
    document.title="Produção de Spot Comercial a partir de R$ 25 | A Locução";
    const desc=document.querySelector('meta[name="description"]');if(desc)desc.content="Produção completa de spot comercial a partir de R$ 25. Pacotes de 5, 15 e 30 produções. Atendimento humano e pedidos online.";
    replaceText(document.body,[["R$ 40,00","R$ 25,00"],["R$ 40","R$ 25"]]);
    const grid=document.querySelector(".package-grid");if(grid){grid.innerHTML=[pkg("01 Produção","R$ 25,00","R$ 25,00 por produção","Olá! Quero comprar 1 Produção por R$ 25,00."),pkg("05 Produções","R$ 115,00","R$ 23,00 por produção","Olá! Quero comprar o pacote de 5 Produções por R$ 115,00."),pkg("15 Produções","R$ 225,00","R$ 15,00 por produção","Olá! Quero comprar o pacote de 15 Produções por R$ 225,00."),pkg("30 Produções","R$ 300,00","R$ 10,00 por produção","Olá! Quero comprar o pacote de 30 Produções por R$ 300,00.",true)].join("");grid.style.gridTemplateColumns="repeat(4,1fr)"}
  }
})();
