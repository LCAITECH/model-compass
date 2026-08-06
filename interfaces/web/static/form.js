// Picking a common use case (from the dropdown or a quick-select pill)
// pre-fills the text field and the priority dropdowns as a starting
// point -- everything stays editable, and if JS is unavailable the
// form still works as plain HTML with the dropdown alone.
document.addEventListener("DOMContentLoaded", () => {
  const useCaseField = document.getElementById("use_case");
  const preset = document.getElementById("use_case_preset");

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
      if (language) language.value = "en";
      if (budget) budget.value = "low";
      document.querySelector("form.context-form")?.requestSubmit();
    });
  }
});
