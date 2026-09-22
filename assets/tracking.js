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

  function serviceFromPath(pathname) {
    const path = String(pathname || "").toLowerCase();
    if (path.includes("spot-para-carro-de-som")) return "spot_carro_de_som";
    if (path.includes("spot-comercial") || path.includes("quanto-custa-um-spot")) return "spot_comercial";
    if (path.includes("locucao-off") || path.includes("locucao_off")) return "locucao_off";
    if (path.includes("campanha-politica") || path.includes("campanha-eleitoral")) return "campanha_politica";
    if (path.includes("calculadora")) return "calculadora";
    if (path.includes("vozes")) return "banco_de_vozes";
    if (path === "/" || path === "") return "pagina_inicial";
    return "outro";
  }

  function firstTouch() {
    const params = new URLSearchParams(window.location.search);
    const referrerHost = (() => {
      try { return document.referrer ? new URL(document.referrer).hostname : ""; }
      catch (error) { return ""; }
    })();
    const current = {
      source: cleanLabel(params.get("utm_source") || referrerHost || "direct"),
      medium: cleanLabel(params.get("utm_medium") || (referrerHost ? "referral" : "none")),
      campaign: cleanLabel(params.get("utm_campaign") || "not_set")
    };

    try {
      const stored = sessionStorage.getItem("alocucao_first_touch");
      if (stored) return JSON.parse(stored);
      sessionStorage.setItem("alocucao_first_touch", JSON.stringify(current));
    } catch (error) {}
    return current;
  }

  const attribution = firstTouch();

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
      page_title: cleanLabel(document.title),
      service_name: serviceFromPath(window.location.pathname),
      cta_id: cleanLabel(link.dataset.cta || link.id || "whatsapp_link"),
      cta_label: cleanLabel(link.textContent || link.getAttribute("aria-label") || "WhatsApp"),
      traffic_source: attribution.source,
      traffic_medium: attribution.medium,
      campaign_name: attribution.campaign
    });
  });
})();
