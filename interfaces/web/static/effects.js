// Visual effects switch. Effects are ON by default (owner decision,
// 2026-10-14) and a visitor can turn them off with the header button; the
// choice is kept in localStorage. The initial value is applied by an inline
// script in <head> so there is no flash, and every effect (CSS and JS)
// keys off html[data-effects="on"] instead of the OS motion preference.
// Without JS the attribute is never set, so the page is static.
(function () {
  const root = document.documentElement;
  const MC = (window.MC = window.MC || {});
  const listeners = [];

  MC.effectsOn = () => root.getAttribute("data-effects") === "on";
  MC.onEffectsChange = (fn) => listeners.push(fn);

  function setEffects(on) {
    root.setAttribute("data-effects", on ? "on" : "off");
    try {
      localStorage.setItem("mc-effects", on ? "on" : "off");
    } catch (e) {}
    listeners.forEach((fn) => fn(on));
  }

  document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("effects-toggle");
    if (!button) return;

    function sync() {
      const on = MC.effectsOn();
      button.setAttribute("aria-pressed", on ? "true" : "false");
      button.setAttribute("title", on ? "Turn visual effects off" : "Turn visual effects on");
      button.setAttribute("aria-label", on ? "Turn visual effects off" : "Turn visual effects on");
    }

    button.addEventListener("click", () => {
      setEffects(!MC.effectsOn());
      sync();
    });
    sync();
  });
})();
