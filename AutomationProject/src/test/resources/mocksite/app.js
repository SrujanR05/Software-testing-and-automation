// Mock Site Application Logic

// Mock Product Database
const PRODUCTS = [
    { id: 1, title: "Quantum Laptop", category: "Electronics", price: 1200, icon: "💻" },
    { id: 2, title: "Noise Cancelling Headphones", category: "Electronics", price: 250, icon: "🎧" },
    { id: 3, title: "Wireless Charger", category: "Electronics", price: 45, icon: "⚡" },
    { id: 4, title: "Waterproof Smartwatch", category: "Electronics", price: 180, icon: "⌚" },
    { id: 5, title: "Premium Leather Jacket", category: "Clothing", price: 150, icon: "🧥" },
    { id: 6, title: "Designer Denim Jeans", category: "Clothing", price: 80, icon: "👖" },
    { id: 7, title: "Organic Cotton T-Shirt", category: "Clothing", price: 25, icon: "👕" },
    { id: 8, title: "The Art of Automation Book", category: "Books", price: 40, icon: "📘" },
    { id: 9, title: "Mastering Selenium 4", category: "Books", price: 55, icon: "📖" },
    { id: 10, title: "Java Testing Cookbook", category: "Books", price: 35, icon: "📚" }
];

// Shopping Cart State
let cart = JSON.parse(sessionStorage.getItem("cart")) || [];

// Contact Form Handler
function handleContactSubmit(event) {
    event.preventDefault();
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const subject = document.getElementById("subject").value.trim();
    const message = document.getElementById("message").value.trim();
    const successMsg = document.getElementById("success-msg");

    if (name && email && subject && message) {
        successMsg.style.display = "block";
        successMsg.innerText = "Thank you! Your message has been submitted successfully.";
        document.getElementById("contact-form").reset();
    }
}

// Login Handler
function handleLoginSubmit(event) {
    event.preventDefault();
    const email = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const errorMsg = document.getElementById("error-msg");

    // Clear previous messages
    errorMsg.style.display = "none";

    if (email === "admin@example.com" && password === "Password123") {
        sessionStorage.setItem("userLoggedIn", "true");
        window.location.href = "dashboard.html";
    } else {
        errorMsg.style.display = "block";
        errorMsg.innerText = "Invalid username or password.";
    }
}

// Email Validator Regex
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Registration Handler
function handleRegistrationSubmit(event) {
    event.preventDefault();
    const firstName = document.getElementById("first-name").value.trim();
    const lastName = document.getElementById("last-name").value.trim();
    const email = document.getElementById("reg-email").value.trim();
    const password = document.getElementById("reg-password").value;
    const confirmPassword = document.getElementById("confirm-password").value;
    const emailError = document.getElementById("email-error-msg");
    const passError = document.getElementById("pass-error-msg");

    // Reset validations
    emailError.style.display = "none";
    passError.style.display = "none";

    let isValid = true;

    if (!isValidEmail(email)) {
        emailError.style.display = "block";
        emailError.innerText = "Invalid email format";
        isValid = false;
    }

    if (password !== confirmPassword) {
        passError.style.display = "block";
        passError.innerText = "Passwords do not match";
        isValid = false;
    }

    if (isValid) {
        sessionStorage.setItem("registeredUser", JSON.stringify({ firstName, lastName, email }));
        window.location.href = "dashboard.html";
    }
}

// Registration Live Email Validator (for interactive testing)
function validateLiveEmail() {
    const emailInput = document.getElementById("reg-email");
    const emailError = document.getElementById("email-error-msg");
    if (!emailInput || !emailError) return;

    const email = emailInput.value.trim();
    if (email === "") {
        emailError.style.display = "none";
        return;
    }

    if (!isValidEmail(email)) {
        emailError.style.display = "block";
        emailError.innerText = "Invalid email format";
    } else {
        emailError.style.display = "none";
    }
}

