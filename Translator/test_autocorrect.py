import re  
from collections import Counter
import textdistance 
import pandas as pd

# Jaccard Algorithm
w = [] #words
with open('big.txt','r',encoding="utf8") as f:
    file_name_data = f.read()
    file_name_data = file_name_data.lower()
    w = re.findall('\w+', file_name_data)

v = set(w) #vocabulary
print(f"The first 10 words in our dictionary are: \n{w[0:10]}")
print(f"The dictionary has {len(v)} words ")


def get_count(words):
        word_freq = {}  
        word_freq = Counter(words)
        return word_freq
word_freq = get_count(w)
print("Most common words in the dataset are: ", word_freq.most_common()[0:10])

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


### ALGORITHM #2
import timeit

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('test.txt').read()))
print(len(WORDS))
print(sum(WORDS.values()))
print(WORDS['the'])

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
    

my_word = input("Enter any word:")
print(correction(my_word))


#### TESTING 
words = w

def spelltest(tests, verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    start = timeit.timeit()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        print(1)
        w = correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in w)
            print(verbose)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, words[w], right, words[right]))
    dt = timeit.timeit() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))
    
def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]

if __name__ == '__main__':
    spelltest(Testset(open('spell-testset1.txt')))
    spelltest(Testset(open('spell-testset2.txt')))

