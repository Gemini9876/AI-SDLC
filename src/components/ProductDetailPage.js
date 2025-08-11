import React, { useState } from 'react';
import ProductDisplaySection from './ProductDisplaySection';
import ProductActionSection from './ProductActionSection';
import './ProductDetailPage.css'; // Component-specific styles

/**
 * ProductDetailPage component orchestrates the display and action sections
 * for a product on its detail page.
 * It manages the local state for quantity and selected options.
 */
function ProductDetailPage({ uiData, onAddToCart, productName }) {
  const [quantity, setQuantity] = useState(uiData.productActionSection.quantityInputPlaceholder || '1');
  const [selectedOption, setSelectedOption] = useState(Object.values(uiData.productActionSection.productOptions)[0] || '');
  const [quantityError, setQuantityError] = useState('');

  /**
   * Handles the click event for the 'Add to Cart' button.
   * Performs local validation and calls the parent's onAddToCart function.
   */
  const handleAddToCartClick = () => {
    setQuantityError(''); // Clear previous errors
    const parsedQuantity = parseInt(quantity, 10);

    if (isNaN(parsedQuantity)) {
      setQuantityError('Please enter a valid number for quantity.');
      return; // Stop the process
    }
    if (parsedQuantity <= 0) {
      setQuantityError('Quantity must be at least 1.');
      return; // Stop the process
    }

    // Call the parent handler to add to cart
    const success = onAddToCart(productName, parsedQuantity, selectedOption);

    // Reset quantity to default if successfully added to cart
    if (success) {
      setQuantity(uiData.productActionSection.quantityInputPlaceholder || '1');
    }
  };

  return (
    <article className="product-detail-page" aria-labelledby="product-name-heading">
      {/* Product Display Section */}
      <ProductDisplaySection
        productData={uiData.productDisplaySection}
      />

      {/* Product Action Section */}
      <ProductActionSection
        actionData={uiData.productActionSection}
        quantity={quantity}
        setQuantity={setQuantity}
        selectedOption={selectedOption}
        setSelectedOption={setSelectedOption}
        onAddToCartClick={handleAddToCartClick}
        quantityError={quantityError}
      />
    </article>
  );
}

export default ProductDetailPage;
