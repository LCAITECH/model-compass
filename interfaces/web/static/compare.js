// Comparator enhancements. All optional: without this file the picker is
// a plain list of submit buttons, the bars are drawn at full length and
// the mobile cards scroll on their own.
//  1. the "Add a model" search filters the list as you type, and Enter
//     adds the first match instead of submitting the whole form;
//  2. the bars in the side-by-side grow in when the board scrolls into view;
//  3. on narrow screens, the dot under the cards follows the card in view.
(function () {
  function setupSearch() {
    const input = document.querySelector("[data-picker-search]");
    if (!input) return;
    const groups = Array.from(document.querySelectorAll("[data-picker-group]"));
    const none = document.querySelector("[data-picker-none]");

    function visibleOptions() {
      return groups.flatMap((group) =>
        Array.from(group.querySelectorAll(".picker-option")).filter((option) => !option.hidden && !option.disabled)
      );
    }

    input.addEventListener("input", () => {
      const query = input.value.trim().toLowerCase();
      let shown = 0;
      groups.forEach((group) => {
        let groupShown = 0;
        group.querySelectorAll(".picker-option").forEach((option) => {
          const match = !query || option.dataset.search.includes(query);
          option.hidden = !match;
          if (match) groupShown += 1;
        });
        group.hidden = groupShown === 0;
        shown += groupShown;
      });
      if (none) none.hidden = shown > 0;
    });

    input.addEventListener("keydown", (event) => {
      if (event.key !== "Enter") return;
      event.preventDefault();
      const first = visibleOptions()[0];
      if (first && input.value.trim()) first.click();
    });

    const details = input.closest("details");
    if (details) {
      details.addEventListener("toggle", () => {
        if (details.open) input.focus({ preventScroll: true });
      });
    }
  }

  function setupBars() {
    const board = document.querySelector(".compare-board");
    if (!board || !("IntersectionObserver" in window)) return;
    board.classList.add("is-armed");
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((entry) => entry.isIntersecting)) {
          board.classList.add("is-revealed");
          observer.disconnect();
        }
      },
      { threshold: 0.05 }
    );
    observer.observe(board);
    // A pane that never paints never reports an intersection; never leave
    // the bars at zero length because of that.
    setTimeout(() => board.classList.add("is-revealed"), 4000);
  }

  function setupCards() {
    const track = document.querySelector("[data-cards]");
    const dots = Array.from(document.querySelectorAll("[data-card-dot]"));
    if (!track || !dots.length) return;
    const cards = Array.from(track.children);

    function mark(index) {
      dots.forEach((dot, i) => dot.classList.toggle("is-active", i === index));
    }

    dots.forEach((dot, i) => {
      dot.addEventListener("click", (event) => {
        event.preventDefault();
        track.scrollTo({ left: cards[i].offsetLeft - track.offsetLeft, behavior: "smooth" });
      });
    });

    track.addEventListener(
      "scroll",
      () => {
        const center = track.scrollLeft + track.clientWidth / 2;
        let nearest = 0;
        cards.forEach((card, i) => {
          const mid = card.offsetLeft - track.offsetLeft + card.offsetWidth / 2;
          const best = cards[nearest].offsetLeft - track.offsetLeft + cards[nearest].offsetWidth / 2;
          if (Math.abs(mid - center) < Math.abs(best - center)) nearest = i;
        });
        mark(nearest);
      },
      { passive: true }
    );
    mark(0);
  }

  function init() {
    setupSearch();
    setupBars();
    setupCards();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
