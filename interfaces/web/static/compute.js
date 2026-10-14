// "Calculating" interstitial. The engine answers in milliseconds, so this
// is a short transition, not a progress meter: it shows no percentages,
// counts or ETA. The stage captions name the steps the engine really
// performs, in order. A full-screen network lights up left to right,
// pulses ride its connections, and at the end it folds into one node that
// flashes into the result.
//
// Skipped (the form submits at once) when effects are off or JS is absent.
(function () {
  const SVG_NS = "http://www.w3.org/2000/svg";
  const LAYERS = [3, 6, 8, 9, 8, 6, 3];
  const DURATION_MS = 3300;
  const CONVERGE_AT_MS = 2300;
  const FLASH_AT_MS = 2950;
  const WIDTH = 1200;
  const HEIGHT = 440;
  const STAGES = [
    "Reading your context",
    "Filtering by language and budget",
    "Weighing your priorities",
    "Ranking the qualifying models",
  ];

  function el(name, attrs) {
    const node = document.createElementNS(SVG_NS, name);
    Object.entries(attrs || {}).forEach(([key, value]) => node.setAttribute(key, value));
    return node;
  }

  function buildNetwork() {
    const svg = el("svg", {
      viewBox: `0 0 ${WIDTH} ${HEIGHT}`,
      class: "compute-net",
      preserveAspectRatio: "xMidYMid meet",
      "aria-hidden": "true",
    });
    const xs = LAYERS.map((_, i) => 60 + (i * (WIDTH - 120)) / (LAYERS.length - 1));
    const points = LAYERS.map((count, layer) =>
      Array.from({ length: count }, (_, i) => ({ x: xs[layer], y: ((i + 1) * HEIGHT) / (count + 1), layer }))
    );
    const centerX = WIDTH / 2;
    const centerY = HEIGHT / 2;

    const edges = el("g", { class: "net-edges" });
    const pulses = el("g", { class: "net-pulses" });
    const nodes = el("g", { class: "net-nodes" });
    let edgeIndex = 0;
    points.slice(0, -1).forEach((from, layer) => {
      from.forEach((a) => {
        points[layer + 1].forEach((b) => {
          const delay = layer * 330 + (edgeIndex % 9) * 40;
          const line = el("line", { x1: a.x, y1: a.y, x2: b.x, y2: b.y, class: "net-edge" });
          line.style.setProperty("--d", `${delay}ms`);
          edges.appendChild(line);
          if (edgeIndex % 2 === 0) {
            const dot = el("circle", { r: 3, class: "net-pulse" });
            dot.appendChild(
              el("animateMotion", {
                dur: `${0.9 + (edgeIndex % 5) * 0.12}s`,
                begin: `${delay + 150}ms`,
                repeatCount: "indefinite",
                path: `M${a.x} ${a.y} L${b.x} ${b.y}`,
              })
            );
            pulses.appendChild(dot);
          }
          edgeIndex += 1;
        });
      });
    });
    points.forEach((layerPoints, layer) => {
      layerPoints.forEach((p, i) => {
        const circle = el("circle", { cx: p.x, cy: p.y, r: 8, class: "net-node" });
        circle.style.setProperty("--d", `${layer * 330 + i * 50}ms`);
        circle.style.setProperty("--dx", `${centerX - p.x}px`);
        circle.style.setProperty("--dy", `${centerY - p.y}px`);
        nodes.appendChild(circle);
      });
    });
    svg.append(edges, pulses, nodes, el("circle", { cx: centerX, cy: centerY, r: 10, class: "net-core" }));
    return svg;
  }

  function buildOverlay() {
    const overlay = document.createElement("div");
    overlay.className = "compute-overlay";
    overlay.setAttribute("role", "status");
    overlay.setAttribute("aria-live", "polite");
    overlay.hidden = true;

    const panel = document.createElement("div");
    panel.className = "compute-panel";
    const net = buildNetwork();
    const caption = document.createElement("p");
    caption.className = "compute-caption";
    const sub = document.createElement("p");
    sub.className = "compute-sub";
    sub.textContent = "Deterministic rules, no guessing. The same context always gives the same answer.";
    panel.append(net, caption, sub);

    const flash = document.createElement("div");
    flash.className = "compute-flash";
    overlay.append(panel, flash);
    return { overlay, caption, net };
  }

  document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form.context-form");
    if (!form) return;

    const { overlay, caption, net } = buildOverlay();
    document.body.appendChild(overlay);
    let timers = [];

    function hide() {
      timers.forEach(clearTimeout);
      timers = [];
      overlay.hidden = true;
      overlay.classList.remove("is-on", "is-converging", "is-flash");
      net.classList.remove("is-converging");
      document.body.classList.remove("is-computing");
    }

    form.addEventListener("submit", (event) => {
      if (event.defaultPrevented || form.dataset.computed === "1") return;
      if (!window.MC || !MC.effectsOn || !MC.effectsOn()) return;
      event.preventDefault();
      form.dataset.computed = "1";

      overlay.hidden = false;
      document.body.classList.add("is-computing");
      requestAnimationFrame(() => overlay.classList.add("is-on"));

      STAGES.forEach((text, i) => {
        timers.push(setTimeout(() => { caption.textContent = text; }, (i * CONVERGE_AT_MS) / STAGES.length));
      });
      timers.push(setTimeout(() => {
        net.classList.add("is-converging");
        overlay.classList.add("is-converging");
        caption.textContent = "Your match";
      }, CONVERGE_AT_MS));
      timers.push(setTimeout(() => overlay.classList.add("is-flash"), FLASH_AT_MS));
      timers.push(setTimeout(() => form.submit(), DURATION_MS));
    });

    // Back/forward cache restores the page with the overlay still up.
    window.addEventListener("pageshow", (event) => {
      if (event.persisted) {
        delete form.dataset.computed;
        hide();
      }
    });
  });
})();
