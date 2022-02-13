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
    for i in range(len(word)):
        if word[i] in checkWord:
            hits[i] = 1
    return hits

def checkWin(hits):
    if 0 in hits or 1 in hits:
        return False
    else:
        return True

def getGuess():
    end = False
    while end == False:
        guess = input()
        if len(guess) != 5 or guess not in guess_words_list:
            print("Word Error")
        else:
            end = True
    return guess

def main():
    guess = getGuess()
    print(compare(guess))
    print(answer)

main()
