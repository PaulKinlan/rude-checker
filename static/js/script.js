document.addEventListener('DOMContentLoaded', () => {
    const productNameInput = document.getElementById('productName');
    const checkButton = document.getElementById('checkButton');
    const resultsDiv = document.getElementById('results');
    const alternativesDiv = document.getElementById('alternatives');

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
            console.log('Received results:', results); // Add this line for debugging
            displayResults(results);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while checking the product name');
        }
    }

    function displayResults(results) {
        resultsDiv.innerHTML = '';
        alternativesDiv.innerHTML = '';
        let isOffensive = false;

        console.log('Displaying results:', results); // Add this line for debugging

        for (const [language, data] of Object.entries(results)) {
            if (language === 'alternative_suggestions') {
                console.log('Alternative suggestions:', data); // Add this line for debugging
                continue;
            }

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

            if (data.is_offensive) {
                isOffensive = true;
            }
        }

        if (isOffensive && results.alternative_suggestions) {
            console.log('Displaying alternative suggestions:', results.alternative_suggestions); // Add this line for debugging
            const alternativesHeader = document.createElement('h3');
            alternativesHeader.textContent = 'Alternative Suggestions:';
            alternativesDiv.appendChild(alternativesHeader);

            const alternativesList = document.createElement('ul');
            results.alternative_suggestions.forEach(suggestion => {
                const listItem = document.createElement('li');
                listItem.textContent = suggestion;
                alternativesList.appendChild(listItem);
            });
            alternativesDiv.appendChild(alternativesList);
        }
    }
});
