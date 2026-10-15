// Catalog notices: the result page's floating dock (collapse, dismiss)
// and the landing radar's scroll-in. The dock starts collapsed on narrow
// screens so it never covers the recommendation itself.
(function () {
  const dock = document.querySelector("[data-notice-dock]");
  if (dock) {
    const handle = dock.querySelector("[data-notice-collapse]");
    const count = dock.querySelector(".notice-dock-count");
    const setCollapsed = (collapsed) => {
      if (collapsed) dock.classList.add("has-collapsed");
      dock.classList.toggle("is-collapsed", collapsed);
      handle.setAttribute("aria-expanded", String(!collapsed));
    };
    if (window.matchMedia("(max-width: 640px)").matches) setCollapsed(true);
    // Open on arrival, then fold into the handle so the dock never keeps
    // covering the decision graph; hovering or touching it cancels that.
    let autoCollapse = window.setTimeout(() => setCollapsed(true), 9000);
    const keepOpen = () => window.clearTimeout(autoCollapse);
    dock.addEventListener("pointerenter", keepOpen);
    dock.addEventListener("focusin", keepOpen);
    handle.addEventListener("click", () => {
      keepOpen();
      setCollapsed(!dock.classList.contains("is-collapsed"));
    });
    dock.querySelectorAll("[data-notice-close]").forEach((button) => {
      button.addEventListener("click", () => {
        button.closest("[data-notice]").classList.add("is-dismissed");
        const left = dock.querySelectorAll("[data-notice]:not(.is-dismissed)").length;
        count.textContent = String(left);
        if (!left) dock.hidden = true;
      });
    });
  }

  const radar = document.querySelector("[data-radar]");
  if (radar && "IntersectionObserver" in window) {
    radar.classList.add("is-armed");
    const observer = new IntersectionObserver((entries) => {
      if (entries.some((entry) => entry.isIntersecting)) {
        radar.classList.add("is-visible");
        observer.disconnect();
      }
    }, { threshold: 0.12 });
    observer.observe(radar);
  }
})();
