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
})();
