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
            console.log('Received results:', results);
            displayResults(results, productName);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while checking the product name');
        }
    }

    function displayResults(results, productName) {
        resultsDiv.innerHTML = '';

        const resultHeader = document.createElement('h2');
        resultHeader.textContent = `Results for "${productName}"`;
        resultsDiv.appendChild(resultHeader);

        // Display literal matches
        const literalMatchesDiv = document.createElement('div');
        literalMatchesDiv.classList.add('result-section');
        literalMatchesDiv.innerHTML = '<h3>Literal Matches</h3>';
        if (results.literal_matches.length > 0) {
            const matchList = document.createElement('ul');
            results.literal_matches.forEach(lang => {
                const listItem = document.createElement('li');
                listItem.textContent = `Offensive in ${lang}`;
                matchList.appendChild(listItem);
            });
            literalMatchesDiv.appendChild(matchList);
        } else {
            literalMatchesDiv.innerHTML += '<p>No literal matches found.</p>';
        }
        resultsDiv.appendChild(literalMatchesDiv);

        // Display phonetic matches
        const phoneticMatchesDiv = document.createElement('div');
        phoneticMatchesDiv.classList.add('result-section');
        phoneticMatchesDiv.innerHTML = '<h3>Phonetic Similarities</h3>';
        if (results.phonetic_matches.length > 0) {
            const matchList = document.createElement('ul');
            results.phonetic_matches.forEach(([lang, word]) => {
                const listItem = document.createElement('li');
                listItem.textContent = `Similar to "${word}" in ${lang}`;
                matchList.appendChild(listItem);
            });
            phoneticMatchesDiv.appendChild(matchList);
        } else {
            phoneticMatchesDiv.innerHTML += '<p>No phonetic similarities found.</p>';
        }
        resultsDiv.appendChild(phoneticMatchesDiv);

        // Display alternative suggestions
        if (results.alternative_suggestions && results.alternative_suggestions.length > 0) {
            const suggestionsDiv = document.createElement('div');
            suggestionsDiv.classList.add('result-section');
            suggestionsDiv.innerHTML = '<h3>Alternative Suggestions</h3>';
            const suggestionList = document.createElement('ul');
            results.alternative_suggestions.forEach(suggestion => {
                const listItem = document.createElement('li');
                listItem.textContent = suggestion;
                suggestionList.appendChild(listItem);
            });
            suggestionsDiv.appendChild(suggestionList);
            resultsDiv.appendChild(suggestionsDiv);
        }
    }
});
