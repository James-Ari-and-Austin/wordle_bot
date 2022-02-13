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
    hits = []
    for i in range(len(word)):
        j = 0
        print("cycle: {0} {1} {2}".format(i, word[i], answer[i] ))
        if word[i] == answer[i]:
            j = j + 1
            print("hit")
        if word[i] in answer:
            j = j + 1
        hits.append(j)
    return hits

print(compare(guess))
print(answer)
print(guess)
