// Decision graph: the result as a network. Every dot is a real model from
// the catalog and its ring is its real standing for the visitor's context:
//   centre  the recommended model
//   ring 1  the top alternatives
//   ring 2  other qualifying models that are practically tied with the winner
//   ring 3  the rest of the qualifying models
//   rim     models that were excluded (language or budget)
// Nothing here is computed: result.html lists the engine's own output in
// .graph-data and this file only draws it. Positions inside a ring are
// spread evenly, so angle carries no meaning; the ring does.
(function () {
  const SVG_NS = "http://www.w3.org/2000/svg";
  const SIZE = 760;
  const C = SIZE / 2;
  const RINGS = {
    alt: { radius: 140, r: 21, spin: 0 },
    tied: { radius: 212, r: 12, spin: 90 },
    out: { radius: 285, r: 7.5, spin: 140 },
    ex: { radius: 346, r: 4.6, spin: 200 },
  };

  function el(name, attrs) {
    const node = document.createElementNS(SVG_NS, name);
    Object.entries(attrs || {}).forEach(([k, v]) => node.setAttribute(k, v));
    return node;
  }

  function read(item) {
    const d = item.dataset;
    let reasons = [];
    try {
      reasons = JSON.parse(d.reasons || "[]");
    } catch (e) {}
    return { ring: d.ring, id: d.id, name: d.name, rank: d.rank, input: d.in, output: d.out, tied: d.tied === "1", reasons };
  }

  function compareHref(centerId, otherId) {
    const link = document.querySelector("a.compare-link");
    if (!link) return null;
    try {
      const url = new URL(link.getAttribute("href"), window.location.origin);
      url.searchParams.delete("m");
      url.searchParams.append("m", centerId);
      url.searchParams.append("m", otherId);
      return url.pathname + url.search;
    } catch (e) {
      return null;
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    const figure = document.getElementById("decision-graph");
    if (!figure) return;
    const items = Array.from(figure.querySelectorAll(".graph-data li")).map(read);
    const center = items.find((m) => m.ring === "center");
    if (!center) return;
    const total = document.querySelector("[data-total-qualifying]");
    const totalQualifying = total ? total.dataset.totalQualifying : "";

    const svg = el("svg", { viewBox: `0 0 ${SIZE} ${SIZE}`, class: "graph-svg", role: "img" });
    svg.setAttribute("aria-label", `Decision graph: ${center.name} at the centre, other models in rings by ranking.`);
    const tip = document.createElement("div");
    tip.className = "graph-tip";
    tip.hidden = true;

    // Guide rings
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

    function place(ring, index, count) {
      const offset = { alt: -90, tied: -70, out: -100, ex: -80 }[ring];
      const angle = ((offset + (360 * index) / Math.max(count, 1)) * Math.PI) / 180;
      return { x: C + Math.cos(angle) * RINGS[ring].radius, y: C + Math.sin(angle) * RINGS[ring].radius };
    }

    const nodes = [];
    Object.keys(RINGS).forEach((key) => {
      const members = items.filter((m) => m.ring === key);
      members.forEach((model, index) => {
        const p = place(key, index, members.length);
        const clickable = key !== "ex";
        if (key === "alt") {
          groups.alt.appendChild(el("line", { x1: C, y1: C, x2: p.x, y2: p.y, class: "graph-edge" }));
          const pulse = el("circle", { r: 3.2, class: "graph-pulse" });
          pulse.appendChild(el("animateMotion", {
            dur: `${2.2 + index * 0.5}s`,
            repeatCount: "indefinite",
            path: `M${C} ${C} L${p.x} ${p.y}`,
          }));
          groups.alt.appendChild(pulse);
        }
        const node = el("circle", { cx: p.x, cy: p.y, r: RINGS[key].r, class: `graph-node node-${key}${model.tied ? " is-tied" : ""}` });
        node.style.setProperty("--i", String(nodes.length));
        if (clickable) node.setAttribute("tabindex", "0");
        node.setAttribute("aria-label", `${model.name}${model.rank ? `, rank ${model.rank}` : ", excluded"}`);
        groups[key].appendChild(node);
        nodes.push({ node, model, key, x: p.x, y: p.y });
        if (key === "alt") {
          const label = el("text", { x: p.x, y: p.y + RINGS.alt.r + 19, class: "graph-label" });
          label.textContent = model.name;
          groups.alt.appendChild(label);
          const rank = el("text", { x: p.x, y: p.y + 5, class: "graph-rank" });
          rank.textContent = `#${model.rank}`;
          groups.alt.appendChild(rank);
        }
      });
    });

    // Centre
    const core = el("g", { class: "graph-center" });
    core.appendChild(el("circle", { cx: C, cy: C, r: 52, class: "graph-halo" }));
    core.appendChild(el("circle", { cx: C, cy: C, r: 34, class: "graph-core" }));
    const one = el("text", { x: C, y: C + 7, class: "graph-core-text" });
    one.textContent = "#1";
    core.appendChild(one);
    svg.appendChild(core);

    function show(entry) {
      const m = entry.model;
      const box = figure.querySelector(".graph-stage").getBoundingClientRect();
      const rect = entry.node.getBoundingClientRect();
      const reasons = m.reasons.slice(0, 2).map((r) => `<li>${r.replace(/</g, "&lt;")}</li>`).join("");
      const place = m.rank ? `#${m.rank} of ${totalQualifying}` : "Excluded";
      const price = m.input ? `$${m.input} / $${m.output} per 1M tokens` : "";
      tip.innerHTML = `<strong></strong><span>${place}${price ? " · " + price : ""}</span>${reasons ? `<ul>${reasons}</ul>` : ""}${
        entry.key !== "ex" && entry.key !== "center" ? "<em>Click to compare with the winner</em>" : ""
      }`;
      tip.querySelector("strong").textContent = m.name;
      tip.hidden = false;
      const left = rect.left - box.left + rect.width / 2;
      tip.style.left = `${Math.min(Math.max(left, 130), box.width - 130)}px`;
      tip.style.top = `${rect.top - box.top - 10}px`;
    }

    nodes.forEach((entry) => {
      entry.node.addEventListener("pointerenter", () => show(entry));
      entry.node.addEventListener("pointerleave", () => { tip.hidden = true; });
      entry.node.addEventListener("focus", () => show(entry));
      entry.node.addEventListener("blur", () => { tip.hidden = true; });
      if (entry.key === "ex") return;
      const go = () => {
        const href = compareHref(center.id, entry.model.id);
        if (href) window.location.href = href;
      };
      entry.node.addEventListener("click", go);
      entry.node.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(); } });
    });

    const stage = figure.querySelector(".graph-stage");
    stage.append(svg, tip);
    figure.classList.add("is-ready");
  });
})();
