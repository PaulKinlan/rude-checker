document.addEventListener('DOMContentLoaded', () => {
    const productNameInput = document.getElementById('productName');
    const checkButton = document.getElementById('checkButton');
    const resultsDiv = document.getElementById('results');

    checkButton.addEventListener('click', () => {
        const productName = productNameInput.value.trim();
        if (productName) {
            checkProductName(productName);
        } else {
            alert('Please enter a product name');
        }
    });

    async function checkProductName(productName) {
        try {
            const response = await fetch('/check', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ product_name: productName }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const results = await response.json();
            displayResults(results);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while checking the product name');
        }
    }

    function displayResults(results) {
        resultsDiv.innerHTML = '';
        for (const [language, isOffensive] of Object.entries(results)) {
            const resultItem = document.createElement('div');
            resultItem.classList.add('result-item');
            resultItem.classList.add(isOffensive ? 'offensive' : 'safe');
            resultItem.textContent = `${language.charAt(0).toUpperCase() + language.slice(1)}: ${isOffensive ? 'Potentially offensive' : 'Safe'}`;
            resultsDiv.appendChild(resultItem);
        }
    }
});
