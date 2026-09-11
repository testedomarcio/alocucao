(() => {
  const ADS_ID = "AW-18420702149";
  const ANALYTICS_ID = "G-TBHF64CH1R";

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };

  window.gtag("consent", "default", {
    ad_storage: "denied",
    analytics_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
    wait_for_update: 500
  });

  try {
    if (localStorage.getItem("alocucao_consent") === "accepted") {
      window.gtag("consent", "update", {
        ad_storage: "granted",
        analytics_storage: "granted",
        ad_user_data: "granted",
        ad_personalization: "denied"
      });
    }
  } catch (error) {}

  const loader = document.createElement("script");
  loader.async = true;
  loader.src = `https://www.googletagmanager.com/gtag/js?id=${ADS_ID}`;
  document.head.appendChild(loader);

  window.gtag("js", new Date());
  window.gtag("config", ADS_ID);
  window.gtag("config", ANALYTICS_ID);

  function cleanLabel(value) {
    return String(value || "")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, 100);
  }

  document.addEventListener("click", (event) => {
    const link = event.target.closest("a[href]");
    if (!link) return;

    let url;
    try {
      url = new URL(link.href, window.location.href);
    } catch (error) {
      return;
    }

    const isWhatsApp =
      url.hostname === "wa.me" ||
      url.hostname === "api.whatsapp.com" ||
      url.hostname === "web.whatsapp.com";

    if (!isWhatsApp) return;

    window.gtag("event", "whatsapp_click", {
      event_category: "conversion",
      contact_method: "whatsapp",
      page_path: window.location.pathname,
      cta_id: cleanLabel(link.dataset.cta || link.id || "whatsapp_link"),
      cta_label: cleanLabel(link.textContent || link.getAttribute("aria-label") || "WhatsApp")
    });
  });
})();
