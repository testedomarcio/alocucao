(() => {
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
    }
  });

  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({event: "page_view_context", page_type: "home", ...tracking});

  document.querySelectorAll('a[href^="https://wa.me/"]').forEach(link => {
    link.addEventListener("click", () => {
      window.dataLayer.push({event: "whatsapp_click", page_type: "home", cta_text: link.textContent.trim(), ...tracking});
      if (typeof window.gtag === "function") {
        window.gtag("event", "conversion", {send_to: "AW-18420702149/U2s-CMSAyOscEMW31s9E"});
      }
    });
  });
})();

