import csv
import random

#Open the Word Lists
file = open("word_libraries/answer_words.csv")
answer_words_csv = csv.reader(file)
file = open("word_libraries/guess_words.csv")
guess_words_csv = csv.reader(file)

#Create the Word Lists
answer_words_list = []
guess_words_list = []
for row in answer_words_csv:
    answer_words_list.append(str(row))
    guess_words_list.append(str(row))
for row in guess_words_csv:
    guess_words_list.append(str(row))
