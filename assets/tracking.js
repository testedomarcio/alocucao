(() => {
  const ADS_ID = "AW-18420702149";
  const ANALYTICS_ID = "G-TBHF64CH1R";

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };

  let googleTagLoaded = false;
  let analyticsConsent = false;

  // Custom interactions belong to GA4 and are sent only after analytics consent.
  window.alocucaoTrackEvent = (name, parameters = {}) => {
    if (!analyticsConsent) return false;
    window.gtag("event", name, { ...parameters, send_to: ANALYTICS_ID });
    return true;
  };

  function loadGoogleTag() {
    if (googleTagLoaded) return;
    googleTagLoaded = true;

    const loader = document.createElement("script");
    loader.async = true;
    loader.src = `https://www.googletagmanager.com/gtag/js?id=${ANALYTICS_ID}`;
    document.head.appendChild(loader);

    window.gtag("js", new Date());
    window.gtag("config", ADS_ID);
    window.gtag("config", ANALYTICS_ID);
  }

  window.gtag("consent", "default", {
    ad_storage: "denied",
    analytics_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
    wait_for_update: 500
  });

  function applyConsent(value) {
    analyticsConsent = value === "accepted";
    window.gtag("consent", "update", {
      ad_storage: analyticsConsent ? "granted" : "denied",
      analytics_storage: analyticsConsent ? "granted" : "denied",
      ad_user_data: analyticsConsent ? "granted" : "denied",
      ad_personalization: "denied"
    });
    if (analyticsConsent) loadGoogleTag();
  }

  window.addEventListener("alocucao:consent", (event) => applyConsent(event.detail?.value));
  let initialConsent = window.alocucaoConsent;
  try { initialConsent = initialConsent || localStorage.getItem("alocucao_consent"); } catch (error) {}
  if (initialConsent === "accepted" || initialConsent === "rejected") applyConsent(initialConsent);

  function cleanLabel(value) {
    return String(value || "")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, 100);
  }

  function serviceFromPath(pathname) {
    const path = String(pathname || "").toLowerCase();
    if (path.includes("perfil-locutor-")) return "perfil_locutor";
    if (path.includes("produtora-de-audio-")) return "servico_regional";
    if (path.includes("black-friday")) return "spot_black_friday";
    if (path.includes("natal")) return "spot_natal";
    if (path.includes("vinheta") || path.includes("podcast")) return "vinhetas";
    if (path.includes("video-institucional")) return "video_institucional";
    if (path.includes("telefonica") || path.includes("ura")) return "ura_telefonica";
    if (path.includes("agencias-revenda")) return "agencias_revenda";
    if (path.includes("voz-infantil")) return "voz_infantil";
    if (path.includes("spot-para-carro-de-som")) return "spot_carro_de_som";
    if (path.includes("spot-comercial") || path.includes("quanto-custa-um-spot")) return "spot_comercial";
    if (path.includes("locucao-off") || path.includes("locucao_off")) return "locucao_off";
    if (path.includes("campanha-politica") || path.includes("campanha-eleitoral")) return "campanha_politica";
    if (path.includes("calculadora")) return "calculadora";
    if (path.includes("vozes")) return "banco_de_vozes";
    if (path.includes("portfolio")) return "portfolio";
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


  document.addEventListener("click", (event) => {
    const link = event.target instanceof Element ? event.target.closest("a[href]") : null;
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

    const panelPath = url.pathname.replace(/\/+$/, "");
    const isPanel = (url.hostname === "vozlocutor.com.br" && /^\/painel\/alocucao(?:\/(?:entrar|cadastro))?$/.test(panelPath)) ||
      (url.origin === new URL(window.location.href).origin && ["/painel", "/cadastro"].includes(panelPath));
    if (isPanel && analyticsConsent) {
      const attribution = firstTouch();
      window.alocucaoTrackEvent("panel_click", {
        event_category: "navigation", panel_action: panelPath.endsWith("/cadastro") ? "register" : "login",
        page_path: window.location.pathname, service_name: serviceFromPath(window.location.pathname),
        cta_id: cleanLabel(link.dataset.cta || link.id || "panel_link"),
        traffic_source: attribution.source, traffic_medium: attribution.medium, campaign_name: attribution.campaign
      });
    }
    if (!isWhatsApp || !analyticsConsent) return;
    const attribution = firstTouch();

    window.alocucaoTrackEvent("whatsapp_click", {
      event_category: "contact",
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
