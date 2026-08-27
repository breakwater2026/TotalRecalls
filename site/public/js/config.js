window.TR_CONFIG = {
  priceLabel: "$24USD",
  priceNote: "discounted launch price",
  normalPriceLabel: "$49 USD",
  lemonCheckoutUrl: "https://totalrecalls.lemonsqueezy.com/checkout/buy/03e11a51-8c63-4826-8b87-998b626285c3",
  thanksPath: "/thanks/",
  versionLabel: "v1.0.0",
};

(function() {
  var priceLabels = document.querySelectorAll('[data-tr-price]');
  var normalPrices = document.querySelectorAll('[data-tr-normal-price]');
  var buyButtons = document.querySelectorAll('[data-tr-buy]');

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
})();
