import pandas as pd
import numpy as np
import textdistance
import re
from collections import Counter

words = []
with open('/book.txt', 'r', encoding='utf8') as f:
    file_name_data = f.read().lower()

words = re.findall(r'\w+', file_name_data)
word_freq = Counter(words)
v = list(word_freq.keys())

relative_p = {}
for w in v:
    relative_p[w] = word_freq[w] / len(words)

def autocorrect(input_word):
    input_word = input_word.lower()
    if input_word in v:
        print("Word is already there: " + input_word)
    else:
        similarities = [1 - textdistance.Jaccard(qval=2).distance(w, input_word) for w in v]
        df = pd.DataFrame(list(zip(v, similarities)), columns=['Word', 'Similarity'])
        output = df.sort_values(['Similarity', 'Word'], ascending=[False, True]).head(10)
        print("Suggested corrections:")
        print(output)


