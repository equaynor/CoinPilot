document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('trade-form');
    const coinError = document.getElementById('coin-error');
    const tradeTypeError = document.getElementById('trade-type-error');
    const quantityError = document.getElementById('quantity-error');
    const priceError = document.getElementById('price-error');
  
    form.addEventListener('submit', function(event) {
      event.preventDefault();
  
      const coin = document.getElementById('id_coin').value;
      const tradeType = document.getElementById('id_trade_type').value;
      const quantity = parseFloat(document.getElementById('id_quantity').value);
      const price = parseFloat(document.getElementById('id_price').value);
  
      let isValid = true;
  
      if (!coin) {
        coinError.textContent = 'Please select a coin.';
        isValid = false;
      } else {
        coinError.textContent = '';
      }
  
      if (!tradeType) {
        tradeTypeError.textContent = 'Please select a trade type.';
        isValid = false;
      } else {
        tradeTypeError.textContent = '';
      }
  
      if (isNaN(quantity) || quantity <= 0) {
        quantityError.textContent = 'Please enter a valid quantity.';
        isValid = false;
      } else {
        quantityError.textContent = '';
      }
  
      if (isNaN(price) || price <= 0) {
        priceError.textContent = 'Please enter a valid price.';
        isValid = false;
      } else {
        priceError.textContent = '';
      }
  
      if (isValid) {
        form.submit();
      }
    });
  });