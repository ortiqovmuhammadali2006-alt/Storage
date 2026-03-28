/* ==========================================
   SHOPVERSE - Main JavaScript
   Django API bilan ulashga tayyor
   ========================================== */

// ===== API CONFIG (Django backend bilan ulashga tayyor) =====
const API_BASE = 'http://localhost:8000/api'; // Django URL

const API = {
  categories: `${API_BASE}/categories/`,
  products: `${API_BASE}/products/`,
  product: (id) => `${API_BASE}/products/${id}/`,
  categoryProducts: (id) => `${API_BASE}/categories/${id}/products/`,
  orders: `${API_BASE}/orders/`,
};

// Demo ma'lumotlar o'chirildi. Endi mahsulot va kategoriyalar ro'yxati faqat Django HTML orqali uzatiladi.

/* ==========================================
   CART MANAGER (localStorage + Django ready)
   ========================================== */
const Cart = {
  getItems() {
    try {
      return JSON.parse(localStorage.getItem('shopverse_cart') || '[]');
    } catch {
      return [];
    }
  },

  saveItems(items) {
    localStorage.setItem('shopverse_cart', JSON.stringify(items));
    this.updateUI();
  },

  addItem(product, quantity = 1) {
    const items = this.getItems();
    const existing = items.find(i => i.id === product.id);

    if (existing) {
      existing.quantity += quantity;
    } else {
      items.push({
        id: product.id,
        name: product.name,
        price: parseFloat(product.price),
        image: product.image,
        category_name: product.category_name,
        quantity,
      });
    }

    this.saveItems(items);
    showToast(`🛒 "${product.name}" savatchaga qo'shildi!`, 'success');
  },

  removeItem(id) {
    const items = this.getItems().filter(i => i.id !== id);
    this.saveItems(items);
    showToast('Mahsulot o\'chirildi', 'info');
  },

  updateQty(id, quantity) {
    if (quantity < 1) return this.removeItem(id);
    const items = this.getItems();
    const item = items.find(i => i.id === id);
    if (item) {
      item.quantity = quantity;
      this.saveItems(items);
    }
  },

  getCount() {
    return this.getItems().reduce((sum, i) => sum + i.quantity, 0);
  },

  getTotal() {
    return this.getItems().reduce((sum, i) => sum + i.price * i.quantity, 0);
  },

  updateUI() {
    const count = this.getCount();
    document.querySelectorAll('.cart-count').forEach(el => {
      el.textContent = count;
      el.style.display = count > 0 ? 'flex' : 'none';
    });
  },

  // Django bilan ulashga tayyor
  async syncWithDjango(userId) {
    // TODO: Django ulanganida bu metodni faollashtiring
    // const response = await fetch(API.orders, {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
    //   body: JSON.stringify({ items: this.getItems(), user: userId })
    // });
    // return await response.json();
  }
};

/* DataService ma'lumotlari to'g'ridan-to'g'ri Django Template'lardan olinmoqda */

/* ==========================================
   UTILITY FUNCTIONS
   ========================================== */
function formatPrice(price) {
  return new Intl.NumberFormat('uz-UZ').format(price) + " so'm";
}

function getStars(rating) {
  const full = Math.floor(rating);
  const half = rating % 1 >= 0.5 ? 1 : 0;
  const empty = 5 - full - half;
  return '★'.repeat(full) + (half ? '½' : '') + '☆'.repeat(empty);
}

