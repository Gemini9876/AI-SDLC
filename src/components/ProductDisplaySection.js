import React from 'react';
import './ProductDisplaySection.css'; // Component-specific styles

/**
 * ProductDisplaySection component displays the product image, name, price, and description.
 */
function ProductDisplaySection({ productData }) {
  const { productImage, productName, productPrice, productDescription } = productData;

  return (
    <section className="product-display-section">
      {/* Accessibility: Image with appropriate alt text */}
      <img
        src={productImage}
        alt={`Image of ${productName}`}
        className="product-image"
        width="400" // Example fixed width for layout
        height="400" // Example fixed height for layout
      />
      <h1 id="product-name-heading" className="product-name">{productName}</h1>
      <p className="product-price">{productPrice}</p>
      {/* XSS Prevention: React automatically escapes string children. 
          If productDescription contained raw HTML that *should* be rendered, 
          a sanitization library like DOMPurify with dangerouslySetInnerHTML would be required. 
          For simple text, direct rendering is safe and default. */}
      <p className="product-description">{productDescription}</p>
    </section>
  );
}

export default ProductDisplaySection;
