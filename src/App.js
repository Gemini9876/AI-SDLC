import React, { useState } from 'react';
import ProductDetailPage from './components/ProductDetailPage';
import ShoppingCartSummary from './components/ShoppingCartSummary';
import './App.css'; // Global styles or for App component

// UI Data Model as provided
const UI_DATA_MODEL = {
  "productDisplaySection": {
    "productImage": "/content/dam/ecommerce/products/super-gadget-pro.jpg",
    "productName": "Super Gadget Pro",
    "productPrice": "$99.99",
    "productDescription": "The Super Gadget Pro is an advanced device designed for unparalleled performance and user experience, making it the perfect addition to your daily life."
  },
  "productActionSection": {
    "quantityInputLabel": "Quantity:",
    "quantityInputPlaceholder": "1",
    "addToCartButtonText": "Add to Cart",
    "productOptions": {
      "optionSizeSmall": "Small",
      "optionSizeMedium": "Medium",
      "optionSizeLarge": "Large"
    },
    "addToCartButtonIcon": "/content/dam/icons/shopping-cart-icon.svg"
  }
};

function App() {
  // State to manage items in the shopping cart (mock)
  const [cartItems, setCartItems] = useState([]);
  const [message, setMessage] = useState({
    text: '',
    type: '' // 'success' or 'error'
  });

  /**
   * Handles adding a product to the cart.
   * This function would typically interact with a backend API.
   * For this implementation, it updates client-side state.
   * @param {string} productName - The name of the product.
   * @param {number} quantity - The quantity to add.
   * @param {string} selectedOption - The selected product option (e.g., size).
   */
  const handleAddToCart = (productName, quantity, selectedOption) => {
    // Clear previous messages
    setMessage({ text: '', type: '' });

    // Input validation for quantity
    if (isNaN(quantity) || quantity <= 0) {
      setMessage({ text: 'Quantity must be at least 1.', type: 'error' });
      return false;
    }
    
    // Simulate adding to cart
    setCartItems(prevItems => {
      const existingItemIndex = prevItems.findIndex(
        item => item.name === productName && item.option === selectedOption
      );

      if (existingItemIndex > -1) {
        // If item exists, update quantity
        const updatedItems = [...prevItems];
        updatedItems[existingItemIndex].quantity += quantity;
        return updatedItems;
      } else {
        // Add new item
        return [...prevItems, { name: productName, quantity: quantity, option: selectedOption }];
      }
    });

    const messageText = quantity === 1
      ? `${productName} has been added to your cart.`
      : `${quantity} ${productName} items have been added to your cart.`;
    setMessage({ text: messageText, type: 'success' });

    return true;
  };

  // Calculate total items for cart icon/count
  const totalCartItems = cartItems.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <div className="App">
      {/* Accessibility: Main content landmark */}
      <main className="product-page-container">
        {/* Global Success/Error Message Display */}
        {message.text && (
          <div className={`global-message ${message.type}`}>
            {message.text}
          </div>
        )}

        <ProductDetailPage
          uiData={UI_DATA_MODEL}
          onAddToCart={handleAddToCart}
          productName={UI_DATA_MODEL.productDisplaySection.productName}
        />

        {/* Mock Shopping Cart Summary, updated based on client-side state */}
        <aside className="shopping-cart-aside">
          <ShoppingCartSummary
            cartItems={cartItems}
            totalItems={totalCartItems}
          />
        </aside>
      </main>
    </div>
  );
}

export default App;
