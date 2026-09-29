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
  const initLazyAudio = audio => {
    if (audio.dataset.lazyLoaded) return;
    audio.dataset.lazyLoaded = "true";
    const srcEl = audio.querySelector("source[data-src]");
    if (srcEl) {
      srcEl.src = srcEl.dataset.src;
      audio.load();
    }
  };

  const setupAudioLazyLoading = () => {
    const audios = document.querySelectorAll("audio");
    if (!audios.length) return;

    if ("IntersectionObserver" in window) {
      const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            initLazyAudio(entry.target);
            obs.unobserve(entry.target);
          }
        });
      }, { rootMargin: "200px 0px" });

      audios.forEach(audio => {
        if (audio.id === "voice-player") return; // Global dock player handled by UI
        observer.observe(audio);
        audio.addEventListener("play", () => initLazyAudio(audio), { once: true });
        audio.addEventListener("pointerdown", () => initLazyAudio(audio), { once: true });
      });
    } else {
      audios.forEach(audio => initLazyAudio(audio));
    }
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setupAudioLazyLoading);
  } else {
    setupAudioLazyLoading();
  }

  document.querySelectorAll("audio").forEach(audio=>{const countedVoices=new Set();audio.addEventListener("play",()=>{const voiceName=audio.dataset.voice||audio.getAttribute("aria-label")||"unknown";if(countedVoices.has(voiceName))return;countedVoices.add(voiceName);window.dataLayer.push({event:"voice_sample_play",page_type:pageType,voice_name:voiceName,...tracking})})});
  document.querySelectorAll("[data-cta]:not([href^='https://wa.me/'])").forEach(link=>link.addEventListener("click",()=>window.dataLayer.push({event:"cta_click",page_type:pageType,cta_location:link.dataset.cta,...tracking})));
  const briefForm=document.getElementById("brief-form"); if(briefForm)briefForm.addEventListener("submit",event=>{event.preventDefault();const data=new FormData(briefForm);const message=["Olá! Vim pelo briefing inicial do site A Locução.","",`Serviço: ${data.get("service")}`,`Prazo: ${data.get("deadline")}`,`Texto: ${data.get("text_ready")}`,"","Pode confirmar o valor, a disponibilidade e me orientar sobre a voz?"].join("\n");window.dataLayer.push({event:"brief_completed",page_type:pageType,service:data.get("service"),deadline:data.get("deadline"),...tracking});window.open(`https://wa.me/5527996529832?text=${encodeURIComponent(message)}`,"_blank","noopener")});

})();
