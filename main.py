from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from offensive_words import offensive_words

app = Flask(__name__)
translator = Translator()

# Supported languages for translation
supported_languages = list(offensive_words.keys())

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

            # Check for offensive words
            is_offensive = any(word in translated_name for word in offensive_words.get(lang_name, []))

            results[lang_name] = {
                "translation": translated_name,
                "is_offensive": is_offensive
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
