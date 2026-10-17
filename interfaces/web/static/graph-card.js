// Decision graph, details: the hover tip and the card that stays open.
//
// The rings spin, so a hover tooltip slid out from under the pointer within
// a second or two. A click, tap or Enter on a dot opens a card that stays
// until closed; while it is open the rings stop (graph-card.css) and the
// chosen dot stays put. `state` is owned by graph-draw.js and read at call
// time, so the same card keeps working after the graph is redrawn.
(function () {
  const G = window.McGraph;

  G.createCard = function (stage, state) {
    const tip = document.createElement("div");
    tip.className = "graph-tip";
    tip.hidden = true;
    const card = document.createElement("div");
    card.className = "graph-card";
    card.setAttribute("role", "dialog");
    card.hidden = true;
    let pinned = null;

    function show(entry) {
      if (pinned) return;
      const m = entry.model;
      const box = stage.getBoundingClientRect();
      const rect = entry.node.getBoundingClientRect();
      const reasons = m.reasons.slice(0, 2).map((r) => `<li>${r.replace(/</g, "&lt;")}</li>`).join("");
      const place = m.rank ? `#${m.rank} of ${state.total}` : "Excluded";
      const price = m.input ? `$${m.input} / $${m.output} per 1M tokens` : "";
      const flags = G.MARKS.filter((mark) => mark.test(m)).map((mark) => mark.text(m)).join(" · ");
      tip.innerHTML = `<strong></strong><span>${place}${price ? " · " + price : ""}</span>${flags ? `<b class="graph-tip-flags">${flags}</b>` : ""}${reasons ? `<ul>${reasons}</ul>` : ""}<em>Click to keep the details open</em>`;
      tip.querySelector("strong").textContent = m.name;
      tip.hidden = false;
      const left = rect.left - box.left + rect.width / 2;
      tip.style.left = `${Math.min(Math.max(left, 130), box.width - 130)}px`;
      tip.style.top = `${rect.top - box.top - 10}px`;
    }

    function placeCard() {
      if (!pinned) return;
      const box = stage.getBoundingClientRect();
      const rect = pinned.node.getBoundingClientRect();
      const half = card.offsetWidth / 2;
      const x = rect.left - box.left + rect.width / 2;
      card.style.left = `${Math.min(Math.max(x, half + 8), box.width - half - 8)}px`;
      const below = rect.top - box.top < card.offsetHeight + 16;
      card.classList.toggle("is-below", below);
      card.style.top = `${below ? rect.bottom - box.top + 12 : rect.top - box.top - 12}px`;
    }

    function unpin(restoreFocus) {
      if (!pinned) return;
      const node = pinned.node;
      node.classList.remove("is-selected");
      pinned = null;
      card.hidden = true;
      stage.classList.remove("is-pinned");
      if (restoreFocus) node.focus();
    }

    function pin(entry, fromKeyboard) {
      if (pinned) pinned.node.classList.remove("is-selected");
      pinned = entry;
      tip.hidden = true;
      const m = entry.model;
      const price = m.input ? `$${m.input} / $${m.output} per 1M tokens` : "";
      const place = m.rank ? `#${m.rank} of ${state.total}` : "";
      const flags = G.MARKS.filter((mark) => mark.test(m)).map((mark) => mark.text(m));
      const href = G.compareHref(state.center.id, m.id);
      card.innerHTML = `<button type="button" class="graph-card-close" aria-label="Close details">&times;</button>
        <p class="graph-card-ring"></p><h3 class="graph-card-name"></h3>
        <p class="graph-card-meta"></p>
        ${flags.length ? '<p class="graph-card-flags"></p>' : ""}
        <ul class="graph-card-reasons"></ul>
        ${href ? '<a class="graph-card-compare"></a>' : ""}`;
      card.querySelector(".graph-card-ring").textContent = G.RING_LABELS[entry.key];
      card.querySelector(".graph-card-name").textContent = m.name;
      card.querySelector(".graph-card-meta").textContent = [place, price].filter(Boolean).join(" · ");
      if (flags.length) card.querySelector(".graph-card-flags").textContent = flags.join(" · ");
      card.setAttribute("aria-label", m.name);
      const list = card.querySelector(".graph-card-reasons");
      m.reasons.forEach((reason) => {
        const li = document.createElement("li");
        li.textContent = reason;
        list.appendChild(li);
      });
      const compare = card.querySelector(".graph-card-compare");
      if (compare) {
        compare.setAttribute("href", href);
        compare.textContent = `Compare with ${state.center.name} →`;
      }
      card.querySelector(".graph-card-close").addEventListener("click", () => unpin(true));
      card.hidden = false;
      entry.node.classList.add("is-selected");
      stage.classList.add("is-pinned");
      placeCard();
      if (fromKeyboard) card.querySelector(".graph-card-close").focus();
    }

    // Once per dot: the entry's model and ring are read at event time.
    function bind(entry) {
      const node = entry.node;
      node.setAttribute("tabindex", "0");
      node.addEventListener("pointerenter", () => show(entry));
      node.addEventListener("pointerleave", () => { tip.hidden = true; });
      node.addEventListener("focus", () => show(entry));
      node.addEventListener("blur", () => { tip.hidden = true; });
      node.addEventListener("click", () => (pinned === entry ? unpin(false) : pin(entry, false)));
      node.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pin(entry, true); }
      });
    }

    // Before a redraw: nothing stays open over dots that are about to move.
    function reset() {
      unpin(false);
      tip.hidden = true;
    }

    document.addEventListener("keydown", (e) => { if (e.key === "Escape") unpin(true); });
    document.addEventListener("pointerdown", (e) => {
      if (pinned && !card.contains(e.target) && !state.entries.some((entry) => entry.node === e.target)) unpin(false);
    });
    window.addEventListener("resize", placeCard);

    return { tip, card, bind, reset };
  };
})();
