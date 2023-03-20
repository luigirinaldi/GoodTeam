import re  
from collections import Counter
import textdistance 
import pandas as pd

w = [] #words
with open('big.txt','r',encoding="utf8") as f:
    file_name_data = f.read()
    file_name_data = file_name_data.lower()
    w = re.findall('\w+', file_name_data)

v = set(w) #vocabulary
#print(f"The first 10 words in our dictionary are: \n{w[0:10]}")
#print(f"The dictionary has {len(v)} words ")


def get_count(words):
        word_freq = {}  
        word_freq = Counter(words)
        return word_freq
word_freq = get_count(w)
# print("Most common words in the dataset are: ", word_freq.most_common()[0:10])

def get_probs(word_count_dict):
    probs = {}
    m = sum(word_count_dict.values())
    for key in word_count_dict.keys():
        probs[key] = word_count_dict[key] / m
    return probs


probs = get_probs(word_freq)

def my_autocorrect(input_word):
    input_word = input_word.lower()
    if input_word in v:
            return('Your word seems to be correct')
    else:
        sim = [1-(textdistance.Jaccard(qval=2).distance(v,input_word)) for v in word_freq.keys()]
        df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
        df = df.rename(columns={'index':'Word', 0:'Prob'})
        df['Similarity'] = sim
        output = df.sort_values(['Similarity', 'Prob'], ascending=False).head()
        best_correction = output.iat[1,0]
        return(best_correction)
    

