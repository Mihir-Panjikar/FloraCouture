const basePrice = 500;
const priceDisplay = document.getElementById("customPrice");
const checkboxes = document.querySelectorAll("input[type='checkbox']");
const form = document.getElementById("customForm");

function updatePrice() {
  let total = basePrice;
  checkboxes.forEach(checkbox => {
    if (checkbox.checked) {
      total += parseInt(checkbox.getAttribute("data-price"));
    }
  });
  priceDisplay.innerText = total;
}

checkboxes.forEach(cb => cb.addEventListener("change", updatePrice));

form.addEventListener("submit", function (e) {
  e.preventDefault();

  const name = document.getElementById("bouquetName").value;
  const message = document.getElementById("message").value;

  const selectedItems = [];
  let price = basePrice;

  checkboxes.forEach(checkbox => {
    if (checkbox.checked) {
      selectedItems.push(checkbox.value);
      price += parseInt(checkbox.getAttribute("data-price"));
    }
  });

  const item = {
    name,
    price,
    details: {
      type: "Custom",
      items: selectedItems,
      message
    }
  };

  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  cart.push(item);
  localStorage.setItem("cart", JSON.stringify(cart));

  alert("Custom bouquet added to cart!");
  form.reset();
  updatePrice();
});
