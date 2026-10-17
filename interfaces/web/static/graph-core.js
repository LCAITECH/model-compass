// Decision graph, shared pieces: the geometry, what each ring means, the
// dated marks a dot can carry, and one shape for the engine's items whether
// they come from the page's hidden list (first paint) or from the what-if
// endpoint (every later redraw).
//
// The graph is a picture of the engine's own output: a dot per catalog model,
// its ring is its real standing for the visitor's context. Nothing is
// computed here; angle inside a ring carries no meaning.
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

  // Dated facts about a model (see catalog_notices.py), as graph marks and a tooltip line.
  const MARKS = [
    { key: "promo", test: (m) => m.promo, label: "Intro price", text: (m) => `Intro price until ${m.promo}` },
    { key: "new", test: (m) => m.isNew, label: "New release", text: () => "New release" },
    {
      key: "retiring", test: (m) => m.retiring, label: "Leaving",
      text: (m) => (m.deprecated ? "Deprecated" : "Retiring") + (m.retiring === "routed" ? ", routed to its successor" : ` · ${m.retiring}`),
    },
  ];

  // What each ring means, said once on the card instead of read off the legend.
  const RING_LABELS = {
    alt: "Top alternative",
    tied: "Practically tied with the winner",
    out: "Also qualifies",
    ex: "Excluded for your context",
  };

  function el(name, attrs) {
    const node = document.createElementNS(SVG_NS, name);
    Object.entries(attrs || {}).forEach(([k, v]) => node.setAttribute(k, v));
    return node;
  }

  // An item as the page lists it (data-* attributes of the hidden list).
  function fromList(item) {
    const d = item.dataset;
    let reasons = [];
    try {
      reasons = JSON.parse(d.reasons || "[]");
    } catch (e) {}
    return {
      ring: d.ring, id: d.id, name: d.name, rank: d.rank, input: d.in, output: d.out, tied: d.tied === "1", reasons,
      isNew: d.new === "1", promo: d.promo || "", retiring: d.retiring || "", deprecated: d.deprecated === "1",
    };
  }

  // An item as interfaces/web/graph_data.py returns it as JSON.
  function fromJson(raw) {
    return {
      ring: raw.ring, id: raw.id, name: raw.name, rank: raw.rank, input: raw.input, output: raw.output,
      tied: !!raw.tied, reasons: raw.reasons || [],
      isNew: !!raw.is_new, promo: raw.promo || "", retiring: raw.retiring || "", deprecated: !!raw.deprecated,
    };
  }

  function compareHref(centerId, otherId) {
    // By destination: the hero also has a compare-link to /plans, listed first.
    const link = document.querySelector('a.compare-link[href^="/compare"]');
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

  window.McGraph = { SVG_NS, SIZE, C, RINGS, MARKS, RING_LABELS, el, fromList, fromJson, compareHref };
})();
