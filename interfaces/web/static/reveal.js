// Result-page reveal. Two effects, both decorative:
//  1. the recommended model's name "decrypts" in place (scrambled glyphs
//     resolve left to right into the real name, then the card pulses);
//  2. the cards below enter in a cascade as they scroll into view.
// The real text is in the markup from the start (and in aria-label), so
// nothing depends on this running; with prefers-reduced-motion, or any
// failure, the page is simply already in its final state.
(function () {
  const GLYPHS = "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789#%&*+=?";
  const SETTLE_MS = 55; // per-character resolve interval
  const START_DELAY_MS = 350;

  function scramble(heading, onDone) {
    const finalText = heading.textContent.trim();
    heading.setAttribute("aria-label", finalText);
    const started = performance.now() + START_DELAY_MS;
    heading.style.minHeight = `${heading.offsetHeight}px`;

    // setTimeout rather than requestAnimationFrame: it keeps running in a
    // tab that is not being painted, so the label never gets stuck.
    function frame() {
      const elapsed = performance.now() - started;
      if (elapsed < 0) {
        heading.textContent = finalText.replace(/[^\s.\-]/g, () => GLYPHS[Math.floor(Math.random() * GLYPHS.length)]);
        setTimeout(frame, 40);
        return;
      }
      const resolved = Math.floor(elapsed / SETTLE_MS);
      let out = "";
      for (let i = 0; i < finalText.length; i += 1) {
        const ch = finalText[i];
        out += i < resolved || /[\s.\-]/.test(ch) ? ch : GLYPHS[Math.floor(Math.random() * GLYPHS.length)];
      }
      heading.textContent = out;
      if (resolved >= finalText.length) {
        heading.textContent = finalText;
        heading.style.minHeight = "";
        onDone();
        return;
      }
      setTimeout(frame, 40);
    }
    frame();
  }

  function cascade() {
    const items = Array.from(
      document.querySelectorAll(".fade-in > .card:not(.card-featured), .alternatives-grid .card")
    );
    if (!items.length || !("IntersectionObserver" in window)) return;

    items.forEach((item, i) => {
      item.classList.add("cascade-item");
      item.style.setProperty("--i", String(i % 4));
    });
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-in");
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.1 }
    );
    items.forEach((item) => observer.observe(item));
    // Safety net: never leave content hidden if the observer misbehaves.
    setTimeout(() => items.forEach((item) => item.classList.add("is-in")), 4000);
  }

  document.addEventListener("DOMContentLoaded", () => {
    const card = document.querySelector(".card-featured.reveal");
    if (!card) return;
    if (!window.MC || !MC.effectsOn || !MC.effectsOn()) return;

    const heading = card.querySelector("h1[data-scramble]");
    const eyebrow = card.querySelector(".eyebrow[data-unlock-label]");
    const finalLabel = eyebrow ? eyebrow.dataset.unlockLabel : "";
    if (eyebrow) eyebrow.textContent = "Unlocking";

    if (heading) {
      scramble(heading, () => {
        if (eyebrow) eyebrow.textContent = finalLabel;
        card.classList.add("is-unlocked");
      });
    } else if (eyebrow) {
      eyebrow.textContent = finalLabel;
    }
    cascade();
  });
})();
