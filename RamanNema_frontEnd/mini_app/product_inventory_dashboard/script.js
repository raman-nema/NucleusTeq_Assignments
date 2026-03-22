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

// updates the 3 numbers at the top of the page
function updateSummaryCards() {
  document.getElementById("totalProducts").textContent = productData.length;

  var totalVal = 0;
  for (var i = 0; i < productData.length; i++) {
    totalVal += productData[i].price * productData[i].stock;
  }
  document.getElementById("totalValue").textContent = "Rs. " + totalVal.toLocaleString("en-IN");

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
    option.textContent = categoryList[k].charAt(0).toUpperCase() + categoryList[k].slice(1);
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


// renders the product cards on the page
function renderProducts() {
  var filtered       = getFilteredProducts();
  var productList    = document.getElementById("productList");
  var noResultMsg    = document.getElementById("noProductsMsg");

  productList.innerHTML = "";

  if (filtered.length === 0) {
    noResultMsg.style.display = "block";
    document.getElementById("paginationBar").innerHTML = "";
    return;
  }
  noResultMsg.style.display = "none";

  var startIndex = (currentPage - 1) * itemsPerPage;
  var pageItems  = filtered.slice(startIndex, startIndex + itemsPerPage);

  for (var i = 0; i < pageItems.length; i++) {
    var product = pageItems[i];

    var statusClass, statusText;
    if (product.stock === 0) {
      statusClass = "noStock";
      statusText  = "Out of stock";
    } else if (product.stock < 5) {
      statusClass = "lowStock";
      statusText  = "Only " + product.stock + " left";
    } else {
      statusClass = "inStock";
      statusText  = "In stock: " + product.stock;
    }

    var card = document.createElement("div");
    card.className = "productCard";
    card.style.animationDelay = (i * 0.05) + "s";
    card.innerHTML =
      '<span class="categoryTag">' + product.category + '</span>' +
      '<p class="productName">' + product.name + '</p>' +
      '<p class="productPrice">Rs. ' + product.price.toLocaleString("en-IN") + '</p>' +
      '<p class="stockStatus ' + statusClass + '">' + statusText + '</p>' +
      '<button class="deleteBtn" data-id="' + product.id + '">Delete</button>';

    productList.appendChild(card);
  }

  renderPagination(filtered.length);
}

// renders the pagination buttons below the grid
function renderPagination(totalItems) {
  var paginationBar = document.getElementById("paginationBar");
  paginationBar.innerHTML = "";

  var totalPages = Math.ceil(totalItems / itemsPerPage);
  if (totalPages <= 1) return;

  var prevBtn = document.createElement("button");
  prevBtn.textContent = "Prev";
  prevBtn.disabled = (currentPage === 1);
  prevBtn.addEventListener("click", function() { currentPage--; renderProducts(); });
  paginationBar.appendChild(prevBtn);

  for (var i = 1; i <= totalPages; i++) {
    (function(pageNum) {
      var pageBtn = document.createElement("button");
      pageBtn.textContent = pageNum;
      if (pageNum === currentPage) pageBtn.classList.add("activePage");
      pageBtn.addEventListener("click", function() { currentPage = pageNum; renderProducts(); });
      paginationBar.appendChild(pageBtn);
    })(i);
  }

  var nextBtn = document.createElement("button");
  nextBtn.textContent = "Next";
  nextBtn.disabled = (currentPage === totalPages);
  nextBtn.addEventListener("click", function() { currentPage++; renderProducts(); });
  paginationBar.appendChild(nextBtn);
}

// handles delete button clicks using event delegation
document.getElementById("productList").addEventListener("click", function(e) {
  if (e.target.classList.contains("deleteBtn")) {
    var productId = parseInt(e.target.getAttribute("data-id"));
    productData = productData.filter(function(p) { return p.id !== productId; });
    saveProducts();
    currentPage = 1;
    updateCategoryDropdown();
    renderProducts();
    updateSummaryCards();
  }
});


// handles the add product button click
document.getElementById("addProductBtn").addEventListener("click", function() {

  // clear any previous error messages
  var fieldIds  = ["newName", "newPrice", "newStock", "newCategory"];
  var errorIds  = ["nameError", "priceError", "stockError", "categoryError"];
  for (var i = 0; i < fieldIds.length; i++) {
    document.getElementById(fieldIds[i]).classList.remove("invalid");
    document.getElementById(errorIds[i]).textContent = "";
  }

  var productName     = document.getElementById("newName").value.trim();
  var productPrice    = parseFloat(document.getElementById("newPrice").value);
  var productStock    = parseInt(document.getElementById("newStock").value);
  var productCategory = document.getElementById("newCategory").value;
  var isValid         = true;

  if (!productName) {
    document.getElementById("newName").classList.add("invalid");
    document.getElementById("nameError").textContent = "Please enter a name.";
    isValid = false;
  }
  if (isNaN(productPrice) || productPrice <= 0) {
    document.getElementById("newPrice").classList.add("invalid");
    document.getElementById("priceError").textContent = "Price must be more than 0.";
    isValid = false;
  }
  if (isNaN(productStock) || productStock < 0) {
    document.getElementById("newStock").classList.add("invalid");
    document.getElementById("stockError").textContent = "Stock cannot be negative.";
    isValid = false;
  }
  if (!productCategory) {
    document.getElementById("newCategory").classList.add("invalid");
    document.getElementById("categoryError").textContent = "Please pick a category.";
    isValid = false;
  }

  if (!isValid) return;

  productData.push({
    id:       Date.now(),
    name:     productName,
    price:    productPrice,
    stock:    productStock,
    category: productCategory
  });

  saveProducts();

  // clear the form after adding
  document.getElementById("newName").value     = "";
  document.getElementById("newPrice").value    = "";
  document.getElementById("newStock").value    = "";
  document.getElementById("newCategory").value = "";

  currentPage = 1;
  updateCategoryDropdown();
  renderProducts();
  updateSummaryCards();
});

// attach events to all the filter controls
document.getElementById("searchBox").addEventListener("input", function() { currentPage = 1; renderProducts(); });
document.getElementById("categoryDropdown").addEventListener("change", function() { currentPage = 1; renderProducts(); });
document.getElementById("sortDropdown").addEventListener("change", function() { currentPage = 1; renderProducts(); });
document.getElementById("lowStockOnly").addEventListener("change", function() { currentPage = 1; renderProducts(); });

// this runs when the page first loads
async function startApp() {
  var loadingScreen = document.getElementById("loadingScreen");
  var data = await loadProductsFromServer();
  productData = data;
  if (!getSavedProducts()) saveProducts();
  loadingScreen.classList.add("hide");
  updateCategoryDropdown();
  renderProducts();
  updateSummaryCards();
}

document.addEventListener("DOMContentLoaded", startApp);
