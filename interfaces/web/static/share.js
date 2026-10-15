// Shareable results. The context form submits by GET, so a result's URL
// rebuilds it (the engine is deterministic). This keeps that URL short by
// leaving empty fields out, gives a result reached by POST its link in the
// address bar, and copies the link on request.
(function () {
  document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form.context-form");
    if (form) {
      form.addEventListener("submit", () => {
        form.querySelectorAll("input[name], select[name], textarea[name]").forEach((field) => {
          if (!field.disabled && field.value === "") {
            field.disabled = true;
            field.dataset.shareOmitted = "1";
          }
        });
      });
      // Coming back to the form from the result (back button, bfcache):
      // the omitted fields must be usable again.
      window.addEventListener("pageshow", () => {
        form.querySelectorAll("[data-share-omitted]").forEach((field) => {
          field.disabled = false;
          delete field.dataset.shareOmitted;
        });
      });
    }

    const button = document.querySelector("[data-share-url]");
    if (!button) return;
    const url = new URL(button.dataset.shareUrl, window.location.origin).href;
    if (!window.location.search) history.replaceState(null, "", url);
    const label = button.textContent;
    button.addEventListener("click", async () => {
      button.textContent = (await copy(url)) ? "Link copied" : "Copy it from the address bar";
      setTimeout(() => { button.textContent = label; }, 2400);
    });
  });

  // The Clipboard API needs HTTPS (or localhost) and permission, and where a
  // permission prompt can't show it never settles; after a second, or on
  // refusal, the older execCommand path still works in most browsers.
  async function copy(text) {
    try {
      const timeout = new Promise((resolve, reject) => setTimeout(() => reject(new Error("timeout")), 1000));
      await Promise.race([navigator.clipboard.writeText(text), timeout]);
      return true;
    } catch (e) {
      const area = document.createElement("textarea");
      area.value = text;
      area.setAttribute("readonly", "");
      area.style.cssText = "position:fixed;opacity:0;pointer-events:none";
      document.body.appendChild(area);
      area.select();
      let copied = false;
      try {
        copied = document.execCommand("copy");
      } catch (err) {
        copied = false;
      }
      area.remove();
      return copied;
    }
  }
})();
