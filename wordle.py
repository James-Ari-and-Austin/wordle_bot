import csv
import random
import string
from PIL import Image, ImageShow

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
answer = answer_words_list[random.randrange(len(answer_words_list))].upper()

#Function Definition
def createLetterImg(color, letter):
    letterImg = Image.open("Images/Tiles/Wordle {0}/{1}.jpeg".format(color, letter))
    letterImg = letterImg.resize((77,76))
    return letterImg

def addLetter(column, row, img, letterImg):
    x = (column - 1) * 87 + 38
    y = (row - 1) * 87 + 43 + round((row * 0.55))
    img.paste(letterImg, (x,y))
    return img

def compare(word):
    checkWord = list(answer)
    guess = list(word)
    hits = []
    for i in range(len(word)):
        if guess[i] == checkWord[i]:
            guess[i] = 0
            hits.append(2)
        else:
            hits.append(0)
    for i in range(len(word)):
        if guess[i] in checkWord:
            hits[i] = 1
            guess[i] = 0
    return hits

def checkWin(hits):
    if 0 in hits or 1 in hits:
        return False
    else:
        return True

def getGuess():
    end = False
    while end == False:
        guess = input().upper()
        if len(guess) != 5 or guess.lower() not in guess_words_list:
            print("Word Error")
        else:
            end = True
    return guess

def returnGuess(hits, guess, cycle, img):
    for i in range(len(hits)):
        if hits[i] == 2:
            letterImg = createLetterImg("Green", guess[i])

        elif hits[i] == 1:
            letterImg = createLetterImg("Yellow", guess[i])
        else:
            letterImg = createLetterImg("Gray", guess[i])
        img = addLetter(i + 1, cycle + 1, img, letterImg)
    ImageShow.show(img)


def main():
    img = Image.open("Images/WordleTemplate.jpeg")
    for cycle in range(5):
        guess = getGuess()
        hits = compare(guess)
        returnGuess(hits, guess, cycle, img)
        if checkWin(hits) == True:
            print("You got the wordle!")
            exit()
    print("You did not get the wordle! It was {0}".format(answer))
    exit()
main()
