import csv
import random
import string
from PIL import Image, ImageShow

#Function Definition
def createLetterImg(color, letter):
    letterImg = Image.open("Images/Tiles/Wordle {0}/{1}.jpeg".format(color, letter))
    letterImg = letterImg.resize((77,76))
    return letterImg

def addLetter(column, row, letterImg):
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
        guess = input()
        if guess ==  '.' or guess == ',':
            return guess
        elif len(guess) != 1 or guess not in letters_list:
            print("Word Error")
        else:
            end = True
    return guess

def returnGuess(hits, guess, cycle):
    for i in range(len(hits)):
        if hits[i] == 2:
            letterImg = createLetterImg("Green", guess[i].upper())

        elif hits[i] == 1:
            letterImg = createLetterImg("Yellow", guess[i].upper())
        else:
            letterImg = createLetterImg("Gray", guess[i].upper())
        img = addLetter(i + 1, cycle + 1, letterImg)
    ImageShow.show(img)

def runRow(row):
    word = []
    while True:
        guess = getGuess()
        if len(word) == 5 and ''.join(word) in guess_words_list and guess == '.':
            return ''.join(word)
        elif guess in letters_list and len(word) < 5:
            guess = guess.upper()
            word.append(guess.lower())
            letterImg = createLetterImg("Gray", guess)
            img = addLetter(len(word), row + 1, letterImg)
        elif guess == ',' and len(word) > 0:
            word.pop()
            letterImg = Image.open("Images/Tiles/Wordle Blank/blank.jpeg")
            img = addLetter(len(word) + 1, row + 1, letterImg)
        ImageShow.show(img)

def wordleSetup():
    print("running")
    #Create the Blank Image
    global img
    img = Image.open("Images/WordleTemplate.jpeg")

    #Open the Word CSVs
    file = open("word_libraries/answer_words.csv")
    answer_words_csv = csv.reader(file)
    file = open("word_libraries/guess_words.csv")
    guess_words_csv = csv.reader(file)
    file = open("word_libraries/letters.csv")
    letters_csv = csv.reader(file)

    #Create the Word Lists
    global answer_words_list
    answer_words_list = []
    global guess_words_list
    guess_words_list = []
    global letters_list
    letters_list = []
    for row in answer_words_csv:
        word = str(row)[2:-2]
        answer_words_list.append(word)
        guess_words_list.append(word)
    for row in guess_words_csv:
        word = str(row)[2:-2]
        guess_words_list.append(word)
    for row in letters_csv:
        letter = str(row)[2:-2]
        letters_list.append(letter)

    #Determines the answer word
    global answer
    answer = answer_words_list[random.randrange(len(answer_words_list))]

def main():

    wordleSetup()

    #Runs the game, row by row
    for row in range(6):
        word = runRow(row).lower()
        print(answer)
        hits = compare(word)
        print(hits)
        returnGuess(hits, word, row)
        if checkWin(hits) == True:
            print("You got the wordle!")
            exit()
    print("You did not get the wordle! It was {0}".format(answer))
    exit()
if __name__ == "__main__":
    main()
