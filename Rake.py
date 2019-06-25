#!/usr/bin/Python
# -*- coding: utf-8 -*
from rake_nltk import Rake
print("hello")

r = Rake()
my_test = "Brisbane International is Now the Worlds First Crypto-Friendly Airport  #Bitcoin https://t.co/km04kEt7yd."
r.extract_keywords_from_text(my_test)

keyword = r.get_ranked_phrases()

# print(r.get_ranked_phrases())
print(keyword)
print(keyword[0])
print(keyword[0][0])
print("==============================")

score = r.get_ranked_phrases_with_scores()
print(score)
print(score[0])
print(score[0][1])

# print(r.get_ranked_phrases_with_scores())
print("===========================")
print(r.stopwords)
print("=============================")
print(r.get_word_degrees())
