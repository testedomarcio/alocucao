(() => {
  document.querySelectorAll('[data-package]').forEach(link => {
    link.addEventListener('click', () => window.alocucaoTrackEvent?.('package_interest', {
      service_name: link.dataset.service,
      package_credits: Number(link.dataset.package),
      package_total: Number(link.dataset.total),
      page_path: location.pathname
    }));
  });
})();
