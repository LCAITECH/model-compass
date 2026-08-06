// Picking a common use case pre-fills the text field and the priority
// dropdowns as a starting point -- everything stays editable, and if
// JS is unavailable the form still works as plain HTML.
document.addEventListener("DOMContentLoaded", () => {
  const preset = document.getElementById("use_case_preset");
  if (!preset) return;

  preset.addEventListener("change", () => {
    const option = preset.options[preset.selectedIndex];
    if (!option.value) return;

    document.getElementById("use_case").value = option.value;

    const priorities = (option.dataset.priorities || "").split(",").filter(Boolean);
    priorities.forEach((value, index) => {
      const select = document.getElementById(`priority_${index + 1}`);
      if (select) select.value = value;
    });
  });
});
