(() => {
  const pageType = location.pathname === "/" ? "home" : location.pathname.replace(/^\/+|\/+$/g, "").replaceAll("/", "_") || "home";
  const menuButton = document.querySelector(".mobile-toggle");
  const menu = document.querySelector(".menu");

  if (menuButton && menu) {
    const setMenu = open => {
      menu.classList.toggle("open", open);
      menuButton.setAttribute("aria-expanded", String(open));
      menuButton.setAttribute("aria-label", open ? "Fechar menu" : "Abrir menu");
    };
    menuButton.addEventListener("click", () => setMenu(!menu.classList.contains("open")));
    menu.querySelectorAll("a").forEach(link => link.addEventListener("click", () => setMenu(false)));
  }

  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  const params = new URLSearchParams(location.search);
  const tracking = {};
  ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid"].forEach(key => {
    const value = params.get(key);
    if (value) {
      tracking[key] = value;
      sessionStorage.setItem("alocucao_" + key, value);
    } else {
      const saved = sessionStorage.getItem("alocucao_" + key);
      if (saved) tracking[key] = saved;
    }
  });

  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({event: "page_view_context", page_type: pageType, ...tracking});

  document.querySelectorAll('a[href^="https://wa.me/"]').forEach(link => {
    link.addEventListener("click", () => {
      const ctaLocation = link.dataset.cta || link.textContent.trim().toLowerCase().replace(/\s+/g, "_").slice(0, 60);
      window.dataLayer.push({event: "whatsapp_click", page_type: pageType, cta_location: ctaLocation, cta_text: link.textContent.trim(), ...tracking});
      window.dataLayer.push({event: "generate_lead", method: "whatsapp", page_type: pageType, cta_location: ctaLocation, ...tracking});
      if (typeof window.gtag === "function") {
        window.gtag("event", "conversion", {send_to: "AW-18420702149/U2s-CMSAyOscEMW31s9E"});
      }
    });
  });

  document.querySelectorAll("audio").forEach(audio => {
    let counted = false;
    audio.addEventListener("play", () => {
      if (counted) return;
      counted = true;
      window.dataLayer.push({event: "voice_sample_play", page_type: pageType, voice_name: audio.dataset.voice || audio.getAttribute("aria-label") || "unknown", ...tracking});
    });
  });

  document.querySelectorAll("[data-cta]:not([href^='https://wa.me/'])").forEach(link => {
    link.addEventListener("click", () => {
      window.dataLayer.push({event: "cta_click", page_type: pageType, cta_location: link.dataset.cta, ...tracking});
    });
  });

  const briefForm = document.getElementById("brief-form");
  if (briefForm) {
    briefForm.addEventListener("submit", event => {
      event.preventDefault();
      const data = new FormData(briefForm);
      const message = [
        "Olá! Vim pelo pedido rápido do site A Locução.",
        "",
        `Serviço: ${data.get("service")}`,
        `Prazo: ${data.get("deadline")}`,
        `Texto: ${data.get("text_ready")}`,
        "",
        "Pode confirmar o valor, a disponibilidade e me orientar sobre a voz?"
      ].join("\n");
      window.dataLayer.push({event: "brief_completed", page_type: pageType, service: data.get("service"), deadline: data.get("deadline"), ...tracking});
      window.dataLayer.push({event: "generate_lead", method: "whatsapp_brief", page_type: pageType, service: data.get("service"), ...tracking});
      if (typeof window.gtag === "function") {
        window.gtag("event", "conversion", {send_to: "AW-18420702149/U2s-CMSAyOscEMW31s9E"});
      }
      window.open(`https://wa.me/5527996529832?text=${encodeURIComponent(message)}`, "_blank", "noopener");
    });
  }
})();

