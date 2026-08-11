// Picking a common use case (from the dropdown or a quick-select pill)
// pre-fills the text field and the priority dropdowns as a starting
// point -- everything stays editable, and if JS is unavailable the
// form still works as plain HTML with the dropdown alone.
document.addEventListener("DOMContentLoaded", () => {
  const useCaseField = document.getElementById("use_case");
  const preset = document.getElementById("use_case_preset");

  // The tier <select> stays `required` in the markup (so it degrades
  // correctly without JS, and so Fixed-tier mode keeps the native
  // validation bubble). CSS hides it in Custom mode, but a
  // display:none descendant is NOT reliably excluded from constraint
  // validation in every browser -- confirmed live: `required` still
  // blocked submission in Custom mode with no visible error, since
  // the browser can't show a validation bubble on a hidden field.
  // Toggling `required` in JS, in sync with the mode radios, is the
  // fix -- Custom mode never needs a tier value at all.
  const budgetModeTierRadio = document.getElementById("budget_mode_tier");
  const budgetModeCustomRadio = document.getElementById("budget_mode_custom");
  const budgetSelect = document.getElementById("budget");

  function syncBudgetRequired() {
    if (!budgetSelect || !budgetModeCustomRadio) return;
    budgetSelect.required = !budgetModeCustomRadio.checked;
  }

  if (budgetModeTierRadio && budgetModeCustomRadio && budgetSelect) {
    budgetModeTierRadio.addEventListener("change", syncBudgetRequired);
    budgetModeCustomRadio.addEventListener("change", syncBudgetRequired);
    syncBudgetRequired(); // covers a bfcache/back-navigation restore with Custom already checked
  }

  function applyUseCase(label, prioritiesCsv) {
    if (useCaseField) useCaseField.value = label;
    const priorities = (prioritiesCsv || "").split(",").filter(Boolean);
    priorities.forEach((value, index) => {
      const select = document.getElementById(`priority_${index + 1}`);
      if (select) select.value = value;
    });
  }

  if (preset) {
    preset.addEventListener("change", () => {
      const option = preset.options[preset.selectedIndex];
      if (!option.value) return;
      applyUseCase(option.value, option.dataset.priorities);
    });
  }

  document.querySelectorAll(".use-case-pill").forEach((pill) => {
    pill.addEventListener("click", () => {
      applyUseCase(pill.dataset.label, pill.dataset.priorities);
    });
  });

  const demoButton = document.getElementById("demo-button");
  if (demoButton) {
    demoButton.addEventListener("click", () => {
      applyUseCase("Telegram / WhatsApp bot", "cost,instruction_following");
      const language = document.getElementById("language");
      const budget = document.getElementById("budget");
      const budgetModeTier = document.getElementById("budget_mode_tier");
      if (language) language.value = "en";
      // Force Fixed tier mode -- if the visitor had already switched to
      // Custom before clicking the demo, the (hidden) tier <select>
      // below wouldn't take effect otherwise.
      if (budgetModeTier) budgetModeTier.checked = true;
      if (budget) budget.value = "low";
      document.querySelector("form.context-form")?.requestSubmit();
    });
  }
});
