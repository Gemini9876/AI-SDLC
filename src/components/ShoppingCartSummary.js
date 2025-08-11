import React from 'react';
import './ShoppingCartSummary.css'; // Component-specific styles

/**
 * ShoppingCartSummary component provides a mock summary of items in the cart.
 * In a real application, this would be a more complex component fetching actual cart data.
 */
function ShoppingCartSummary({ cartItems, totalItems }) {
  return (
    <div className="shopping-cart-summary" aria-live="polite" aria-atomic="true">
      <h2>Your Cart ({totalItems} items)</h2>
      {cartItems.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <ul>
          {cartItems.map((item, index) => (
            <li key={index} className="cart-item">
              {item.name} ({item.option ? item.option + ', ' : ''}Qty: {item.quantity})
            </li>
          ))}
        </ul>
      )}
      {/* Mock Cart Icon/Count - This would typically be in a header component */}
      <div className="mock-cart-icon">
        🛒 <span className="cart-count">{totalItems}</span>
      </div>
    </div>
  );
}

export default ShoppingCartSummary;
