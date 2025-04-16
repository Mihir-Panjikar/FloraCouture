const bouquets = [
    {
      name: "Romantic Red Roses",
      description: "12 fresh red roses wrapped in love.",
      price: 499,
      image: "assets/rose.jpg"
    },
    {
      name: "Sunny Sunflowers",
      description: "Bright sunflowers to light up someone’s day.",
      price: 599,
      image: "assets/sunflower.jpg"
    },
    {
      name: "Mixed Bloom Beauty",
      description: "Colorful mix of roses, lilies, and orchids.",
      price: 699,
      image: "assets/mixed.jpg"
    },
    {
      name: "Elegant White Lilies",
      description: "Sleek white lilies tied with lavender ribbon.",
      price: 799,
      image: "assets/lilies.jpg"
    },
    {
      name: "Teddy & Roses Combo",
      description: "Roses with a cute teddy for extra love.",
      price: 899,
      image: "assets/teddy.jpg"
    },
    {
      name: "Chocolate Delight",
      description: "Bouquet paired with Ferrero Rocher chocolates.",
      price: 999,
      image: "assets/choco.jpg"
    }
  ];
  
  const bouquetGrid = document.getElementById("bouquetGrid");
  
  bouquets.forEach((item, index) => {
    const card = document.createElement("div");
    card.className = "bouquet-card";
    card.innerHTML = `
      <img src="${item.image}" alt="${item.name}" />
      <h3>${item.name}</h3>
      <p>${item.description}</p>
      <p><strong>₹${item.price}</strong></p>
      <button onclick="addToCart(${index})">Add to Cart</button>
    `;
    bouquetGrid.appendChild(card);
  });
  
  function addToCart(index) {
    const item = bouquets[index];
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    cart.push({
      name: item.name,
      details: { type: "Simple Bouquet" },
      price: item.price
    });
    localStorage.setItem("cart", JSON.stringify(cart));
    alert(`${item.name} added to cart!`);
  }
  