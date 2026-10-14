// "Calculating" interstitial. The engine answers in milliseconds, so the
// animation is a short, honest-looking transition, not a progress meter:
// it shows no percentages, counts or ETA. The stage captions name the
// steps the engine really performs, in order.
//
// Without JS, or with prefers-reduced-motion, the form submits at once.
(function () {
  const SVG_NS = "http://www.w3.org/2000/svg";
  const LAYERS = [3, 5, 6, 5, 3];
  const DURATION_MS = 3000;
  const CONVERGE_AT_MS = 2150; // the last stretch: the network folds into one node
  const WIDTH = 640;
  const HEIGHT = 260;
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
    const svg = el("svg", { viewBox: `0 0 ${WIDTH} ${HEIGHT}`, class: "compute-net", "aria-hidden": "true" });
    const xs = LAYERS.map((_, i) => 40 + (i * (WIDTH - 80)) / (LAYERS.length - 1));
    const points = LAYERS.map((count, layer) =>
      Array.from({ length: count }, (_, i) => ({
        x: xs[layer],
        y: ((i + 1) * HEIGHT) / (count + 1),
        layer,
      }))
    );
    const centerY = HEIGHT / 2;
    const coreX = WIDTH / 2;

    const edges = el("g", { class: "net-edges" });
    const pulses = el("g", { class: "net-pulses" });
    const nodes = el("g", { class: "net-nodes" });
    let edgeIndex = 0;
    points.slice(0, -1).forEach((from, layer) => {
      from.forEach((a) => {
        points[layer + 1].forEach((b) => {
          const delay = layer * 380 + (edgeIndex % 7) * 45;
          const line = el("line", { x1: a.x, y1: a.y, x2: b.x, y2: b.y, class: "net-edge" });
          line.style.setProperty("--d", `${delay}ms`);
          edges.appendChild(line);

          // Every third edge carries a travelling pulse: a dot that rides the
          // edge left to right, restarting while the network is "thinking".
          if (edgeIndex % 3 === 0) {
            const dot = el("circle", { r: 2.6, class: "net-pulse" });
            const motion = el("animateMotion", {
              dur: "1.1s",
              begin: `${delay + 200}ms`,
              repeatCount: "indefinite",
              path: `M${a.x} ${a.y} L${b.x} ${b.y}`,
            });
            dot.appendChild(motion);
            pulses.appendChild(dot);
          }
          edgeIndex += 1;
        });
      });
    });
    points.forEach((layerPoints, layer) => {
      layerPoints.forEach((p, i) => {
        const circle = el("circle", { cx: p.x, cy: p.y, r: 7, class: "net-node" });
        circle.style.setProperty("--d", `${layer * 380 + i * 60}ms`);
        // Where this node slides to when the network converges (the centre).
        circle.style.setProperty("--dx", `${coreX - p.x}px`);
        circle.style.setProperty("--dy", `${centerY - p.y}px`);
        nodes.appendChild(circle);
      });
    });
    const core = el("circle", { cx: coreX, cy: centerY, r: 9, class: "net-core" });
    svg.appendChild(edges);
    svg.appendChild(pulses);
    svg.appendChild(nodes);
    svg.appendChild(core);
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
    panel.appendChild(net);

    const caption = document.createElement("p");
    caption.className = "compute-caption";
    panel.appendChild(caption);

    const sub = document.createElement("p");
    sub.className = "compute-sub";
    sub.textContent = "Deterministic rules, no guessing. The same context always gives the same answer.";
    panel.appendChild(sub);

    overlay.appendChild(panel);
    return { overlay, caption, net };
  }

  document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form.context-form");
    if (!form) return;
    const reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduceMotion) return;

    const { overlay, caption, net } = buildOverlay();
    document.body.appendChild(overlay);
    let timers = [];

    function hide() {
      timers.forEach(clearTimeout);
      timers = [];
      overlay.hidden = true;
      overlay.classList.remove("is-on", "is-converging");
      net.classList.remove("is-converging");
      document.body.classList.remove("is-computing");
    }

    form.addEventListener("submit", (event) => {
      if (event.defaultPrevented || form.dataset.computed === "1") return;
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
