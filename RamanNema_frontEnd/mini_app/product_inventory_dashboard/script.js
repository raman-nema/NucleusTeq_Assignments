// default product list used when nothing is saved yet
var defaultProducts = [
  { id: 1, name: "Laptop", price: 55000, stock: 5, category: "electronics" },
  {
    id: 2,
    name: "Wireless Earbuds",
    price: 3499,
    stock: 0,
    category: "electronics",
  },
  {
    id: 3,
    name: "Smartwatch",
    price: 14999,
    stock: 8,
    category: "electronics",
  },
  { id: 4, name: "Linen Shirt", price: 999, stock: 30, category: "clothing" },
  { id: 5, name: "Denim Jacket", price: 2999, stock: 2, category: "clothing" },
  { id: 6, name: "Atomic Habits", price: 499, stock: 0, category: "books" },
  { id: 7, name: "JS: Good Parts", price: 699, stock: 12, category: "books" },
  {
    id: 8,
    name: "Leather Wallet",
    price: 899,
    stock: 3,
    category: "accessories",
  },
  {
    id: 9,
    name: "Running Shoes",
    price: 4299,
    stock: 0,
    category: "accessories",
  },
  { id: 10, name: "Desk Lamp", price: 1299, stock: 9, category: "accessories" },
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
  return new Promise(function (resolve) {
    setTimeout(function () {
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
  return new Promise(function (resolve) {
    setTimeout(function () {
      var saved = getSavedProducts();
      resolve(saved || defaultProducts);
    }, 1500);
  });
}

// updates the 3 numbers at the top of the page
function updateSummaryCards() {
  document.getElementById("totalProducts").textContent = productData.length;

  var totalVal = 0;
  for (var i = 0; i < productData.length; i++) {
    totalVal += productData[i].price * productData[i].stock;
  }
  document.getElementById("totalValue").textContent =
    "Rs. " + totalVal.toLocaleString("en-IN");

  var outOfStockCount = 0;
  for (var j = 0; j < productData.length; j++) {
    if (productData[j].stock === 0) outOfStockCount++;
  }
  document.getElementById("outOfStock").textContent = outOfStockCount;
}

// fills the category dropdown based on what categories exist
function updateCategoryDropdown() {
  var dropdown = document.getElementById("categoryDropdown");
  var selectedValue = dropdown.value;

  var alreadyAdded = {};
  var categoryList = [];
  for (var i = 0; i < productData.length; i++) {
    var cat = productData[i].category;
    if (!alreadyAdded[cat]) {
      alreadyAdded[cat] = true;
      categoryList.push(cat);
    }
  }
  categoryList.sort();

  while (dropdown.options.length > 1) dropdown.remove(1);

  for (var k = 0; k < categoryList.length; k++) {
    var option = document.createElement("option");
    option.value = categoryList[k];
    option.textContent =
      categoryList[k].charAt(0).toUpperCase() + categoryList[k].slice(1);
    dropdown.appendChild(option);
  }

  dropdown.value = selectedValue || "all";
}

// reads the filters and returns matching products
function getFilteredProducts() {
  var searchText     = document.getElementById("searchBox").value.toLowerCase().trim();
  var selectedCat    = document.getElementById("categoryDropdown").value;
  var selectedSort   = document.getElementById("sortDropdown").value;
  var showLowOnly    = document.getElementById("lowStockOnly").checked;

  var filtered = productData.slice();

  if (searchText) {
    filtered = filtered.filter(function(p) {
      return p.name.toLowerCase().indexOf(searchText) !== -1;
    });
  }

  if (selectedCat !== "all") {
    filtered = filtered.filter(function(p) {
      return p.category === selectedCat;
    });
  }

  if (showLowOnly) {
    filtered = filtered.filter(function(p) {
      return p.stock < 5;
    });
  }

  if (selectedSort === "low")  filtered.sort(function(a, b) { return a.price - b.price; });
  if (selectedSort === "high") filtered.sort(function(a, b) { return b.price - a.price; });
  if (selectedSort === "az")   filtered.sort(function(a, b) { return a.name.localeCompare(b.name); });
  if (selectedSort === "za")   filtered.sort(function(a, b) { return b.name.localeCompare(a.name); });

  return filtered;
}
