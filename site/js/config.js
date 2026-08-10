/**
 * TotalRecalls site config — edit after Lemon Squeezy product is created.
 * Lemon dashboard → Product → Share → Checkout link (or overlay).
 */
window.TR_CONFIG = {
  priceLabel: "$24",
  priceNote: "one-time · Windows",
  // Paste full checkout URL from Lemon Squeezy, e.g.
  // "https://YOURSTORE.lemonsqueezy.com/checkout/buy/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  lemonCheckoutUrl: "",
  // Thank-you page after successful payment (set this URL in Lemon "Confirmation" / redirect)
  thanksPath: "/thanks.html",
  // Direct zip (also attach the same file inside Lemon as the digital download)
  windowsZipUrl:
    "https://github.com/breakwater2026/TotalRecalls/releases/download/v1.3.0/TotalRecalls-windows-x64-v1.3.0.zip",
  versionLabel: "v1.3.0",
};

(function () {
  var c = window.TR_CONFIG || {};
  var buyHref = (c.lemonCheckoutUrl || "").trim();
  var zip = c.windowsZipUrl || "#";
  var price = c.priceLabel || "$24";

  function wireBuy(el) {
    if (!el) return;
    if (buyHref && buyHref.indexOf("http") === 0) {
      el.setAttribute("href", buyHref);
      el.classList.remove("is-pending");
      if (el.dataset.labelReady) el.textContent = el.dataset.labelReady.replace("{price}", price);
    } else {
      el.setAttribute("href", "#get-totalrecalls");
      el.classList.add("is-pending");
      if (el.dataset.labelPending) el.textContent = el.dataset.labelPending.replace("{price}", price);
    }
  }

  document.querySelectorAll("[data-tr-buy]").forEach(wireBuy);

  document.querySelectorAll("[data-tr-download]").forEach(function (el) {
    el.setAttribute("href", zip);
  });

  document.querySelectorAll("[data-tr-price]").forEach(function (el) {
    el.textContent = price;
  });

  document.querySelectorAll("[data-tr-price-note]").forEach(function (el) {
    el.textContent = c.priceNote || "one-time";
  });

  var banner = document.getElementById("checkout-pending");
  if (banner) {
    banner.hidden = !!(buyHref && buyHref.indexOf("http") === 0);
  }
})();
