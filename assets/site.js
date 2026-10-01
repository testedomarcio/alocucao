(() => {
  const pageType = location.pathname === "/" ? "home" : location.pathname.replace(/^\/+|\/+$/g, "").replaceAll("/", "_") || "home";
  const menuButton = document.querySelector(".mobile-toggle");
  const menu = document.querySelector(".menu");
  if (menuButton && menu) {
    const setMenu = open => { menu.classList.toggle("open", open); menuButton.setAttribute("aria-expanded", String(open)); menuButton.setAttribute("aria-label", open ? "Fechar menu" : "Abrir menu"); };
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.addEventListener("click", () => setMenu(!menu.classList.contains("open")));
    menu.querySelectorAll("a").forEach(link => link.addEventListener("click", () => setMenu(false)));
  }
  const year = document.getElementById("year"); if (year) year.textContent = new Date().getFullYear();
  const params = new URLSearchParams(location.search); const tracking = {};
  ["utm_source","utm_medium","utm_campaign","utm_term","utm_content","gclid"].forEach(key => { const value=params.get(key); if(value){tracking[key]=value;sessionStorage.setItem("alocucao_"+key,value)}else{const saved=sessionStorage.getItem("alocucao_"+key);if(saved)tracking[key]=saved}});
  window.dataLayer=window.dataLayer||[]; window.dataLayer.push({event:"page_view_context",page_type:pageType,...tracking});

  // Global WhatsApp Floating Widget Component
  const setupWhatsAppFloat = () => {
    if (document.getElementById("whatsapp-float-widget")) return;

    if (!document.getElementById("wa-float-style")) {
      const style = document.createElement("style");
      style.id = "wa-float-style";
      style.textContent = `
        .wa-float-widget {
          position: fixed;
          right: 20px;
          bottom: 20px;
          z-index: 9999;
          display: flex;
          align-items: center;
          gap: 12px;
          pointer-events: none;
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        .wa-float-tooltip {
          position: relative;
          background: #ffffff;
          color: #0f172a;
          padding: 10px 16px;
          border-radius: 12px;
          font-size: 0.88rem;
          font-weight: 700;
          box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
          white-space: nowrap;
          display: flex;
          align-items: center;
          user-select: none;
          line-height: 1.2;
          pointer-events: none;
        }
        .wa-tooltip-arrow {
          position: absolute;
          right: -8px;
          top: 50%;
          transform: translateY(-50%);
          width: 0;
          height: 0;
          border-top: 7px solid transparent;
          border-bottom: 7px solid transparent;
          border-left: 8px solid #ffffff;
        }
        .wa-float-button {
          width: 60px;
          height: 60px;
          border-radius: 50%;
          background-color: #25D366;
          color: #ffffff;
          display: flex;
          align-items: center;
          justify-content: center;
          text-decoration: none;
          box-shadow: 0 8px 24px rgba(37, 211, 102, 0.4);
          transition: transform 0.2s ease, background-color 0.2s ease, box-shadow 0.2s ease;
          animation: wa-pulse 5s infinite ease-in-out;
          flex-shrink: 0;
          pointer-events: auto;
        }
        .wa-float-button:hover {
          background-color: #20ba5a;
          transform: scale(1.08);
          box-shadow: 0 10px 28px rgba(37, 211, 102, 0.5);
        }
        .wa-float-button svg {
          width: 32px;
          height: 32px;
          fill: currentColor;
        }
        @keyframes wa-pulse {
          0%, 100% { transform: scale(1); }
          10%, 20% { transform: scale(1.1); }
          15% { transform: scale(0.95); }
          25% { transform: scale(1.05); }
          30% { transform: scale(1); }
        }
        @media (max-width: 768px) {
          .wa-float-widget {
            right: 16px;
            bottom: 20px;
            gap: 8px;
          }
          .wa-float-tooltip {
            display: none;
          }
          .wa-float-button {
            width: 52px;
            height: 52px;
          }
          .wa-float-button svg {
            width: 28px;
            height: 28px;
          }
        }
        @media (max-width: 620px) {
          body:has(.mobile-conversion-bar, .mobile-bar) .wa-float-widget,
          body.has-mobile-bar .wa-float-widget {
            bottom: 75px;
          }
        }
      `;
      document.head.appendChild(style);
    }

    if (document.querySelector(".mobile-conversion-bar, .mobile-bar")) {
      document.body.classList.add("has-mobile-bar");
    }

    const widget = document.createElement("div");
    widget.id = "whatsapp-float-widget";
    widget.className = "wa-float-widget";
    widget.innerHTML = `
      <div class="wa-float-tooltip">
        <span>Faça seu orçamento agora! 🎙️</span>
        <span class="wa-tooltip-arrow"></span>
      </div>
      <a class="wa-float-button"
         href="https://api.whatsapp.com/send?phone=5527996529832&text=Ol%C3%A1!%20Estou%20no%20site%20e%20gostaria%20de%20falar%20com%20o%20atendimento."
         target="_blank"
         rel="noopener noreferrer"
         aria-label="Falar com o atendimento pelo WhatsApp"
         data-cta="whatsapp_flutuante">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path fill-rule="evenodd" clip-rule="evenodd" d="M18.403 5.592A9.002 9.002 0 003.111 16.29L1.87 20.83a.6.6 0 00.732.732l4.54-1.241A9.002 9.002 0 0018.403 5.592zM12.004 2.2a9.792 9.792 0 00-8.48 14.691l-1.3 4.757a1.2 1.2 0 001.465 1.465l4.757-1.3A9.794 9.794 0 1012.004 2.2zm4.846 12.191c-.225-.113-1.328-.655-1.534-.73-.205-.075-.355-.113-.505.113-.15.225-.58.73-.711.88-.131.15-.262.169-.487.056a6.126 6.126 0 01-1.802-1.112 6.757 6.757 0 01-1.248-1.554c-.131-.225-.014-.347.098-.459.1-.1.225-.262.338-.394.113-.131.15-.225.225-.375.075-.15.038-.281-.019-.394-.056-.113-.505-1.218-.692-1.668-.182-.438-.367-.378-.505-.386l-.43-.008a.83.83 0 00-.6.281c-.206.225-.787.769-.787 1.875 0 1.106.806 2.175.918 2.325.113.15 1.587 2.423 3.845 3.398.537.232.956.37 1.283.474.54.172 1.03.148 1.418.09.432-.065 1.328-.543 1.516-1.068.188-.525.188-.975.131-1.068-.056-.094-.206-.15-.431-.263z" fill="currentColor"/>
        </svg>
      </a>
    `;
    document.body.appendChild(widget);
  };

  const initGlobal = () => {
    setupWhatsAppFloat();
    setupAudioLazyLoading();
  };

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
        if (audio.id === "voice-player") return;
        observer.observe(audio);
        audio.addEventListener("play", () => initLazyAudio(audio), { once: true });
        audio.addEventListener("pointerdown", () => initLazyAudio(audio), { once: true });
      });
    } else {
      audios.forEach(audio => initLazyAudio(audio));
    }
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initGlobal);
  } else {
    initGlobal();
  }

  document.querySelectorAll("audio").forEach(audio=>{
    const countedVoices=new Set();
    audio.addEventListener("play",()=>{
      const voiceName=audio.dataset.voice||audio.getAttribute("aria-label")||"unknown";
      if(countedVoices.has(voiceName))return;
      countedVoices.add(voiceName);
      const payload={page_type:pageType,voice_name:voiceName,...tracking};
      window.dataLayer.push({event:"voice_sample_play",...payload});
      if(typeof window.gtag==="function"){
        window.gtag("event","voice_sample_play",payload);
      }
    });
  });
  document.querySelectorAll("[data-cta]:not([href^='https://wa.me/'])").forEach(link=>link.addEventListener("click",()=>window.dataLayer.push({event:"cta_click",page_type:pageType,cta_location:link.dataset.cta,...tracking})));
  const briefForm=document.getElementById("brief-form");
  if(briefForm)briefForm.addEventListener("submit",event=>{
    event.preventDefault();
    const data=new FormData(briefForm);
    const message=["Olá! Vim pelo briefing inicial do site A Locução.","",`Serviço: ${data.get("service")}`,`Prazo: ${data.get("deadline")}`,`Texto: ${data.get("text_ready")}`,"","Pode confirmar o valor, a disponibilidade e me orientar sobre a voz?"].join("\n");
    const payload={page_type:pageType,service:data.get("service"),deadline:data.get("deadline"),...tracking};
    window.dataLayer.push({event:"brief_completed",...payload});
    if(typeof window.gtag==="function"){
      window.gtag("event","brief_completed",payload);
    }
    window.open(`https://wa.me/5527996529832?text=${encodeURIComponent(message)}`,"_blank","noopener");
  });

})();