function showToast(message, type = 'success') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span class="toast-icon">${icons[type] || '✅'}</span>
    <span class="toast-msg">${message}</span>
  `;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'slideIn 0.4s ease reverse';
    setTimeout(() => toast.remove(), 400);
  }, 3000);
}

function getCategoryParam() {
  return new URLSearchParams(window.location.search).get('category');
}

function getProductParam() {
  return new URLSearchParams(window.location.search).get('id');
}

/* ==========================================
   COMPONENTS
   ========================================== */
/* Komponentalar HTML shablonda to'g'ridan to'g'ri renderlanmoqda */

function toggleWishlist(id, btn) {
  const isLiked = btn.textContent === '❤️';
  btn.textContent = isLiked ? '🤍' : '❤️';
  showToast(isLiked ? 'Sevimlilardan olib tashlandi' : 'Sevimlilarga qo\'shildi!', isLiked ? 'info' : 'success');
}

/* ==========================================
   NAVBAR
   ========================================== */
function initNavbar() {
  Cart.updateUI();

  // Hamburger
  const hamburger = document.querySelector('.hamburger');
  const nav = document.querySelector('.navbar-nav');
  if (hamburger && nav) {
    hamburger.addEventListener('click', () => {
      nav.classList.toggle('open');
    });
  }

  // Active link
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.navbar-nav a').forEach(a => {
    if (a.getAttribute('href') === currentPage) {
      a.classList.add('active');
    }
  });
}

/* Sahifalar backend tomonidan oldindan renderlanadi */

/* ==========================================
   CART PAGE
   ========================================== */
function initCartPage() {
  renderCart();
}

function renderCart() {
  const items = Cart.getItems();
  const cartItemsEl = document.getElementById('cartItems');
  const cartEmptyEl = document.getElementById('cartEmpty');
  const cartContentEl = document.getElementById('cartContent');

  if (!cartItemsEl) return;

  if (items.length === 0) {
    if (cartContentEl) cartContentEl.style.display = 'none';
    if (cartEmptyEl) cartEmptyEl.style.display = 'block';
    return;
  }

  if (cartContentEl) cartContentEl.style.display = 'grid';
  if (cartEmptyEl) cartEmptyEl.style.display = 'none';

  cartItemsEl.innerHTML = items.map(item => `
    <div class="cart-item" id="cart-item-${item.id}">
      <div class="cart-item-product">
        <img src="${item.image}" alt="${item.name}" class="cart-item-img"
             onerror="this.src='https://via.placeholder.com/70x70/0f3460/e94560?text=?'">
        <div>
          <div class="cart-item-name">${item.name}</div>
          <div class="cart-item-cat">${item.category_name}</div>
        </div>
      </div>
      <div class="cart-item-price">${formatPrice(item.price)}</div>
      <div class="cart-item-qty-cell">
        <div class="qty-control">
          <button class="qty-btn" onclick="changeCartQty(${item.id}, ${item.quantity - 1})">−</button>
          <input class="qty-input" type="number" value="${item.quantity}" readonly>
          <button class="qty-btn" onclick="changeCartQty(${item.id}, ${item.quantity + 1})">+</button>
        </div>
      </div>
      <div class="cart-item-total">${formatPrice(item.price * item.quantity)}</div>
      <button class="remove-btn" onclick="removeFromCart(${item.id})">✕</button>
    </div>
  `).join('');

  updateCartSummary();
}

function changeCartQty(id, newQty) {
  Cart.updateQty(id, newQty);
  renderCart();
}

function removeFromCart(id) {
  Cart.removeItem(id);
  renderCart();
}

function updateCartSummary() {
  const items = Cart.getItems();
  const subtotal = Cart.getTotal();
  const shipping = subtotal > 500000 ? 0 : 30000;
  const total = subtotal + shipping;

  const el = (id) => document.getElementById(id);
  if (el('summarySubtotal')) el('summarySubtotal').textContent = formatPrice(subtotal);
  if (el('summaryShipping')) el('summaryShipping').textContent = shipping === 0 ? "Bepul" : formatPrice(shipping);
  if (el('summaryTotal')) el('summaryTotal').textContent = formatPrice(total);
  if (el('summaryCount')) el('summaryCount').textContent = `${Cart.getCount()} ta mahsulot`;
}

/* ==========================================
   PROMO CODE
   ========================================== */
function applyPromo() {
  const code = document.getElementById('promoInput')?.value?.trim().toUpperCase();
  const validCodes = { 'FIRST10': 10, 'SAVE20': 20, 'VIP30': 30 };

  if (validCodes[code]) {
    showToast(`🎉 "${code}" promokod qo'llanildi! -${validCodes[code]}% chegirma`, 'success');
  } else {
    showToast('❌ Noto\'g\'ri promokod', 'error');
  }
}

/* ==========================================
   CHECKOUT (Django tayyor)
   ========================================== */
async function proceedToCheckout() {
  const items = Cart.getItems();
  if (items.length === 0) {
    showToast('Savatcha bo\'sh!', 'warning');
    return;
  }

  showToast('⏳ Buyurtma yaratilmoqda...', 'info');

  // TODO: Django ulanganda bu qismni faollashtiring
  // try {
  //   const response = await fetch(API.orders, {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json',
  //       'X-CSRFToken': getCookie('csrftoken')
  //     },
  //     body: JSON.stringify({
  //       items: items,
  //       total: Cart.getTotal()
  //     })
  //   });
  //   const order = await response.json();
  //   localStorage.removeItem('shopverse_cart');
  //   Cart.updateUI();
  //   window.location.href = `/orders/${order.id}/`;
  // } catch (err) {
  //   showToast('Xatolik yuz berdi. Qaytadan urining.', 'error');
  // }

  // Demo rejim
  setTimeout(() => {
    showToast('✅ Buyurtmangiz qabul qilindi! (Demo rejim)', 'success');
  }, 1500);
}

/* ==========================================
   PAGE INIT
   ========================================== */
document.addEventListener('DOMContentLoaded', () => {
  initNavbar();

  const page = window.location.pathname.split('/').pop() || 'index.html';

  if (page === 'cart.html') {
    initCartPage();
  }
});