// Products Filter and Render Handler
function renderProducts() {
    const grid = document.getElementById("products-grid");
    if (!grid) return;

    // Get filter states
    const checkedCategories = Array.from(document.querySelectorAll(".category-filter:checked")).map(cb => cb.value);
    const minPriceInput = document.getElementById("min-price");
    const maxPriceInput = document.getElementById("max-price");
    const minPrice = parseFloat(minPriceInput ? minPriceInput.value : 0) || 0;
    const maxPrice = parseFloat(maxPriceInput ? maxPriceInput.value : 9999) || 9999;

    // Filter products
    const filtered = PRODUCTS.filter(prod => {
        const matchesCategory = checkedCategories.length === 0 || checkedCategories.includes(prod.category);
        const matchesPrice = prod.price >= minPrice && prod.price <= maxPrice;
        return matchesCategory && matchesPrice;
    });

    // Populate grid
    grid.innerHTML = filtered.map(prod => `
        <div class="product-card" data-category="${prod.category}" data-price="${prod.price}">
            <div class="product-img">${prod.icon}</div>
            <div class="product-info">
                <span class="product-category">${prod.category}</span>
                <h3 class="product-title">${prod.title}</h3>
                <div class="product-price-row">
                    <span class="product-price">$${prod.price}</span>
                    <button class="add-to-cart-btn" onclick="addToCart(${prod.id})">Add to Cart</button>
                </div>
            </div>
        </div>
    `).join("");
}

// Shopping Cart Actions
function addToCart(productId) {
    const product = PRODUCTS.find(p => p.id === productId);
    if (!product) return;

    const existing = cart.find(item => item.product.id === productId);
    if (existing) {
        existing.quantity++;
    } else {
        cart.push({ product, quantity: 1 });
    }

    saveCart();
    updateCartUI();
    
    // Redirect to cart page or just update UI
    const toast = document.createElement("div");
    toast.style.position = "fixed";
    toast.style.bottom = "20px";
    toast.style.right = "20px";
    toast.style.background = "#10b981";
    toast.style.color = "white";
    toast.style.padding = "10px 20px";
    toast.style.borderRadius = "5px";
    toast.style.zIndex = "1000";
    toast.innerText = `${product.title} added to cart!`;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
}

function increaseQty(productId) {
    const item = cart.find(i => i.product.id === productId);
    if (item) {
        item.quantity++;
        saveCart();
        updateCartUI();
    }
}

function decreaseQty(productId) {
    const item = cart.find(i => i.product.id === productId);
    if (item) {
        item.quantity--;
        if (item.quantity <= 0) {
            removeFromCart(productId);
        } else {
            saveCart();
            updateCartUI();
        }
    }
}

function removeFromCart(productId) {
    cart = cart.filter(i => i.product.id !== productId);
    saveCart();
    updateCartUI();
}

function saveCart() {
    sessionStorage.setItem("cart", JSON.stringify(cart));
}

function updateCartUI() {
    const cartList = document.getElementById("cart-items-list");
    if (!cartList) return;

    if (cart.length === 0) {
        cartList.innerHTML = `<p style="text-align: center; color: var(--text-muted);">Your cart is empty.</p>`;
        document.getElementById("cart-subtotal").innerText = "$0.00";
        document.getElementById("cart-grandtotal").innerText = "$0.00";
        return;
    }

    cartList.innerHTML = cart.map(item => `
        <div class="cart-item" data-id="${item.product.id}">
            <div class="cart-item-img">${item.product.icon}</div>
            <div>
                <div class="cart-item-title">${item.product.title}</div>
                <div class="cart-item-price">$${item.product.price}</div>
            </div>
            <div class="cart-qty-control">
                <button class="qty-btn qty-dec-btn" onclick="decreaseQty(${item.product.id})">-</button>
                <span class="item-qty">${item.quantity}</span>
                <button class="qty-btn qty-inc-btn" onclick="increaseQty(${item.product.id})">+</button>
            </div>
            <div style="font-weight: 700;">$${(item.product.price * item.quantity).toFixed(2)}</div>
            <button class="remove-item-btn" onclick="removeFromCart(${item.product.id})">Remove</button>
        </div>
    `).join("");

    // Calculate Subtotal
    const subtotal = cart.reduce((sum, item) => sum + (item.product.price * item.quantity), 0);
    const tax = subtotal * 0.1; // 10% tax
    const total = subtotal + tax;

    document.getElementById("cart-subtotal").innerText = `$${subtotal.toFixed(2)}`;
    document.getElementById("cart-tax").innerText = `$${tax.toFixed(2)}`;
    document.getElementById("cart-grandtotal").innerText = `$${total.toFixed(2)}`;
}

