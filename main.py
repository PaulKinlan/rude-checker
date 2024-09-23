from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from offensive_words import offensive_words
import spacy
import random
import string
import logging
import nltk
from nltk.corpus import wordnet

app = Flask(__name__)
translator = Translator()
nlp = spacy.load("en_core_web_sm")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data
nltk.download('wordnet')

# Supported languages for translation
supported_languages = ["english", "spanish", "french", "german", "italian", "japanese", "zh-cn", "russian"]

def contains_offensive_word(text, word_list):
    for word in word_list:
        if word in text:
            logger.info(f"Offensive word detected: {word}")
            return True
    return False

def analyze_text_sentiment(text):
    doc = nlp(text)
    sentiment_score = sum([token.sentiment for token in doc]) / len(doc)
    return sentiment_score

def is_offensive(text, lang_code):
    logger.debug(f"Checking if '{text}' is offensive in {lang_code}")
    
    # Check for offensive words
    if contains_offensive_word(text, offensive_words.get(lang_code, [])):
        logger.info(f"Offensive content detected in {lang_code}: {text}")
        return True
    
    # Analyze sentiment (for English only)
    if lang_code == "english":
        sentiment_score = analyze_text_sentiment(text)
        logger.debug(f"Sentiment score for '{text}': {sentiment_score}")
        if sentiment_score < -0.5:  # Adjust this threshold as needed
            logger.info(f"Negative sentiment detected in English: {text} (score: {sentiment_score})")
            return True
    
    logger.debug(f"'{text}' is not offensive in {lang_code}")
    return False

def generate_alternative_names(product_name, num_suggestions=3):
    alternatives = []
    words = product_name.split()
    
    for _ in range(num_suggestions):
        new_name = []
        for word in words:
            synsets = wordnet.synsets(word)
            if synsets:
                synonym = random.choice(synsets).lemmas()[0].name()
                new_name.append(synonym)
            else:
                new_name.append(word)
        
        alternative = ' '.join(new_name)
        if alternative != product_name and alternative not in alternatives:
            alternatives.append(alternative)
    
    # If we couldn't generate enough alternatives, fall back to character replacement
    while len(alternatives) < num_suggestions:
        chars = list(product_name)
        index = random.randint(0, len(chars) - 1)
        chars[index] = random.choice(string.ascii_lowercase)
        alternative = ''.join(chars)
        if alternative != product_name and alternative not in alternatives:
            alternatives.append(alternative)
    
    logger.info(f"Generated alternative names for '{product_name}': {alternatives}")
    return alternatives

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_product_name():
    product_name = request.json["product_name"].lower()
    results = {}
    is_offensive_in_any_language = False

    for lang_code in supported_languages:
        try:
            # Translate the product name
            translation = translator.translate(product_name, dest=lang_code)
            translated_name = translation.text.lower()

            # Get the language name
            lang_name = translation.dest

            # Check for offensive content using spaCy and custom logic
            is_offensive_result = is_offensive(translated_name, lang_name)

            results[lang_name] = {
                "translation": translated_name,
                "is_offensive": is_offensive_result
            }

            if is_offensive_result:
                is_offensive_in_any_language = True

        except Exception as e:
            # Log the error and continue with the next language
            logger.error(f"Error translating to {lang_code}: {str(e)}")
            results[lang_code] = {
                "translation": "Translation failed",
                "is_offensive": False
            }

    # Log the value of is_offensive_in_any_language
    logger.debug(f"Is offensive in any language: {is_offensive_in_any_language}")

    # Generate alternative suggestions if the name is offensive in any language
    if is_offensive_in_any_language:
        alternative_suggestions = generate_alternative_names(product_name)
        results["alternative_suggestions"] = alternative_suggestions
        logger.info(f"Generated alternative suggestions for offensive name '{product_name}': {alternative_suggestions}")
    else:
        logger.info(f"No offensive content detected for '{product_name}' in any language")

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
