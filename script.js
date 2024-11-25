<script>
async function submitOrder() {
    // Collect order data from form fields (example fields)
    const orderData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        address: document.getElementById('address').value,
        cartItems: ["item1", "item2"]  // Replace with real cart items
    };

    // Send data to the Flask backend
    const response = await fetch('http://127.0.0.1:5000/submit-order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(orderData)
    });

    const result = await response.json();
    alert(result.message);  // Display success message
    
}
</script>