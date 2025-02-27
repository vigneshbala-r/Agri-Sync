const products = [
    { id: 1, name: "Fresh Tomatoes", price: 50 },
    { id: 2, name: "Organic Carrots", price: 40 },
    { id: 3, name: "Potatoes", price: 30 }
];

const cart = [];

function displayProducts() {
    const productGrid = document.getElementById("productGrid");
    products.forEach(product => {
        const productCard = document.createElement("div");
        productCard.classList.add("product-card");
        productCard.innerHTML = `
            <h3>${product.name}</h3>
            <p>Price: ₹${product.price} per kg</p>
            <input type="number" id="qty-${product.id}" placeholder="Enter quantity (kg)" min="1">
            <button onclick="addToCart(${product.id})">Request & Add to Cart</button>
        `;
        productGrid.appendChild(productCard);
    });
}

function addToCart(productId) {
    const quantity = document.getElementById(`qty-${productId}`).value;
    if (quantity && quantity > 0) {
        const product = products.find(p => p.id === productId);
        cart.push({ ...product, quantity: parseInt(quantity) });
        updateCart();
    } else {
        alert("Please enter a valid quantity.");
    }
}

function updateCart() {
    const cartItems = document.getElementById("cartItems");
    cartItems.innerHTML = "";
    cart.forEach(item => {
        const cartItem = document.createElement("li");
        cartItem.textContent = `${item.name} - ${item.quantity} kg (₹${item.price * item.quantity})`;
        cartItems.appendChild(cartItem);
    });
}

function checkout() {
    alert("Your request has been sent to the farmer! Thank you for using AgriTech.");
    cart.length = 0;
    updateCart();
}

document.addEventListener("DOMContentLoaded", displayProducts);