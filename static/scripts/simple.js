const bouquets = [
    {
      name: "Romantic Red Roses Bouquet",
      description: "12 fresh red roses wrapped in love.",
      price: 499,
      image: "assets/Red Rose bouquet.jpg"
    },
    {
      name: "Pink Rose Bouquet",
      description: "Fresh Pink roses wrapped in love.",
      price: 599,
      image: "assets/pink rose bouquet.jpg"
    },
    {
      name: "White Rose Bouquet",
      description: "Fresh White roses wrapped in love.",
      price: 699,
      image: "assets/White Rose Bouquet.jpg"
    },
    {
      name: "Tulip Bouquet",
      description: "Elegant tulip bouquet bursting with color and charm.",
      price: 799,
      image: "assets/Tulip Bouquet.jpg"
    },
    {
      name: "Black Rose Bouquet",
      description: "Fresh Black roses wrapped in love.",
      price: 899,
      image: "assets/Black Rose Bouquet.jpeg"
    },
    {
      name: "Lavender Bouquet",
      description: "Fresh Lavenders wrapped in love.",
      price: 699,
      image: "assets/Lavender Bouquet.jpg"
    },
    {
      name: "Lily Bouquet",
      description: "Graceful lily bouquet radiating purity , elegance, and fragrance.",
      price: 799,
      image: "assets/Lily Bouquet.jpg"
    },
    {
    name: "Mixed Bouquet",
    description: "A bouquet with elegent flowers",
    price: 599,
    image: "assets/Mixed Bouquet.jpg"
    },
    {
      name: "Sunflower Bouquet",
      description: "Vibrant sunflower bouquet shining with warmth and happiness.",
      price: 899,
      image: "assets/Sunflower Bouquet.jpg"
    },
    {
        name: "White Daisy Bouquet",
        description: "Vibrant White Daisy bouquet shining with purity and elegance.",
        price: 799,
        image: "assets/White Daisy Bouquet.jpg"
    },
   
    {
      name: "Box Bouquet",
      description: "",
      price: 999,
      image: "assets/Box Bouquet.jpg"
    },
    {
      name: "Chocolate Bouquet",
      description: "",
      price: 899,
      image: "assets/Chocolate Bouquet.jpg"
    },
    {
      name: "Ferrero rocher Bouquet",
      description: "",
      price: 999,
      image: "assets/Ferrero rocher Bouquet.webp"
    },
    {
      name: "Heart shaped Bouquet",
      description: "",
      price: 1299,
      image: "assets/Heart shaped Bouquet.jpg"
    },
    {
      name: "Hot wheels Bouquet",
      description: "",
      price: 1399,
      image: "assets/Hot wheels Bouquet.jpg"
    },
    {
      name: "Money Bouquet",
      description: "",
      price: 899,
      image: "assets/Money Bouquet.jpg"
    },
    {
      name: "Personlized Bouquet",
      description: "",
      price: 1299,
      image: "assets/Personalized Bouquet.jpg"
    },
    {
      name: "Ribbon Bouquet",
      description: "",
      price: 899,
      image: "assets/Ribbion bouquet.jpg"
    },
    {
      name: "Toy Bouquet",
      description: "",
      price: 999,
      image: "assets/Toy bouquet.jpg"
    },
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
  