// Upload & Download Handler
function handleFileUpload(event) {
    event.preventDefault();
    const fileInput = document.getElementById("file-upload-input");
    const statusMsg = document.getElementById("upload-status-msg");

    statusMsg.style.display = "none";
    statusMsg.className = "alert";

    if (!fileInput.files.length) {
        statusMsg.style.display = "block";
        statusMsg.className += " alert-danger";
        statusMsg.innerText = "Please select a file to upload.";
        return;
    }

    const file = fileInput.files[0];
    const extension = file.name.split('.').pop().toLowerCase();

    if (extension === "txt" || extension === "pdf") {
        statusMsg.style.display = "block";
        statusMsg.className += " alert-success";
        statusMsg.innerText = `File uploaded successfully: ${file.name}`;
    } else {
        statusMsg.style.display = "block";
        statusMsg.className += " alert-danger";
        statusMsg.innerText = "Error: Unsupported file type. Only .txt and .pdf files are allowed.";
    }
}

// Initialize components when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
    // Determine active navbar link
    const path = window.location.pathname.split("/").pop() || "index.html";
    document.querySelectorAll(".nav-link").forEach(link => {
        if (link.getAttribute("href") === path) {
            link.classList.add("active");
        }
    });

    // Check specific pages and register handlers
    const contactForm = document.getElementById("contact-form");
    if (contactForm) {
        contactForm.addEventListener("submit", handleContactSubmit);
    }

    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", handleLoginSubmit);
    }

    const regForm = document.getElementById("reg-form");
    if (regForm) {
        regForm.addEventListener("submit", handleRegistrationSubmit);
        const emailInput = document.getElementById("reg-email");
        if (emailInput) {
            emailInput.addEventListener("input", validateLiveEmail);
        }
    }

    const productsGrid = document.getElementById("products-grid");
    if (productsGrid) {
        renderProducts();
        // Bind filter button if exists
        const filterBtn = document.getElementById("filter-btn");
        if (filterBtn) {
            filterBtn.addEventListener("click", renderProducts);
        }
        // Bind category checks
        document.querySelectorAll(".category-filter").forEach(cb => {
            cb.addEventListener("change", renderProducts);
        });
        // Bind price changes
        const minPriceInput = document.getElementById("min-price");
        const maxPriceInput = document.getElementById("max-price");
        if (minPriceInput) minPriceInput.addEventListener("input", renderProducts);
        if (maxPriceInput) maxPriceInput.addEventListener("input", renderProducts);
    }

    const cartList = document.getElementById("cart-items-list");
    if (cartList) {
        updateCartUI();
    }

    const uploadForm = document.getElementById("upload-form");
    if (uploadForm) {
        uploadForm.addEventListener("submit", handleFileUpload);
    }

    // Set up download mock link dynamically
    const downloadLink = document.getElementById("file-download-link");
    if (downloadLink) {
        const fileContent = "Mock file content generated for Selenium automation download verification.";
        const blob = new Blob([fileContent], { type: "text/plain" });
        const url = URL.createObjectURL(blob);
        downloadLink.href = url;
        downloadLink.setAttribute("download", "testdownload.txt");
    }

    // Handle dashboard messages
    const welcomeMsg = document.getElementById("welcome-msg");
    if (welcomeMsg) {
        const user = JSON.parse(sessionStorage.getItem("registeredUser"));
        if (user) {
            welcomeMsg.innerText = `Welcome to your dashboard, ${user.firstName} ${user.lastName}!`;
        } else {
            welcomeMsg.innerText = `Welcome to your dashboard!`;
        }
    }
});
