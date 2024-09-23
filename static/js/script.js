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
        for (const [language, data] of Object.entries(results)) {
            const resultItem = document.createElement('div');
            resultItem.classList.add('result-item');
            resultItem.classList.add(data.is_offensive ? 'offensive' : 'safe');
            
            const languageHeader = document.createElement('h3');
            languageHeader.textContent = language.charAt(0).toUpperCase() + language.slice(1);
            resultItem.appendChild(languageHeader);

            const translationPara = document.createElement('p');
            translationPara.textContent = `Translation: ${data.translation}`;
            resultItem.appendChild(translationPara);

            const offensivePara = document.createElement('p');
            offensivePara.textContent = data.is_offensive ? 'Potentially offensive' : 'Safe';
            resultItem.appendChild(offensivePara);

            resultsDiv.appendChild(resultItem);
        }
    }
});
