// Site-wide neural field: a fixed canvas behind every page. Nodes sit at
// different depths (bigger and faster when closer) and shift with the
// pointer; pulses of light travel along the links; a click sends a shock
// wave through the field. Decorative only (aria-hidden, no data in it).
// The landing page runs it at full intensity, other pages at a calmer one.
// With effects off it draws one still frame and stops.
(function () {
  const canvas = document.getElementById("field");
  if (!canvas || !canvas.getContext) return;
  const ctx = canvas.getContext("2d");
  const MC = (window.MC = window.MC || {});
  const intense = () => document.body.classList.contains("page-index");

  let W = 0;
  let H = 0;
  let nodes = [];
  let pulses = [];
  let waves = [];
  let running = false;
  let frame = 0;
  let lastSpawn = 0;
  let colors = { a: "#8b8cff", b: "#22d3ee", light: false };
  const pointer = { x: 0.5, y: 0.5, px: -9999, py: -9999 };

  function readColors() {
    const style = getComputedStyle(document.documentElement);
    colors = {
      a: style.getPropertyValue("--accent").trim() || colors.a,
      b: style.getPropertyValue("--accent-secondary").trim() || colors.b,
      light: document.documentElement.getAttribute("data-theme") === "light",
    };
  }

  function linkDistance() {
    return Math.min(190, Math.max(120, W / 9));
  }

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = window.innerWidth;
    H = window.innerHeight;
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const count = Math.max(24, Math.min(intense() ? 120 : 70, Math.round((W * H) / (intense() ? 9500 : 17000))));
    nodes = Array.from({ length: count }, () => {
      const z = 0.35 + Math.random() * 0.65;
      return {
        x: Math.random() * W,
        y: Math.random() * H,
        vx: (Math.random() - 0.5) * 0.35 * z,
        vy: (Math.random() - 0.5) * 0.35 * z,
        z,
      };
    });
    pulses = [];
  }

  function shown(n) {
    // Position on screen: base position plus pointer parallax (closer = more).
    return {
      x: n.x + (pointer.x - 0.5) * 60 * n.z,
      y: n.y + (pointer.y - 0.5) * 40 * n.z,
    };
  }

  function step(now) {
    for (const n of nodes) {
      n.x += n.vx;
      n.y += n.vy;
      if (n.x < -20) n.x = W + 20;
      if (n.x > W + 20) n.x = -20;
      if (n.y < -20) n.y = H + 20;
      if (n.y > H + 20) n.y = -20;
    }
    for (const w of waves) {
      w.r += 9;
      for (const n of nodes) {
        const dx = n.x - w.x;
        const dy = n.y - w.y;
        const d = Math.hypot(dx, dy);
        if (d > 1 && Math.abs(d - w.r) < 22) {
          n.vx += (dx / d) * 0.5 * n.z;
          n.vy += (dy / d) * 0.5 * n.z;
        }
      }
    }
    waves = waves.filter((w) => w.r < w.max);
    for (const n of nodes) {
      n.vx *= 0.985;
      n.vy *= 0.985;
      if (Math.abs(n.vx) + Math.abs(n.vy) < 0.06) {
        n.vx += (Math.random() - 0.5) * 0.03;
        n.vy += (Math.random() - 0.5) * 0.03;
      }
    }
    if (now - lastSpawn > (intense() ? 140 : 380) && pulses.length < (intense() ? 26 : 8)) {
      lastSpawn = now;
      const a = Math.floor(Math.random() * nodes.length);
      const pa = shown(nodes[a]);
      let best = -1;
      let bestD = linkDistance();
      for (let j = 0; j < nodes.length; j += 1) {
        if (j === a) continue;
        const pb = shown(nodes[j]);
        const d = Math.hypot(pa.x - pb.x, pa.y - pb.y);
        if (d < bestD && Math.random() < 0.35) {
          best = j;
          bestD = d;
        }
      }
      if (best >= 0) pulses.push({ a, b: best, t: 0, speed: 0.012 + Math.random() * 0.014 });
    }
    for (const p of pulses) p.t += p.speed;
    pulses = pulses.filter((p) => p.t < 1);
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    const strong = intense();
    const fade = strong ? Math.max(0.4, 1 - window.scrollY / (H * 1.3)) : 0.55;
    const dist = linkDistance();
    ctx.lineWidth = 1;
    const pts = nodes.map(shown);

    for (let i = 0; i < nodes.length; i += 1) {
      for (let j = i + 1; j < nodes.length; j += 1) {
        const d = Math.hypot(pts[i].x - pts[j].x, pts[i].y - pts[j].y);
        if (d < dist) {
          ctx.globalAlpha = (1 - d / dist) * 0.42 * fade * Math.min(nodes[i].z, nodes[j].z + 0.3);
          ctx.strokeStyle = colors.a;
          ctx.beginPath();
          ctx.moveTo(pts[i].x, pts[i].y);
          ctx.lineTo(pts[j].x, pts[j].y);
          ctx.stroke();
        }
      }
    }

    ctx.globalCompositeOperation = colors.light ? "source-over" : "lighter";
    for (const p of pulses) {
      const a = pts[p.a];
      const b = pts[p.b];
      const e = p.t * p.t * (3 - 2 * p.t); // ease in-out
      const x = a.x + (b.x - a.x) * e;
      const y = a.y + (b.y - a.y) * e;
      const t0 = Math.max(0, e - 0.16);
      ctx.globalAlpha = Math.sin(p.t * Math.PI) * 0.9 * fade;
      ctx.strokeStyle = colors.b;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(a.x + (b.x - a.x) * t0, a.y + (b.y - a.y) * t0);
      ctx.lineTo(x, y);
      ctx.stroke();
      ctx.fillStyle = colors.b;
      ctx.beginPath();
      ctx.arc(x, y, 2.6, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.lineWidth = 1;

    for (let i = 0; i < nodes.length; i += 1) {
      const n = nodes[i];
      const near = Math.hypot(pts[i].x - pointer.px, pts[i].y - pointer.py) < 160;
      const r = 1.1 + n.z * 2.4 + (near ? 1.6 : 0);
      ctx.globalAlpha = (0.35 + n.z * 0.55) * fade;
      ctx.fillStyle = near ? colors.b : colors.a;
      ctx.beginPath();
      ctx.arc(pts[i].x, pts[i].y, r, 0, Math.PI * 2);
      ctx.fill();
      if (strong && n.z > 0.85) {
        ctx.globalAlpha = 0.1 * fade;
        ctx.beginPath();
        ctx.arc(pts[i].x, pts[i].y, r * 4, 0, Math.PI * 2);
        ctx.fill();
      }
    }
    ctx.globalCompositeOperation = "source-over";

    for (const w of waves) {
      ctx.globalAlpha = (1 - w.r / w.max) * 0.5;
      ctx.strokeStyle = colors.b;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(w.x, w.y, w.r, 0, Math.PI * 2);
      ctx.stroke();
    }
    ctx.globalAlpha = 1;
  }

  function loop(now) {
    if (!running) return;
    if (frame % 90 === 0) readColors();
    frame += 1;
    step(now);
    draw();
    requestAnimationFrame(loop);
  }

  function start() {
    if (running || !MC.effectsOn || !MC.effectsOn() || document.hidden) return;
    running = true;
    requestAnimationFrame(loop);
  }

  function stop() {
    running = false;
  }

  function still() {
    readColors();
    draw();
  }

  readColors();
  resize();
  still();

  window.addEventListener("resize", () => { resize(); if (!running) still(); });
  window.addEventListener("pointermove", (e) => {
    pointer.x = e.clientX / W;
    pointer.y = e.clientY / H;
    pointer.px = e.clientX;
    pointer.py = e.clientY;
  }, { passive: true });
  window.addEventListener("pointerdown", (e) => {
    if (running) waves.push({ x: e.clientX, y: e.clientY, r: 0, max: 460 });
  }, { passive: true });
  window.addEventListener("scroll", () => { if (!running) still(); }, { passive: true });
  document.addEventListener("visibilitychange", () => (document.hidden ? stop() : start()));
  new MutationObserver(() => { readColors(); if (!running) still(); }).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"],
  });
  if (MC.onEffectsChange) MC.onEffectsChange((on) => (on ? start() : (stop(), still())));
  start();
})();
