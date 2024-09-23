from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from offensive_words import offensive_words
import spacy

app = Flask(__name__)
translator = Translator()
nlp = spacy.load("en_core_web_sm")

# Supported languages for translation
supported_languages = ["english", "spanish", "french", "german", "italian", "japanese", "chinese", "russian"]

def contains_offensive_word(text, word_list):
    return any(offensive_word in text for offensive_word in word_list)

def analyze_text_sentiment(text):
    doc = nlp(text)
    sentiment_score = sum([token.sentiment for token in doc]) / len(doc)
    return sentiment_score

def is_offensive(text, lang_code):
    # Check for offensive words
    if contains_offensive_word(text, offensive_words.get(lang_code, [])):
        return True
    
    # Analyze sentiment (for English only)
    if lang_code == "english":
        sentiment_score = analyze_text_sentiment(text)
        if sentiment_score < -0.5:  # Adjust this threshold as needed
            return True
    
    return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_product_name():
    product_name = request.json["product_name"].lower()
    results = {}

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
        except Exception as e:
            # Log the error and continue with the next language
            print(f"Error translating to {lang_code}: {str(e)}")
            results[lang_code] = {
                "translation": "Translation failed",
                "is_offensive": False
            }

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
