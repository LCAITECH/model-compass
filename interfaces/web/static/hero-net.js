// Landing hero background: a drifting network of nodes that reacts to the
// pointer (nearby nodes are drawn toward it and wired to it). Decorative
// only (aria-hidden, pointer-events none). With prefers-reduced-motion it
// draws one still frame; it pauses when the tab is hidden or the hero is
// scrolled out of view. Colours come from the theme's CSS variables.
(function () {
  document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("hero-net");
    if (!canvas || !canvas.getContext) return;
    const ctx = canvas.getContext("2d");
    const reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const LINK_DIST = 120;
    const POINTER_DIST = 170;
    let width = 0;
    let height = 0;
    let nodes = [];
    let pointer = null;
    let running = false;
    let visible = true;
    let colors = { a: "#4f46e5", b: "#06b6d4" };

    function readColors() {
      const style = getComputedStyle(document.documentElement);
      colors = {
        a: style.getPropertyValue("--accent").trim() || colors.a,
        b: style.getPropertyValue("--accent-secondary").trim() || colors.b,
      };
    }

    function resize() {
      const rect = canvas.getBoundingClientRect();
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      width = rect.width;
      height = rect.height;
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const count = Math.max(14, Math.min(70, Math.round((width * height) / 9000)));
      nodes = Array.from({ length: count }, () => ({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.25,
        vy: (Math.random() - 0.5) * 0.25,
        r: 1.4 + Math.random() * 1.6,
      }));
    }

    function step() {
      for (const n of nodes) {
        if (pointer) {
          const dx = pointer.x - n.x;
          const dy = pointer.y - n.y;
          const d = Math.hypot(dx, dy);
          if (d < POINTER_DIST && d > 1) {
            n.vx += (dx / d) * 0.012;
            n.vy += (dy / d) * 0.012;
          }
        }
        n.vx *= 0.985;
        n.vy *= 0.985;
        // A minimum drift keeps the field alive even when nothing is near.
        if (Math.abs(n.vx) + Math.abs(n.vy) < 0.05) {
          n.vx += (Math.random() - 0.5) * 0.02;
          n.vy += (Math.random() - 0.5) * 0.02;
        }
        n.x += n.vx;
        n.y += n.vy;
        if (n.x < 0 || n.x > width) n.vx *= -1;
        if (n.y < 0 || n.y > height) n.vy *= -1;
      }
    }

    function draw() {
      ctx.clearRect(0, 0, width, height);
      ctx.lineWidth = 1;
      for (let i = 0; i < nodes.length; i += 1) {
        const a = nodes[i];
        for (let j = i + 1; j < nodes.length; j += 1) {
          const b = nodes[j];
          const d = Math.hypot(a.x - b.x, a.y - b.y);
          if (d < LINK_DIST) {
            ctx.globalAlpha = (1 - d / LINK_DIST) * 0.45;
            ctx.strokeStyle = colors.a;
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
            ctx.stroke();
          }
        }
        if (pointer) {
          const d = Math.hypot(a.x - pointer.x, a.y - pointer.y);
          if (d < POINTER_DIST) {
            ctx.globalAlpha = (1 - d / POINTER_DIST) * 0.75;
            ctx.strokeStyle = colors.b;
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(pointer.x, pointer.y);
            ctx.stroke();
          }
        }
      }
      ctx.globalAlpha = 0.75;
      for (const n of nodes) {
        ctx.fillStyle = colors.a;
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.globalAlpha = 1;
    }

    let frame = 0;
    function loop() {
      if (!running) return;
      if (frame % 60 === 0) readColors(); // picks up a theme switch within a second
      frame += 1;
      step();
      draw();
      requestAnimationFrame(loop);
    }

    function start() {
      if (running || reduceMotion || !visible || document.hidden) return;
      running = true;
      requestAnimationFrame(loop);
    }

    function stop() {
      running = false;
    }

    readColors();
    resize();
    draw();
    if (reduceMotion) return;

    window.addEventListener("resize", () => { resize(); draw(); });
    window.addEventListener("pointermove", (event) => {
      const rect = canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      pointer = x >= 0 && y >= 0 && x <= rect.width && y <= rect.height ? { x, y } : null;
    }, { passive: true });
    document.addEventListener("visibilitychange", () => (document.hidden ? stop() : start()));
    if ("IntersectionObserver" in window) {
      new IntersectionObserver((entries) => {
        visible = entries[0].isIntersecting;
        if (visible) start(); else stop();
      }).observe(canvas);
    }
    start();
  });
})();
