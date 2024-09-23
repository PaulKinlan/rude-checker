from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-memory dictionary of offensive words in different languages
# In a production environment, this would be stored in a database
offensive_words = {
    "english": ["offensive1", "offensive2", "offensive3"],
    "spanish": ["ofensivo1", "ofensivo2", "ofensivo3"],
    "french": ["offensant1", "offensant2", "offensant3"]
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_product_name():
    product_name = request.json["product_name"].lower()
    results = {}

    for language, words in offensive_words.items():
        is_offensive = any(word in product_name for word in words)
        results[language] = is_offensive

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
