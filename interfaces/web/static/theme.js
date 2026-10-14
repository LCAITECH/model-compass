// Theme switch. The initial theme is applied by a tiny inline script in
// <head> (base.html) before first paint, so there is no flash; this file
// only wires the toggle. localStorage can throw (private mode, blocked
// site data), so every access is guarded and the page works without it.
(function () {
  const root = document.documentElement;

  function systemPrefersDark() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function currentTheme() {
    return root.getAttribute("data-theme") || (systemPrefersDark() ? "dark" : "light");
  }

  document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("theme-toggle");
    if (!button) return;

    function syncLabel() {
      const next = currentTheme() === "dark" ? "light" : "dark";
      button.setAttribute("aria-label", `Switch to ${next} mode`);
      button.setAttribute("title", `Switch to ${next} mode`);
    }

    button.addEventListener("click", () => {
      const next = currentTheme() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try {
        localStorage.setItem("mc-theme", next);
      } catch (e) {}
      syncLabel();
    });

    syncLabel();
  });
})();
