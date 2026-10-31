// Decision graph, drawing: the result as a network. Every dot is a real model
// from the catalog and its ring is its real standing for the visitor's context:
//   centre  the recommended model
//   ring 1  the top alternatives
//   ring 2  other qualifying models that are practically tied with the winner
//   ring 3  the rest of the qualifying models
//   rim     models that were excluded (language, budget or provider status)
//
// render(items, total) draws whatever it is given and can be called again: a
// dot is created once per model and then only moves. The first paint reads
// the page's hidden list; the what-if panel (whatif.js) calls render with the
// items the server computed for another context. Nothing is computed here.
(function () {
  const G = window.McGraph;
  const { RINGS, MARKS, C, el } = G;

  function place(ring, index, count) {
    const offset = { alt: -90, tied: -70, out: -100, ex: -80 }[ring];
    const angle = ((offset + (360 * index) / Math.max(count, 1)) * Math.PI) / 180;
    return { x: C + Math.cos(angle) * RINGS[ring].radius, y: C + Math.sin(angle) * RINGS[ring].radius };
  }

  document.addEventListener("DOMContentLoaded", () => {
    const figure = document.getElementById("decision-graph");
    if (!figure) return;
    const initial = Array.from(figure.querySelectorAll(".graph-data li")).map(G.fromList);
    if (!initial.some((m) => m.ring === "center")) return;

    const stage = figure.querySelector(".graph-stage");
    const svg = el("svg", { viewBox: `0 0 ${G.SIZE} ${G.SIZE}`, class: "graph-svg", role: "img" });
    Object.values(RINGS).forEach((ring) => {
      svg.appendChild(el("circle", { cx: C, cy: C, r: ring.radius, class: "graph-guide" }));
    });
    const groups = {};
    Object.keys(RINGS).forEach((key) => {
      const group = el("g", { class: `graph-ring ring-${key}` });
      group.style.setProperty("--spin", `${RINGS[key].spin}s`);
      groups[key] = group;
      svg.appendChild(group);
    });
    const core = el("g", { class: "graph-center" });
    core.appendChild(el("circle", { cx: C, cy: C, r: 52, class: "graph-halo" }));
    core.appendChild(el("circle", { cx: C, cy: C, r: 34, class: "graph-core" }));
    const one = el("text", { x: C, y: C + 7, class: "graph-core-text" });
    one.textContent = "#1";
    core.appendChild(one);
    svg.appendChild(core);

    const state = { center: null, total: figure.dataset.totalQualifying || "", entries: [] };
    const ui = G.createCard(stage, state);
    const records = new Map();
    const legend = figure.querySelector(".graph-legend");

    // The dot for one model: its circle, marks and (top alternatives) label,
    // grouped so they travel together when it changes ring.
    function createRecord(order) {
      const record = { dot: el("g", { class: "graph-dot" }), node: el("circle", {}), model: null, key: null, placed: false };
      record.node.style.setProperty("--i", String(order));
      ui.bind(record);
      return record;
    }

    function updateRecord(record, model, key, p) {
      const node = record.node;
      record.model = model;
      record.key = key;
      node.setAttribute("cx", p.x);
      node.setAttribute("cy", p.y);
      node.setAttribute("r", RINGS[key].r);
      node.classList.remove("node-alt", "node-tied", "node-out", "node-ex", "is-tied");
      node.classList.add("graph-node", `node-${key}`);
      if (model.tied) node.classList.add("is-tied");
      node.setAttribute("aria-label", `${model.name}${model.rank ? `, rank ${model.rank}` : ", excluded"}`);
      Array.from(record.dot.children).forEach((child) => { if (child !== node) child.remove(); });
      record.dot.prepend(node);
      MARKS.filter((mark) => mark.test(model)).forEach((mark, n) => {
        record.dot.appendChild(el("circle", { cx: p.x, cy: p.y, r: RINGS[key].r + 4 + n * 4, class: `graph-mark graph-mark-${mark.key}` }));
      });
      if (key === "alt") {
        const label = el("text", { x: p.x, y: p.y + RINGS.alt.r + 19, class: "graph-label" });
        label.textContent = model.name;
        record.dot.appendChild(label);
        const rank = el("text", { x: p.x, y: p.y + 5, class: "graph-rank" });
        rank.textContent = `#${model.rank}`;
        record.dot.appendChild(rank);
      }
    }

    // The top alternatives hang off the centre by an edge with a pulse of light.
    function addEdge(index, p) {
      const pulse = el("circle", { r: 3.2, class: "graph-pulse" });
      pulse.appendChild(el("animateMotion", {
        dur: `${2.2 + index * 0.5}s`,
        repeatCount: "indefinite",
        path: `M${C} ${C} L${p.x} ${p.y}`,
      }));
      groups.alt.prepend(pulse);
      groups.alt.prepend(el("line", { x1: C, y1: C, x2: p.x, y2: p.y, class: "graph-edge" }));
    }

    // FLIP: dots that changed ring glide from where they were drawn to where
    // they now belong. The ring groups keep their own rotation, so a dot that
    // did not move is not disturbed.
    function glide(before) {
      const scale = svg.getBoundingClientRect().width / G.SIZE || 1;
      const moving = [];
      records.forEach((record, id) => {
        const from = before.get(id);
        if (!from) return;
        const to = record.node.getBoundingClientRect();
        const dx = (from.left + from.width / 2 - (to.left + to.width / 2)) / scale;
        const dy = (from.top + from.height / 2 - (to.top + to.height / 2)) / scale;
        if (Math.abs(dx) + Math.abs(dy) < 1) return;
        record.dot.style.transition = "none";
        record.dot.style.transform = `translate(${dx}px, ${dy}px)`;
        moving.push(record);
      });
      void svg.getBoundingClientRect();
      moving.forEach((record) => {
        record.dot.style.transition = "transform 700ms cubic-bezier(0.2, 0.8, 0.2, 1)";
        record.dot.style.transform = "";
      });
      window.setTimeout(() => moving.forEach((record) => { record.dot.style.transition = ""; }), 800);
    }

    function updateLegend(items) {
      const counts = { alt: 0, tied: 0, out: 0, ex: 0 };
      // Same rule as ring_counts() in graph_data.py: a tied top alternative
      // also counts as practically tied.
      items.forEach((m) => {
        if (counts[m.ring] !== undefined) counts[m.ring] += 1;
        if (m.ring === "alt" && m.tied) counts.tied += 1;
      });
      figure.querySelectorAll("[data-ring-count]").forEach((span) => { span.textContent = String(counts[span.dataset.ringCount]); });
      if (!legend) return;
      legend.querySelectorAll(".is-mark-key").forEach((li) => li.remove());
      MARKS.filter((mark) => items.some(mark.test)).forEach((mark) => {
        const li = document.createElement("li");
        li.className = "is-mark-key";
        li.innerHTML = `<span class="key key-mark" style="--mark: var(--tone-${mark.key === "retiring" ? "retire" : mark.key})"></span>${mark.label}`;
        legend.appendChild(li);
      });
    }

    function render(items, total) {
      const animate = records.size > 0 && document.documentElement.getAttribute("data-effects") === "on";
      const before = new Map();
      if (animate) records.forEach((record, id) => { if (record.placed) before.set(id, record.node.getBoundingClientRect()); });
      ui.reset();

      state.center = items.find((m) => m.ring === "center");
      state.total = String(total || "");
      figure.dataset.totalQualifying = state.total;
      svg.setAttribute("aria-label", `Decision graph: ${state.center.name} at the centre, other models in rings by ranking.`);
      groups.alt.querySelectorAll(".graph-edge, .graph-pulse").forEach((node) => node.remove());

      let order = 0;
      const placed = new Set();
      Object.keys(RINGS).forEach((key) => {
        const members = items.filter((m) => m.ring === key);
        members.forEach((model, index) => {
          const p = place(key, index, members.length);
          let record = records.get(model.id);
          if (record) record.node.classList.add("is-settled"); // already entered: no entrance animation on a move
          else records.set(model.id, (record = createRecord(order)));
          updateRecord(record, model, key, p);
          groups[key].appendChild(record.dot);
          record.placed = true;
          placed.add(model.id);
          if (key === "alt") addEdge(index, p);
          order += 1;
        });
      });
      // The winner sits in the centre, not on a ring: its dot leaves its old one.
      records.forEach((record, id) => {
        if (!placed.has(id)) { record.dot.remove(); record.placed = false; }
      });
      state.entries = Array.from(records.values()).filter((record) => record.placed);
      updateLegend(items);
      if (animate) glide(before);
    }

    render(initial, state.total);
    stage.append(svg, ui.tip, ui.card);
    figure.classList.add("is-ready");

    // For whatif.js: redraw with another context's items; `baseline` is what the page was rendered with.
    G.baseline = { items: initial, total: state.total };
    G.render = (items, total) => render(items, total);
  });
})();
