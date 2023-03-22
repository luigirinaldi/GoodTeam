from utils import *
import sys

# word = "Hello world"
word = sys.argv[1]
word = word.replace(" ", "x")
print(word)

print(wordToTaps(word))