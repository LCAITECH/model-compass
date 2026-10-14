// Turns the decision form's four stages into a step-by-step wizard. It is
// progressive enhancement: without JS every stage is visible and the form
// works as one long page. Field ids, names and the submit button are
// untouched, so form.js and the server see exactly the same form.
(function () {
  document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form.decision-form");
    if (!form) return;
    const stages = Array.from(form.querySelectorAll(":scope > .decision-stage"));
    const submit = form.querySelector('button[type="submit"]');
    if (stages.length < 2 || !submit) return;

    const names = stages.map((stage) => {
      const name = stage.querySelector(".stage-name");
      return name ? name.firstChild.textContent.trim() : "Step";
    });
    let current = 0;
    let furthest = 0;

    const progress = document.createElement("ol");
    progress.className = "wizard-progress";
    const steps = names.map((label, i) => {
      const item = document.createElement("li");
      const button = document.createElement("button");
      button.type = "button";
      button.innerHTML = `<span class="dot">${i + 1}</span><span class="label"></span>`;
      button.querySelector(".label").textContent = label;
      button.addEventListener("click", () => {
        if (i <= furthest && i !== current) go(i);
      });
      item.appendChild(button);
      progress.appendChild(item);
      return item;
    });
    const bar = document.createElement("div");
    bar.className = "wizard-bar";
    bar.innerHTML = "<span></span>";

    const nav = document.createElement("div");
    nav.className = "wizard-nav";
    const back = document.createElement("button");
    back.type = "button";
    back.className = "wizard-back";
    back.textContent = "Back";
    const next = document.createElement("button");
    next.type = "button";
    next.className = "wizard-next";
    nav.append(back, next);

    form.insertBefore(bar, form.firstChild);
    form.insertBefore(progress, form.firstChild);
    form.insertBefore(nav, submit);
    form.classList.add("wizard-on");

    function validCurrent() {
      const fields = Array.from(stages[current].querySelectorAll("input, select, textarea"));
      for (const field of fields) {
        if (field.disabled || field.checkValidity()) continue;
        field.reportValidity();
        return false;
      }
      return true;
    }

    function render() {
      stages.forEach((stage, i) => stage.classList.toggle("is-active", i === current));
      steps.forEach((item, i) => {
        item.classList.toggle("is-current", i === current);
        item.classList.toggle("is-done", i < current);
        item.querySelector("button").disabled = i > furthest;
      });
      bar.firstElementChild.style.width = `${(current / (stages.length - 1)) * 100}%`;
      back.hidden = current === 0;
      const last = current === stages.length - 1;
      next.hidden = last;
      next.textContent = current === stages.length - 2 ? "Add access details (optional)" : "Next";
      // The access stage is optional, so Submit is offered from the budget step on.
      submit.classList.toggle("is-ready", current >= stages.length - 2);
    }

    function go(index) {
      const forward = index > current;
      stages[index].dataset.dir = forward ? "fwd" : "back";
      current = index;
      furthest = Math.max(furthest, current);
      render();
      const field = stages[current].querySelector("input[type=text], select");
      if (field && window.matchMedia && window.matchMedia("(pointer: fine)").matches) field.focus({ preventScroll: true });
    }

    next.addEventListener("click", () => {
      if (current < stages.length - 1 && validCurrent()) go(current + 1);
    });
    back.addEventListener("click", () => {
      if (current > 0) go(current - 1);
    });
    // Enter inside a text field advances instead of submitting half a form.
    form.addEventListener("keydown", (event) => {
      if (event.key !== "Enter" || event.target.tagName !== "INPUT" || event.target.type === "submit") return;
      if (submit.classList.contains("is-ready")) return;
      event.preventDefault();
      next.click();
    });

    render();
  });
})();
