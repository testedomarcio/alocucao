(() => {
  const ADS_ID = "AW-18420702149";
  const ANALYTICS_ID = "G-TBHF64CH1R";
  const UET_ID = "187279262";

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };

  let googleTagLoaded = false;
  let analyticsConsent = false;
  let uetLoaded = false;
  window.uetq = window.uetq || [];
  window.uetq.push("consent", "default", { ad_storage: "denied" });

  function loadUet() {
    if (uetLoaded) return;
    uetLoaded = true;
    const loader = document.createElement("script");
    loader.async = true;
    loader.src = "https://bat.bing.net/bat.js?ti=" + UET_ID;
    loader.onload = () => {
      if (typeof window.UET !== "function") return;
      window.uetq = new window.UET({ ti: UET_ID, q: window.uetq, enableAutoSpaTracking: true });
      if (analyticsConsent) window.uetq.push("pageLoad");
    };
    document.head.appendChild(loader);
  }


  // Custom interactions belong to GA4 and are sent only after analytics consent.
  window.alocucaoTrackEvent = (name, parameters = {}) => {
    if (!analyticsConsent) return false;
    window.gtag("event", name, { ...parameters, send_to: ANALYTICS_ID });
    if (name === "whatsapp_click") window.uetq.push("event", "whatsapp_click", {
      event_category: "contact",
      event_label: (parameters.page_path || "/") + " | " + (parameters.cta_id || parameters.service_name || "outro")
    });
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
    window.uetq.push("consent", "update", { ad_storage: analyticsConsent ? "granted" : "denied" });
    if (analyticsConsent) {
      loadGoogleTag();
      loadUet();
    }
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
    if (path.includes("narracao-para-videos")) return "narracao_videos";
    if (path.includes("narracao-de-audiobooks")) return "audiobooks";
    if (path.includes("narracoes")) return "narracao_longa";
    if (path.includes("tratamento-de-audio")) return "tratamento_audio";
    if (path.includes("dublagem-de-videos")) return "dublagem_videos";
    if (path.includes("producao-de-podcasts")) return "producao_podcasts";
    if (path.includes("locucao-ia")) return "locucao_ia";
    if (path.includes("off-comercial")) return "off_comercial";
    if (path.includes("gravacao-off-e-producao")) return "off_producao";
    if (path.includes("/locutores/") || path.includes("perfil-locutor-")) return "perfil_locutor";
    if (path.includes("produtora-de-audio-")) return "servico_regional";
    if (path.includes("producao-para-supermercados")) return "producao_supermercados";
    if (path.includes("producao-para-igrejas")) return "producao_igrejas";
    if (path.includes("black-friday")) return "spot_black_friday";
    if (path.includes("natal")) return "spot_natal";
    if (path.includes("vinheta") || path.includes("podcast")) return "vinhetas";
    if (path.includes("video-institucional")) return "video_institucional";
    if (path.includes("telefonica") || path.includes("ura")) return "ura_telefonica";
    if (path.includes("agencias-revenda")) return "agencias_produtoras";
    if (path.includes("voz-infantil")) return "voz_infantil";
    if (path.includes("spot-para-carro-de-som")) return "spot_carro_de_som";
    if (path.includes("spot_comercial") || path.includes("spotcomercial") || path.includes("spot-comercial") || path.includes("quanto-custa-um-spot")) return "spot_comercial";
    if (path.includes("locucao-off") || path.includes("locucao_off")) return "locucao_off";
    if (path.includes("campanha-politica") || path.includes("campanha-eleitoral")) return "campanha_politica";
    if (path.includes("calculadora")) return "calculadora";
    if (path.includes("locutores")) return "banco_de_vozes";
    if (path.includes("vozes-ia")) return "vozes_ia";
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

    if (!analyticsConsent) return;
    const intent = link.dataset.cta === "solicitar_amostra" ? "solicitar_amostra" :
      isWhatsApp && /contratar|pedir locução|pedir produção|quero uma locução|quero produção/i.test(link.textContent || "") ? "contratar_locucao" :
      url.origin === window.location.origin && !url.hash && (/^\/locutores\/[^/]+\/$/.test(url.pathname) || url.pathname === "/vozes/") ? "escolher_voz" : "contato";
    if (intent !== "contato") window.alocucaoTrackEvent(intent + "_click", {
      page_path: window.location.pathname,
      service_name: serviceFromPath(window.location.pathname),
      voice_name: cleanLabel(link.dataset.voiceName || (intent === "escolher_voz" ? url.pathname.split("/")[2] : "")),
      cta_id: cleanLabel(link.dataset.cta || intent),
      contact_method: isWhatsApp ? "whatsapp" : "site"
    });
    if (!isWhatsApp) return;
    const attribution = firstTouch();

    window.alocucaoTrackEvent("whatsapp_click", {
      event_category: "contact",
      cta_intent: intent,
      contact_method: "whatsapp",
      page_path: window.location.pathname,
      page_title: cleanLabel(document.title),
      service_name: serviceFromPath(window.location.pathname),
      cta_id: cleanLabel(link.dataset.cta || link.id || "whatsapp_link"),
      voice_kind: cleanLabel(link.dataset.voiceKind || "synthetic"),
      voice_name: cleanLabel(link.dataset.voiceName),
      service_selected: cleanLabel(link.dataset.service || "a_confirmar"),
      cta_label: cleanLabel(link.textContent || link.getAttribute("aria-label") || "WhatsApp"),
      traffic_source: attribution.source,
      traffic_medium: attribution.medium,
      campaign_name: attribution.campaign
    });
  });

})();
