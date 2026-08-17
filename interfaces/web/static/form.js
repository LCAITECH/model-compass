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

  // Free-text detection: a deterministic keyword match against the
  // same 14 use-case categories (interfaces/web/use_case_matcher.py),
  // shown as a dismissible suggestion. Never applied automatically --
  // priorities only change if the developer clicks "Use these
  // priorities", same as picking a pill or the dropdown.
  const suggestionBox = document.getElementById("use-case-suggestion");
  let suggestionRequestId = 0;
  let suggestionDebounce;

  function renderSuggestion(data) {
    if (!suggestionBox) return;

    if (data.category) {
      const labels = data.priorities
        .map((value) => value.replace(/_/g, " "))
        .join(" and ");
      suggestionBox.innerHTML = "";
      suggestionBox.append(`Detected: ${data.category} → prioritize ${labels}. `);
      const acceptButton = document.createElement("button");
      acceptButton.type = "button";
      acceptButton.className = "use-case-suggestion-accept";
      acceptButton.textContent = "Use these priorities";
      acceptButton.addEventListener("click", () => {
        data.priorities.forEach((value, index) => {
          const select = document.getElementById(`priority_${index + 1}`);
          if (select) select.value = value;
        });
      });
      suggestionBox.append(acceptButton);
      suggestionBox.hidden = false;
    } else if (data.tied_categories.length > 1) {
      suggestionBox.textContent =
        `Detected multiple possible use cases (${data.tied_categories.join(", ")}) — choose your priorities manually.`;
      suggestionBox.hidden = false;
    } else {
      suggestionBox.hidden = true;
      suggestionBox.textContent = "";
    }
  }

  // 3 chars is the shortest real keyword in use_case_matcher.py
  // ("sql", "rag") -- anything shorter can never match, so skip the
  // round trip instead of firing a request that's guaranteed empty.
  const MIN_SUGGESTION_LENGTH = 3;

  if (useCaseField && suggestionBox) {
    useCaseField.addEventListener("input", () => {
      clearTimeout(suggestionDebounce);
      const text = useCaseField.value;
      if (text.trim().length < MIN_SUGGESTION_LENGTH) {
        suggestionBox.hidden = true;
        suggestionBox.textContent = "";
        return;
      }
      suggestionDebounce = setTimeout(() => {
        const requestId = ++suggestionRequestId;
        fetch(`/use-case-suggestion?text=${encodeURIComponent(text)}`)
          .then((response) => (response.ok ? response.json() : null))
          .then((data) => {
            if (data && requestId === suggestionRequestId) renderSuggestion(data);
          })
          .catch(() => {});
      }, 400);
    });
  }

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
