/* Site-wide runtime config + checkout wiring.
 *
 * Checkout is Paddle.js (Paddle Billing). There is NO "checkout link" URL in
 * Paddle Billing: a checkout is opened client-side from a price (+ optional
 * discount), or from a server-created transaction's `checkout.url`. The old
 * `paddleCheckoutUrl` pointing at pay.paddle.io/checkout/hsc_… was never a real
 * Paddle Billing construct (GET /checkout-links returns 404), so it dead-ended
 * every buyer.
 *
 * The client-side token below is public by design — it ships in the page. The
 * SECRET API key (pdl_live_apikey_…) must never appear here.
 */
window.TR_CONFIG = {
  // TEMPORARY LIVE-TEST VALUES (2026-09-26). The Paddle list price is set to
  // 0.99 and the 50% launch discount is paused at checkout, because Paddle
  // refuses to charge below 70 minor units (USD 0.70), so 0.99 - 50% = 0.49
  // could not be charged at all. Revert all four lines with the price.
  priceLabel: "$0.99 USD",
  priceNote: "test price",
  normalPriceLabel: "",
  paddleClientToken: "live_bcdb7746fc6d13a152b0431abf5",
  paddlePriceId: "pri_01m37qpx77bst2w1gnf3zkf4zd",
  paddleDiscountId: "",
  successPath: "/thanks/",
  thanksPath: "/thanks/",
  versionLabel: "v1.0.0",
};

(function () {
  var cfg = window.TR_CONFIG;

  document.querySelectorAll("[data-tr-price]").forEach(function (el) {
    el.textContent = cfg.priceLabel;
  });
  document.querySelectorAll("[data-tr-normal-price]").forEach(function (el) {
    el.textContent = cfg.normalPriceLabel;
  });

  var paddleReady = null;
  function loadPaddle() {
    if (paddleReady) { return paddleReady; }
    paddleReady = new Promise(function (resolve, reject) {
      function init() {
        if (!window.Paddle) { reject(new Error("Paddle.js missing")); return; }
        try {
          window.Paddle.Initialize({ token: cfg.paddleClientToken });
        } catch (err) {
          /* re-initialising an already-initialised Paddle is harmless */
        }
        resolve(window.Paddle);
      }
      if (window.Paddle) { init(); return; }
      var script = document.createElement("script");
      script.src = "https://cdn.paddle.com/paddle/v2/paddle.js";
      script.async = true;
      script.onload = init;
      script.onerror = function () { reject(new Error("Paddle.js failed to load")); };
      document.head.appendChild(script);
    });
    return paddleReady;
  }

  var buyButtons = document.querySelectorAll("[data-tr-buy]");
  var checkoutPending = document.getElementById("checkout-pending");

  buyButtons.forEach(function (btn) {
    btn.addEventListener("click", function (event) {
      event.preventDefault();
      var original = btn.getAttribute("data-tr-label") || btn.textContent;
      btn.classList.add("is-pending");
      loadPaddle().then(function (Paddle) {
        btn.classList.remove("is-pending");
        Paddle.Checkout.open({
          items: [{ priceId: cfg.paddlePriceId, quantity: 1 }],
          discountId: cfg.paddleDiscountId || undefined,
          settings: {
            displayMode: "overlay",
            theme: "light",
            locale: "en",
            successUrl: new URL(cfg.successPath, window.location.origin).href,
          },
        });
      }).catch(function () {
        /* Never leave a buyer on a dead button. */
        btn.classList.remove("is-pending");
        btn.textContent = "Checkout unavailable — please retry";
        setTimeout(function () { btn.textContent = original; }, 4000);
      });
    });
  });

  // Paddle builds a checkout payment link as: <default payment link>?_ptxn=<txn_id>
  // Paddle.js is expected to open that transaction automatically, provided it is
  // present and initialised. The normal flow loads it lazily on the first Buy
  // click, so a buyer arriving on a Paddle-issued link (payment-method updates,
  // invoice links) would otherwise land on a page that never opens their
  // checkout. Load eagerly when _ptxn is present.
  if (new URLSearchParams(window.location.search).has("_ptxn")) {
    loadPaddle().catch(function () {
      /* the page still renders and the Buy button still works */
    });
  }

  if (checkoutPending) {
    checkoutPending.style.display = buyButtons.length ? "none" : "block";
  }
})();
