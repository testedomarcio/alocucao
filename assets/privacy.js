(() => {
  const STORAGE_KEY = "alocucao_consent";
  const saved = localStorage.getItem(STORAGE_KEY);

  function updateConsent(value) {
    if (typeof window.gtag === "function") {
      window.gtag("consent", "update", {
        ad_storage: value === "accepted" ? "granted" : "denied",
        analytics_storage: value === "accepted" ? "granted" : "denied",
        ad_user_data: value === "accepted" ? "granted" : "denied",
        ad_personalization: "denied"
      });
    }
  }

  if (saved === "accepted" || saved === "rejected") {
    updateConsent(saved);
    return;
  }

  const style = document.createElement("style");
  style.textContent = [
    ".privacy-banner{position:fixed;z-index:999;left:16px;right:16px;bottom:16px;max-width:760px;margin:auto;background:#fff;color:#17202a;border:1px solid #dfe7ef;border-radius:16px;box-shadow:0 18px 55px rgba(13,27,42,.2);padding:18px;display:grid;grid-template-columns:1fr auto;gap:18px;align-items:center}",
    ".privacy-banner p{margin:0;font:500 .92rem/1.5 Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif;color:#475569}",
    ".privacy-banner a{color:#0b706c;font-weight:800}",
    ".privacy-actions{display:flex;gap:8px;flex-wrap:wrap}",
    ".privacy-actions button{border:1px solid #cbd5e1;border-radius:10px;padding:10px 13px;font:800 .88rem/1 Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif;cursor:pointer;background:#fff;color:#0d1b2a}",
    ".privacy-actions .accept{background:#0b706c;border-color:#0b706c;color:#fff}",
    ".privacy-actions button:focus-visible{outline:3px solid #f2b84b;outline-offset:2px}",
    "@media(max-width:680px){.privacy-banner{grid-template-columns:1fr;bottom:10px;left:10px;right:10px}.privacy-actions button{flex:1}}"
  ].join("");
  document.head.appendChild(style);

  const banner = document.createElement("aside");
  banner.className = "privacy-banner";
  banner.setAttribute("aria-label", "Preferências de privacidade");
  banner.innerHTML = '<p>Usamos cookies opcionais para medir o desempenho do site e dos anúncios. Você pode aceitar ou recusar. Veja a <a href="/politica-de-privacidade/">Política de Privacidade</a>.</p><div class="privacy-actions"><button type="button" data-consent="rejected">Recusar opcionais</button><button type="button" class="accept" data-consent="accepted">Aceitar</button></div>';
  document.body.appendChild(banner);

  banner.querySelectorAll("[data-consent]").forEach(button => {
    button.addEventListener("click", () => {
      const value = button.dataset.consent;
      localStorage.setItem(STORAGE_KEY, value);
      updateConsent(value);
      banner.remove();
    });
  });
})();

