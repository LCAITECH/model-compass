// /plans form helpers. Optional: without this file the form still works
// (the server ignores an amount that was filled in for another plan).
//  1. picking another plan refills the amount with that plan's list price;
//  2. picking another model resubmits, since the plan list depends on it.
(function () {
  const form = document.getElementById("plans-form");
  if (!form) return;
  const model = form.querySelector("[data-plans-model]");
  const plan = form.querySelector("[data-plans-plan]");
  const amount = form.querySelector("[data-plans-amount]");
  const amountFor = form.querySelector("[data-plans-amount-for]");

  if (plan && amount && amountFor) {
    plan.addEventListener("change", () => {
      const option = plan.options[plan.selectedIndex];
      amount.value = option.dataset.price || "";
      amountFor.value = plan.value;
    });
  }

  if (model) {
    model.addEventListener("change", () => {
      if (plan) plan.disabled = true; // a plan of the previous model means nothing now
      if (amount) amount.disabled = true;
      if (amountFor) amountFor.disabled = true;
      if (model.value) form.submit();
    });
  }
})();
