function loadCart() {
    const cartItemsContainer = document.getElementById("cartItems");
    const totalPriceElem = document.getElementById("totalPrice");
  
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
  
    cartItemsContainer.innerHTML = "";
    let total = 0;
  
    if (cart.length === 0) {
      cartItemsContainer.innerHTML = "<p>Your cart is empty 🌼</p>";
      document.querySelector(".cart-summary").style.display = "none";
      return;
    }
  
    cart.forEach((item, index) => {
      total += item.price;
  
      const card = document.createElement("div");
      card.className = "cart-card";
      card.innerHTML = `
        <div>
          <h3>${item.name}</h3>
          <p>Type: ${item.details?.type || "Simple"}</p>
          <p>₹${item.price}</p>
        </div>
        <button onclick="removeItem(${index})">Remove</button>
      `;
      cartItemsContainer.appendChild(card);
    });
  
    totalPriceElem.innerText = total;
    document.querySelector(".cart-summary").style.display = "block";
  }
  
  function removeItem(index) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    cart.splice(index, 1);
    localStorage.setItem("cart", JSON.stringify(cart));
    loadCart();
  }
  
  function placeOrder() {
    localStorage.removeItem("cart");
    window.location.href = "thank-you.html";
  }
  
  window.onload = loadCart;
  