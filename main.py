from flask import Flask, render_template, request, jsonify
from offensive_words import offensive_words
import logging
import jellyfish
import random
import string
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up the Gemini API
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

def is_offensive(text, lang_code):
    logger.debug(f"Checking if '{text}' is offensive in {lang_code}")
    
    # Check for offensive words
    if text.lower() in offensive_words.get(lang_code, []):
        logger.info(f"Offensive content detected in {lang_code}: {text}")
        return True
    
    logger.debug(f"'{text}' is not offensive in {lang_code}")
    return False

def check_phonetic_similarity(input_word, offensive_words):
    similar_words = []
    for lang, words in offensive_words.items():
        for word in words:
            if jellyfish.soundex(input_word) == jellyfish.soundex(word):
                similar_words.append((lang, word))
    return similar_words

def generate_alternative_names(product_name, num_suggestions=3):
    alternatives = set()
    while len(alternatives) < num_suggestions:
        new_name = list(product_name)
        for i in range(random.randint(1, len(product_name))):
            index = random.randint(0, len(product_name) - 1)
            new_name[index] = random.choice(string.ascii_lowercase)
        alternative = ''.join(new_name)
        if alternative != product_name:
            alternatives.add(alternative)
    return list(alternatives)

def check_offensive_content_llm(text):
    prompt = f"Analyze the following product name for any offensive, rude, or culturally inappropriate meanings across different languages and cultures. If it's problematic, explain why. If it's not, just say it's fine: {text}"
    response = model.generate_content(prompt)
    return response.text

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_product_name():
    product_name = request.json["product_name"].lower()
    results = {
        "literal_matches": [],
        "phonetic_matches": [],
        "alternative_suggestions": [],
        "llm_analysis": check_offensive_content_llm(product_name)
    }

    # Check for literal matches
    for lang_code, words in offensive_words.items():
        if is_offensive(product_name, lang_code):
            results["literal_matches"].append(lang_code)

    # Check for phonetic similarities
    phonetic_matches = check_phonetic_similarity(product_name, offensive_words)
    results["phonetic_matches"] = phonetic_matches

    # Generate alternative suggestions if there are any matches
    if results["literal_matches"] or results["phonetic_matches"]:
        results["alternative_suggestions"] = generate_alternative_names(product_name)

    logger.info(f"Results for '{product_name}': {results}")

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
