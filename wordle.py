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
    word = str(row)[2:-2]
    answer_words_list.append(word)
    guess_words_list.append(word)
for row in guess_words_csv:
    word = str(row)[2:-2]
    guess_words_list.append(word)

#Determine words
answer = answer_words_list[random.randrange(len(answer_words_list))]
guess = input("Enter your guess: ")

#Function Definition
def compare(word):
    checkWord = list(answer)
    hits = []
    for i in range(len(word)):
        if word[i] == checkWord[i]:
            checkWord[i] = 0
            hits.append(2)
        else:
            hits.append(0)
    for i in range(len(word[i])):
        if word[i] in checkWord:
            hits[i] = 1
    return hits

print(compare(guess))
print(answer)
