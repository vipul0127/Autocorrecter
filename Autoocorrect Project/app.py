from flask import Flask, request, jsonify, render_template
import pandas as pd
import re
import textdistance
from collections import Counter

app = Flask(__name__)

# Load and process the word data
words = []
with open('book.txt', 'r', encoding='utf8') as f:
    file_name_data = f.read().lower()

words = re.findall(r'\w+', file_name_data)
word_freq = Counter(words)
v = list(word_freq.keys())

def autocorrect(input_word):
    input_word = input_word.lower()
    if input_word in v:
        return {"message": f"Word is already there: {input_word}", "suggestions": []}
    else:
        similarities = [1 - textdistance.Jaccard(qval=2).distance(w, input_word) for w in v]
        df = pd.DataFrame(list(zip(v, similarities)), columns=['Word', 'Similarity'])
        output = df.sort_values(['Similarity', 'Word'], ascending=[False, True]).head(10)
        suggestions = output.to_dict(orient='records')
        return {"message": "Suggested corrections:", "suggestions": suggestions}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_similar_words', methods=['POST'])
def get_similar_words():
    input_word = request.json.get('word', '')
    result = autocorrect(input_word)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
