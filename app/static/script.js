document.addEventListener('DOMContentLoaded', () => {
    const reviewInput = document.getElementById('review-input');
    const charCount = document.getElementById('char-count');
    const sentimentIndicator = document.getElementById('sentiment-indicator');
    const emojiDisplay = document.getElementById('emoji-display');
    const sentimentLabel = document.getElementById('sentiment-label');
    const sentimentSubtext = document.getElementById('sentiment-subtext');
    const posPercent = document.getElementById('pos-percent');
    const negPercent = document.getElementById('neg-percent');
    const posBar = document.getElementById('pos-bar');
    const negBar = document.getElementById('neg-bar');
    const exampleBtns = document.querySelectorAll('.example-btn');

    // Debounce function to limit API requests while typing
    function debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    // Call the sentiment analysis API
    async function analyzeSentiment(text) {
        if (!text.trim()) {
            resetUI();
            return;
        }

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text })
            });

            if (!response.ok) {
                throw new Error('API request failed');
            }

            const data = await response.json();
            updateUI(data);
        } catch (error) {
            console.error('Error analyzing sentiment:', error);
            sentimentLabel.textContent = "Error";
            sentimentSubtext.textContent = "Could not connect to model backend.";
        }
    }

    // Debounced version of our analysis function
    const debouncedAnalyze = debounce((text) => analyzeSentiment(text), 300);

    // Reset UI to initial state
    function resetUI() {
        sentimentIndicator.className = 'sentiment-indicator';
        emojiDisplay.textContent = '🤔';
        sentimentLabel.textContent = 'Awaiting Input';
        sentimentSubtext.textContent = 'Start typing or click a quick example to analyze.';
        
        posPercent.textContent = '50%';
        negPercent.textContent = '50%';
        posBar.style.width = '50%';
        negBar.style.width = '50%';
    }

    // Update UI components with API results
    function updateUI(data) {
        const { sentiment, confidence, probabilities } = data;
        
        // Convert probabilities to whole percentages
        const posVal = Math.round(probabilities.positive * 100);
        const negVal = Math.round(probabilities.negative * 100);

        // Update progress bars
        posPercent.textContent = `${posVal}%`;
        negPercent.textContent = `${negVal}%`;
        posBar.style.width = `${posVal}%`;
        negBar.style.width = `${negVal}%`;

        // Update main sentiment indicator card
        sentimentIndicator.className = 'sentiment-indicator'; // Reset classes
        
        if (sentiment === 'positive') {
            sentimentIndicator.classList.add('positive');
            sentimentLabel.textContent = 'Positive Sentiment';
            
            // Adjust emoji based on confidence
            if (confidence > 0.85) {
                emojiDisplay.textContent = '😍';
                sentimentSubtext.textContent = `Excellent! Extremely high positive score (${(confidence * 100).toFixed(1)}%).`;
            } else {
                emojiDisplay.textContent = '😊';
                sentimentSubtext.textContent = `Looks positive! Confidence score: ${(confidence * 100).toFixed(1)}%.`;
            }
        } else if (sentiment === 'negative') {
            sentimentIndicator.classList.add('negative');
            sentimentLabel.textContent = 'Negative Sentiment';
            
            // Adjust emoji based on confidence
            if (confidence > 0.85) {
                emojiDisplay.textContent = '😡';
                sentimentSubtext.textContent = `Oh no! Highly critical negative score (${(confidence * 100).toFixed(1)}%).`;
            } else {
                emojiDisplay.textContent = '😞';
                sentimentSubtext.textContent = `Seems negative. Confidence score: ${(confidence * 100).toFixed(1)}%.`;
            }
        } else {
            resetUI();
        }
    }

    // Input text area event listeners
    reviewInput.addEventListener('input', (e) => {
        const text = e.target.value;
        charCount.textContent = text.length;
        debouncedAnalyze(text);
    });

    // Handle Quick Example button clicks
    exampleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const sampleText = btn.getAttribute('data-text');
            reviewInput.value = sampleText;
            charCount.textContent = sampleText.length;
            
            // Trigger animation for filling text
            reviewInput.classList.add('fill-anim');
            setTimeout(() => reviewInput.classList.remove('fill-anim'), 300);

            // Execute immediately without debounce for examples
            analyzeSentiment(sampleText);
        });
    });
});
