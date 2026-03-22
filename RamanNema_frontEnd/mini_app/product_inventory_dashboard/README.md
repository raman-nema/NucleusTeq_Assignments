Raman Nema | mini_project

## Product Inventory Dashboard

## Overview / Description:

The Product Inventory Dashboard is a web-based application designed to efficiently manage and monitor product data. It allows users to view, search, filter, and sort products while keeping track of stock availability in a simple and user-friendly interface.

Built using HTML, CSS, and JavaScript, this project focuses on implementing core frontend concepts without relying on any external frameworks. It demonstrates practical usage of DOM manipulation, event handling, and dynamic data rendering.

The dashboard helps users quickly identify low-stock items, organize products by category, and perform real-time searches, making it a useful tool for basic inventory management and analysis.

## Features:

• Product Listing
Displays products with essential details such as name, price, stock, and category in a clear and organized layout.

• Real-Time Search
Allows users to quickly find products by typing keywords, with instant results as they type.

• Category Filtering
Enables filtering of products based on selected categories for better organization and focus.

• Sorting Options
Provides sorting by price, name, or stock to help users arrange and analyze data easily.

• Low Stock Indicator
Highlights products with low or zero stock, making it easy to identify items that need attention.

• Dynamic Updates
Updates the product list instantly based on user actions without reloading the page.

• Local Storage Support
Saves data in the browser to maintain product information even after refreshing.

• User-Friendly Interface
Simple and clean design for smooth and intuitive interaction

## Tech Stack:

• HTML5 – Used for structuring the web page and content layout
• CSS3 – Used for styling, layout design, and creating a visually appealing interface
• JavaScript (ES6) – Used for implementing application logic, DOM manipulation, event handling, and dynamic updates
• Browser Local Storage – Used for storing and persisting product data on the client side

## Project Structure:

product-inventory-dashboard/
│
├── index.html # Main HTML file (structure of the application)
├── style.css # Styling and layout of the dashboard
├── script.js # Core JavaScript logic (search, filter, sort, render)
│
└── README.md # Project documentation

## How to run:

1. Clone the repository
   git clone <https://github.com/raman-nema/NucleusTeq_Assignments/tree/main/RamanNema_frontEnd/mini_app/product_inventory_dashboard>

2. Navigate to the project folder
   cd product-inventory-dashboard
3. Open the project
   • Double-click index.html
   OR
   • Open it using a browser:
   open index.html

4. Start using the application
   • View the product list
   • Use search, filter, and sort features
   • Data will be stored automatically in the browser (Local Storage)

OR
Optional (Using VS Code Live Server) 1. Open the project in VS Code 2. Install Live Server extension 3. Right-click index.html → Open with Live Server

## Data Structure:

The application uses an array of JavaScript objects to store product information. Each product is represented as an object with the following properties:
{
id: Number, // Unique identifier for each product
name: String, // Name of the product
price: Number, // Price of the product
stock: Number, // Available quantity in inventory
category: String // Category of the product (e.g., electronics, clothing)
}

## Key Concepts Used

• DOM Manipulation
Used to dynamically update and display product data on the webpage.
• Event Handling
Implemented to handle user interactions such as search input, dropdown selection, and checkbox actions.

• Array Methods
Functions like filter(), sort(), and map() are used to process and manage product data efficiently.

• Conditional Rendering
Applied to display different UI states such as low stock or out-of-stock products.

• Local Storage
Used to store and retrieve product data, ensuring persistence even after page refresh.

• Dynamic UI Updates
Enables real-time updates in the interface without reloading the page.

• Modular Code Structure
Code is organized into functions to improve readability and maintainability.

## Output:

## Dashboard Overview

This screenshot shows the main interface of the Product Inventory Dashboard. It displays key summary metrics such as total products, total inventory value, and out-of-stock items at the top.

Below the summary section, users can interact with features like search, category filtering, sorting, and low-stock filtering. The product cards display individual product details including name, price, stock status, and category.

The lower section provides a form to add new products, allowing users to dynamically update the inventory. The overall layout is clean and user-friendly, enabling efficient inventory management.

![Dashboard Screenshot](https://github.com/raman-nema/NucleusTeq_Assignments/blob/719010cbb637e6df4af80b960fa550c2bd92afe9/RamanNema_frontEnd/mini_app/assets/mp%201.png)


## Search Functionality

This screenshot demonstrates the real-time search feature of the application. As the user types a keyword (e.g., “rd”) in the search bar, the product list dynamically filters to display only the matching results.

The filtering is case-insensitive and updates instantly without reloading the page, providing a smooth and efficient user experience.

![searchFunc Screenshot](https://github.com/raman-nema/NucleusTeq_Assignments/blob/719010cbb637e6df4af80b960fa550c2bd92afe9/RamanNema_frontEnd/mini_app/assets/mp%202.png)

## Category Filtering

This screenshot demonstrates the category filtering feature of the dashboard. When the user selects a specific category (e.g., “Electronics”) from the dropdown menu, only the products belonging to that category are displayed.

This functionality helps users easily organize and view relevant products without distraction, improving overall usability and data navigation.

![categoryFiltering Screenshot](https://github.com/raman-nema/NucleusTeq_Assignments/blob/719010cbb637e6df4af80b960fa550c2bd92afe9/RamanNema_frontEnd/mini_app/assets/mp%203.png)

## Sorting Functionality

This screenshot demonstrates the sorting feature of the dashboard. Users can organize products based on different criteria such as price (low to high or high to low) and name (A to Z or Z to A) using the dropdown menu.

The product list updates instantly based on the selected option, allowing users to analyze and arrange inventory data efficiently.

![sortingFunc Screenshot](https://github.com/raman-nema/NucleusTeq_Assignments/blob/719010cbb637e6df4af80b960fa550c2bd92afe9/RamanNema_frontEnd/mini_app/assets/mp%204.png)

## Low Stock Indicator

This screenshot highlights the low stock filtering feature of the dashboard. When the “Low Stock Only” option is enabled, only products with limited stock are displayed.

Products with low inventory are clearly marked (e.g., “Only 4 left”), helping users quickly identify items that require restocking and take necessary action.

![lowStockInd Screenshot](https://github.com/raman-nema/NucleusTeq_Assignments/blob/719010cbb637e6df4af80b960fa550c2bd92afe9/RamanNema_frontEnd/mini_app/assets/mp%205.png)

## Local Storage Persistence

This screenshot shows the browser’s Local Storage where product data is stored in JSON format under different keys such as products, inventoryData, and inv_products.

The presence of this data confirms that the application stores and retrieves product information using the browser’s Local Storage API. This ensures that all inventory data persists even after refreshing or reopening the application.

This demonstrates successful implementation of client-side data persistence.

![localStorage Screenshot](https://github.com/raman-nema/NucleusTeq_Assignments/blob/719010cbb637e6df4af80b960fa550c2bd92afe9/RamanNema_frontEnd/mini_app/assets/mp%206.png)

## Conclusion

This project demonstrates the practical implementation of core JavaScript concepts such as DOM manipulation, event handling, and data persistence using Local Storage. It provides a simple yet effective solution for managing product inventory in a user-friendly way.
