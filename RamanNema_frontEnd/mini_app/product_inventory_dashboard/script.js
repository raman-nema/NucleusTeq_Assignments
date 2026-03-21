// default product list used when nothing is saved yet
var defaultProducts = [
  { id: 1,  name: "Laptop",           price: 55000, stock: 5,  category: "electronics" },
  { id: 2,  name: "Wireless Earbuds", price: 3499,  stock: 0,  category: "electronics" },
  { id: 3,  name: "Smartwatch",       price: 14999, stock: 8,  category: "electronics" },
  { id: 4,  name: "Linen Shirt",      price: 999,   stock: 30, category: "clothing"    },
  { id: 5,  name: "Denim Jacket",     price: 2999,  stock: 2,  category: "clothing"    },
  { id: 6,  name: "Atomic Habits",    price: 499,   stock: 0,  category: "books"       },
  { id: 7,  name: "JS: Good Parts",   price: 699,   stock: 12, category: "books"       },
  { id: 8,  name: "Leather Wallet",   price: 899,   stock: 3,  category: "accessories" },
  { id: 9,  name: "Running Shoes",    price: 4299,  stock: 0,  category: "accessories" },
  { id: 10, name: "Desk Lamp",        price: 1299,  stock: 9,  category: "accessories" }
];


var productData = [];
var currentPage = 1;
var itemsPerPage = 6;

// save current product list to localStorage
function saveProducts() {
  localStorage.setItem("inventoryData", JSON.stringify(productData));
}

// load saved products from localStorage
function getSavedProducts() {
  var saved = localStorage.getItem("inventoryData");
  return saved ? JSON.parse(saved) : null;
}

// simulates loading data from a server (uses Promise + setTimeout)
function loadProductsFromServer() {
  return new Promise(function(resolve) {
    setTimeout(function() {
      var saved = getSavedProducts();
      resolve(saved || defaultProducts);
    }, 1500);
  });
}


// save current product list to localStorage
function saveProducts() {
  localStorage.setItem("inventoryData", JSON.stringify(productData));
}

// load saved products from localStorage
function getSavedProducts() {
  var saved = localStorage.getItem("inventoryData");
  return saved ? JSON.parse(saved) : null;
}

// simulates loading data from a server (uses Promise + setTimeout)
function loadProductsFromServer() {
  return new Promise(function(resolve) {
    setTimeout(function() {
      var saved = getSavedProducts();
      resolve(saved || defaultProducts);
    }, 1500);
  });
}