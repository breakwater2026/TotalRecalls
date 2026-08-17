window.TR_CONFIG = {
  priceLabel: "$24USD",
  priceNote: "discounted launch price",
  normalPriceLabel: "$49 USD",
  lemonCheckoutUrl: "https://totalrecalls.lemonsqueezy.com/checkout/buy/03e11a51-8c63-4826-8b87-998b626285c3",
  thanksPath: "/thanks/",
  windowsZipUrl: "https://github.com/breakwater2026/totalrecalls-releases/releases/download/v1.3.0/TotalRecalls-windows-x64-v1.3.0.zip",
  versionLabel: "v1.0",
};

(function() {
  var priceLabels = document.querySelectorAll('[data-tr-price]');
  var normalPrices = document.querySelectorAll('[data-tr-normal-price]');
  var buyButtons = document.querySelectorAll('[data-tr-buy]');
  var downloadLinks = document.querySelectorAll('[data-tr-download]');

  priceLabels.forEach(function(el) {
    el.textContent = window.TR_CONFIG.priceLabel;
  });
  normalPrices.forEach(function(el) {
    el.textContent = window.TR_CONFIG.normalPriceLabel;
  });

  var checkoutPending = document.getElementById('checkout-pending');
  if (window.TR_CONFIG.lemonCheckoutUrl) {
    buyButtons.forEach(function(btn) {
      btn.href = window.TR_CONFIG.lemonCheckoutUrl;
      btn.classList.remove('is-pending');
    });
    if (checkoutPending) { checkoutPending.style.display = 'none'; }
  } else {
    if (checkoutPending) { checkoutPending.style.display = 'block'; }
  }

  downloadLinks.forEach(function(link) {
    link.href = window.TR_CONFIG.windowsZipUrl;
  });
})();
