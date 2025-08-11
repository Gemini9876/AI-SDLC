import React from 'react';
import './ProductActionSection.css'; // Component-specific styles

/**
 * ProductActionSection component handles quantity input, product options, and the Add to Cart button.
 */
function ProductActionSection({
  actionData,
  quantity,
  setQuantity,
  selectedOption,
  setSelectedOption,
  onAddToCartClick,
  quantityError
}) {
  const {
    quantityInputLabel,
    quantityInputPlaceholder,
    addToCartButtonText,
    productOptions,
    addToCartButtonIcon
  } = actionData;

  // Convert productOptions object to an array for easier mapping
  const optionsArray = Object.entries(productOptions);

  return (
    <section className="product-action-section">
      {/* Product Options (e.g., Size) - Accessibility: Grouped with fieldset/legend */}
      <fieldset className="product-options">
        <legend className="sr-only">Product Options</legend>
        {optionsArray.map(([key, value]) => (
          <div key={key} className="option-item">
            <input
              type="radio"
              id={`option-${key}`}
              name="product-size"
              value={value}
              checked={selectedOption === value}
              onChange={() => setSelectedOption(value)}
              className="option-radio"
            />
            <label htmlFor={`option-${key}`} className="option-label">{value}</label>
          </div>
        ))}
      </fieldset>

      {/* Quantity Input - Accessibility: Labeled input */}
      <div className="quantity-input-group">
        <label htmlFor="quantity-input" className="quantity-label">
          {quantityInputLabel}
        </label>
        <input
          type="number" // Use type="number" for better mobile keyboards and validation
          id="quantity-input"
          className={`quantity-input ${quantityError ? 'input-error' : ''}`}
          placeholder={quantityInputPlaceholder}
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
          min="1" // HTML5 validation: Minimum value
          aria-invalid={!!quantityError} // ARIA attribute for invalid state
          aria-describedby={quantityError ? 'quantity-error-message' : undefined} // Link to error message
        />
        {quantityError && (
          <p id="quantity-error-message" className="error-message" role="alert">
            {quantityError}
          </p>
        )}
      </div>

      {/* Add to Cart Button - Accessibility: Icon with meaningful alt text if not purely decorative */}
      <button
        type="button"
        className="add-to-cart-button"
        onClick={onAddToCartClick}
      >
        {/* Icon: If icon is purely decorative alongside text, it could have aria-hidden="true".
            Given it's a shopping cart, it adds context, so an alt is appropriate. */}
        <img
          src={addToCartButtonIcon}
          alt="Shopping cart icon"
          className="cart-icon"
          width="20" // Example icon size
          height="20" // Example icon size
        />
        {addToCartButtonText}
      </button>
    </section>
  );
}

export default ProductActionSection;
