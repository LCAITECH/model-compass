// "What if...": change the budget or the priority order and watch the decision
// graph redraw. Every answer comes from the server, which runs the same engine
// on the new context (GET /whatif); this file only holds the controls, asks,
// and hands the result to graph-draw.js. Nothing is computed here.
//
// The scenario lives in the address (history.replaceState, same query as
// GET /recommend), so "Copy link" shares what is on screen. The hero card on
// the left stays the visitor's own result.
(function () {
  document.addEventListener("DOMContentLoaded", () => {
    const panel = document.querySelector("[data-whatif]");
    const G = window.McGraph;
    if (!panel || !G || !G.render || !window.fetch || !window.URLSearchParams) return;

    const options = JSON.parse(panel.dataset.options);
    const baseQuery = panel.dataset.baseQuery;
    const baseParams = new URLSearchParams(baseQuery.split("?")[1] || "");
    const initial = { budget: panel.dataset.budget, priorities: JSON.parse(panel.dataset.priorities) };
    const state = { budget: initial.budget, priorities: initial.priorities.slice() };
    const figure = document.getElementById("decision-graph");
    const part = (name) => panel.querySelector(`[data-whatif-${name}]`);
    const els = {
      budgets: part("budgets"), list: part("priorities"), add: part("add"), addWrap: part("add-wrap"),
      headline: part("headline"), note: part("scenario-note"), open: part("open"), reset: part("reset"),
      nearbyButton: part("nearby"), nearbyBox: part("nearby-box"),
    };
    const labelOf = Object.fromEntries(options.priorities.map((p) => [p.value, p.label]));
    const sameList = (a, b) => a.length === b.length && a.every((value, index) => value === b[index]);
    const isBase = () => state.budget === initial.budget && sameList(state.priorities, initial.priorities);

    function button(text, className, label, onClick, disabled) {
      const b = document.createElement("button");
      b.type = "button";
      b.className = className;
      b.textContent = text;
      if (label) b.setAttribute("aria-label", label);
      b.disabled = !!disabled;
      b.addEventListener("click", onClick);
      return b;
    }

    function renderControls(focusKey) {
      if (els.budgets) {
        els.budgets.textContent = "";
        options.budgets.forEach((budget) => {
          const b = button(budget.label, "whatif-segment", "", () => { state.budget = budget.value; changed(`budget-${budget.value}`); });
          b.setAttribute("role", "radio");
          b.setAttribute("aria-checked", String(state.budget === budget.value));
          b.dataset.key = `budget-${budget.value}`;
          els.budgets.appendChild(b);
        });
      }
      els.list.textContent = "";
      const last = state.priorities.length - 1;
      state.priorities.forEach((value, index) => {
        const li = document.createElement("li");
        li.className = "whatif-priority";
        const rank = document.createElement("span");
        rank.className = "whatif-rank";
        rank.textContent = String(index + 1);
        const name = document.createElement("span");
        name.className = "whatif-pname";
        name.textContent = labelOf[value];
        const move = (to) => { const [item] = state.priorities.splice(index, 1); state.priorities.splice(to, 0, item); };
        const up = button("↑", "whatif-icon", `Move ${labelOf[value]} up`, () => { move(index - 1); changed(`up-${value}`); }, index === 0);
        const down = button("↓", "whatif-icon", `Move ${labelOf[value]} down`, () => { move(index + 1); changed(`down-${value}`); }, index === last);
        const remove = button("×", "whatif-icon", `Remove ${labelOf[value]}`, () => { state.priorities.splice(index, 1); changed("add"); }, last === 0);
        up.dataset.key = `up-${value}`;
        down.dataset.key = `down-${value}`;
        li.append(rank, name, up, down, remove);
        els.list.appendChild(li);
      });
      const free = options.priorities.filter((p) => !state.priorities.includes(p.value));
      els.addWrap.hidden = state.priorities.length >= options.max_priorities || !free.length;
      els.add.textContent = "";
      const placeholder = new Option("Add a priority…", "");
      els.add.appendChild(placeholder);
      free.forEach((p) => els.add.appendChild(new Option(p.label, p.value)));
      els.add.value = "";
      els.reset.hidden = isBase();
      // Keep the keyboard where it was; a move that ends at an edge disables
      // its own button, so fall back to the opposite move of the same item.
      const opposite = focusKey && focusKey.replace(/^(up|down)-/, (m, d) => (d === "up" ? "down-" : "up-"));
      const target = [focusKey, opposite].map((key) => key && panel.querySelector(`[data-key="${key}"]`)).find((el) => el && !el.disabled);
      if (target) target.focus();
      else if (focusKey === "add" && !els.addWrap.hidden) els.add.focus();
    }

    els.add.addEventListener("change", () => {
      if (els.add.value) { state.priorities.push(els.add.value); changed("add"); }
    });

    function paramsFor() {
      const params = new URLSearchParams(baseParams);
      if (initial.budget) params.set("budget", state.budget);
      [1, 2, 3].forEach((n) => params.delete(`priority_${n}`));
      state.priorities.forEach((value, index) => params.set(`priority_${index + 1}`, value));
      return params;
    }

    function setAddress(query) {
      try { window.history.replaceState(null, "", query); } catch (e) {}
      const share = document.querySelector("[data-share-url]");
      if (share) share.setAttribute("data-share-url", query);
    }

    function showBase() {
      figure.classList.remove("is-empty");
      G.render(G.baseline.items, G.baseline.total);
      els.headline.textContent = "";
      els.note.hidden = true;
      els.reset.hidden = true;
      setAddress(baseQuery);
    }

    function showScenario(data) {
      if (data.winner) {
        figure.classList.remove("is-empty");
        G.render(data.items.map(G.fromJson), data.total_qualifying);
      } else {
        figure.classList.add("is-empty");
      }
      els.headline.textContent = data.headline;
      els.open.setAttribute("href", data.query);
      els.note.hidden = false;
      els.reset.hidden = false;
      setAddress(data.query);
    }

    let timer = null;
    let controller = null;
    function changed(focusKey) {
      renderControls(focusKey);
      window.clearTimeout(timer);
      timer = window.setTimeout(ask, 150);
    }

    async function ask() {
      if (controller) controller.abort();
      if (isBase()) { showBase(); return; }
      controller = new AbortController();
      try {
        const url = `/whatif?${paramsFor().toString()}&from=${encodeURIComponent(baseQuery)}`;
        const response = await fetch(url, { signal: controller.signal, headers: { Accept: "application/json" } });
        const data = await response.json();
        if (!response.ok) { els.headline.textContent = data.error || "This scenario could not be run."; return; }
        showScenario(data);
      } catch (error) {
        if (error.name !== "AbortError") els.headline.textContent = "The server could not be reached to run this scenario.";
      }
    }

    els.reset.addEventListener("click", () => {
      state.budget = initial.budget;
      state.priorities = initial.priorities.slice();
      window.clearTimeout(timer);
      if (controller) controller.abort();
      renderControls();
      showBase();
    });

    // The single-step changes that would give a different winner, for the visitor's own context.
    els.nearbyButton.addEventListener("click", async () => {
      els.nearbyBox.hidden = false;
      els.nearbyBox.textContent = "Running the engine on nearby contexts…";
      try {
        const response = await fetch(`/whatif/neighbors?${baseParams.toString()}`, { headers: { Accept: "application/json" } });
        const data = await response.json();
        if (!response.ok) { els.nearbyBox.textContent = data.error || "This could not be checked."; return; }
        els.nearbyBox.textContent = "";
        const intro = document.createElement("p");
        intro.className = "whatif-nearby-intro";
        els.nearbyBox.appendChild(intro);
        if (!data.changes.length) {
          intro.textContent = `The winner holds under every single-step change (${data.tested} tested).`;
          return;
        }
        intro.textContent = `${data.changes.length} of ${data.tested} single-step changes give a different winner:`;
        const list = document.createElement("ul");
        list.className = "whatif-nearby-list";
        data.changes.forEach((change) => {
          const item = document.createElement("li");
          const b = button("", "whatif-nearby-change", "", () => applyChange(change.set));
          const label = document.createElement("span");
          label.textContent = change.label;
          const winner = document.createElement("strong");
          winner.textContent = change.winner ? change.winner.name : "no model qualifies";
          b.append(label, winner);
          if (change.practically_tied) {
            const tied = document.createElement("em");
            tied.textContent = "practically tied";
            b.appendChild(tied);
          }
          item.appendChild(b);
          list.appendChild(item);
        });
        els.nearbyBox.appendChild(list);
      } catch (error) {
        els.nearbyBox.textContent = "The server could not be reached.";
      }
    });

    function applyChange(set) {
      if (set.budget) state.budget = set.budget;
      if ("priority_1" in set) state.priorities = [1, 2, 3].map((n) => set[`priority_${n}`]).filter(Boolean);
      changed();
    }

    panel.hidden = false;
    renderControls();
  });
})();
