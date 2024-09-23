from flask import Flask, render_template, request, jsonify
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

# In-memory dictionary of offensive words in different languages
# In a production environment, this would be stored in a database
offensive_words = {
    "english": ["offensive1", "offensive2", "offensive3"],
    "spanish": ["ofensivo1", "ofensivo2", "ofensivo3"],
    "french": ["offensant1", "offensant2", "offensant3"]
}

# Supported languages for translation
supported_languages = ["en", "es", "fr"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_product_name():
    product_name = request.json["product_name"].lower()
    results = {}

    for lang_code in supported_languages:
        # Translate the product name
        translation = translator.translate(product_name, dest=lang_code)
        translated_name = translation.text.lower()

        # Check for offensive words
        lang_name = translation.dest_lang
        is_offensive = any(word in translated_name for word in offensive_words.get(lang_name, []))

        results[lang_name] = {
            "translation": translated_name,
            "is_offensive": is_offensive
        }

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
