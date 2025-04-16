function loadCart() {
  // Get cart data from the API
  fetch('/api/cart/', {
    method: 'GET',
    headers: {
      'Authorization': `Token ${localStorage.getItem('authToken')}`,
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(data => {
    const cartItemsContainer = document.querySelector('.cart-items');
    let totalPrice = 0;
    
    // Clear existing items
    cartItemsContainer.innerHTML = '';
    
    // Add each item to the cart
    data.items.forEach((item, index) => {
      const cartItem = document.createElement('div');
      cartItem.classList.add('cart-item');
      
      cartItem.innerHTML = `
        <img src="${item.image}" alt="${item.name}">
        <div class="item-details">
          <h3>${item.name}</h3>
          <p>₹${item.price}</p>
        </div>
        <button onclick="removeItem(${index})">Remove</button>
      `;
      
      cartItemsContainer.appendChild(cartItem);
      totalPrice += item.price;
    });
    
    // Update total price
    document.querySelector('.total-price').textContent = `₹${totalPrice}`;
    document.querySelector(".cart-summary").style.display = "block";
  })
  .catch(error => {
    console.error('Error loading cart:', error);
  });
}

function removeItem(index) {
  fetch(`/api/cart/${index}/`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Token ${localStorage.getItem('authToken')}`,
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    }
  })
  .then(response => {
    if (response.ok) {
      loadCart(); // Reload the cart
    } else {
      throw new Error('Failed to remove item');
    }
  })
  .catch(error => {
    console.error('Error removing item:', error);
  });
}

function placeOrder() {
  fetch('/api/orders/', {
    method: 'POST',
    headers: {
      'Authorization': `Token ${localStorage.getItem('authToken')}`,
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    }
  })
  .then(response => {
    if (response.ok) {
      window.location.href = '/thank-you/';
    } else {
      throw new Error('Failed to place order');
    }
  })
  .catch(error => {
    console.error('Error placing order:', error);
    alert('Failed to place order. Please try again.');
  });
}

// Function to get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

window.onload = loadCart;
