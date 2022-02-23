#Import Libraries
import discord
import tracemalloc
import csv
import random
import string
import io
from discord.ui import Button, View
from discord.ext import commands
from PIL import Image, ImageShow

#Infrastructure
token = "OTQyMjE3ODg2NDAxOTU3ODk4.YghSyQ.OQBVr3_pbyA-13bNdxVu8auVBzs"
bot = commands.Bot(command_prefix = '=')

#Commands
@bot.command()
async def wordle(ctx):

    #Create the Blank Image and saves to memory
    global img
    img = Image.open("Images/WordleTemplate.jpeg")
    global mem
    mem = io.BytesIO()
    img.save(mem, format='PNG')
    mem.seek(0)

    #Open the Word CSVs
    file = open("word_libraries/answer_words.csv")
    answer_words_csv = csv.reader(file)
    file = open("word_libraries/guess_words.csv")
    guess_words_csv = csv.reader(file)
    file = open("word_libraries/letters.csv")
    letters_csv = csv.reader(file)

    #Create the Lists
    global answer_words_list
    answer_words_list = []
    global guess_words_list
    guess_words_list = []
    global letters_list
    letters_list = []
    for row in answer_words_csv:
        tempWord = str(row)[2:-2]
        answer_words_list.append(tempWord)
        guess_words_list.append(tempWord)
    for row in guess_words_csv:
        tempWord = str(row)[2:-2]
        guess_words_list.append(tempWord)
    for row in letters_csv:
        letter = str(row)[2:-2]
        letters_list.append(letter)
    global word
    word = []

    #Determines the answer word
    global answer
    answer = answer_words_list[random.randrange(len(answer_words_list))]

    #Create Wordle Class
    class wordleClass(object):
        def __init__(self, input):
            self.input = input
            self.input.bind_to(self.advanceWordle)
            self.gameRow = 1

        def advanceWordle(self, buttonNum):
            global buttonID
            if buttonNum < 26:
                buttonID = letters_list[buttonNum].upper()
            elif buttonNum == 26:
                buttonID = "Del"
            elif buttonNum == 27:
                buttonID = "Enter"
            print("ButtonID = {0}".format(buttonID))
            if len(word) == 5 and ''.join(word) in guess_words_list and buttonID == 'Enter':
                checkWord = ''.join(word)
                print(checkWord)
                self.gameRow += 1
            elif buttonID in letters_list and len(word) < 5:
                word.append(buttonID.lower())
                letterImg = wordle.createLetterImg("Gray", buttonID)

                img = wordle.addLetter(len(word), self.gameRow, letterImg)
            elif buttonID == 'Del' and len(word) > 0:
                word.pop()
                letterImg = Image.open("Images/Tiles/Wordle Blank/blank.jpeg")
                img = wordle.addLetter(len(word) + 1, self.gameRow + 1, letterImg)
            print(''.join(word))
            ImageShow.show(img)

        def createLetterImg(self, color, letter):
            letterImg = Image.open("Images/Tiles/Wordle {0}/{1}.jpeg".format(color, letter))
            letterImg = letterImg.resize((77,76))
            return letterImg

        def addLetter(self, column, row, letterImg):
            x = (column - 1) * 87 + 38
            y = (row - 1) * 87 + 43 + round((row * 0.55))
            img.paste(letterImg, (x,y))
            return img

        def compare(self, word):
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

        def checkWin(self, hits):
            if 0 in hits or 1 in hits:
                return False
            else:
                return True

        #def getGuess(self):
            #end = False
            #while end == False:
                #guess = input()
                #if guess ==  '.' or guess == ',':
                    #return guess
                #elif len(guess) != 1 or guess not in letters_list:
                    #print("Word Error")
                #else:
                    #end = True
            #return guess

        def returnGuess(self, hits, guess, cycle):
            for i in range(len(hits)):
                if hits[i] == 2:
                    letterImg = createLetterImg("Green", guess[i].upper())

                elif hits[i] == 1:
                    letterImg = createLetterImg("Yellow", guess[i].upper())
                else:
                    letterImg = createLetterImg("Gray", guess[i].upper())
                img = addLetter(i + 1, cycle + 1, letterImg)
            ImageShow.show(img)

        def runRow(self, row, word, letter):
                guess = letter
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

    #Create input Class
    class inputClass(object): #This runs when an object is initialized with this class

        def __init__(self):
            self._buttonNum = 0
            self._observers = [] #This is a list of all the callbacks that are called when this object is updated
        @property #A property is something you can reference in order to get the variable everything is going to subscribe to I think

        def buttonNum(self):
            return self._buttonNum
        @buttonNum.setter #This calls the functions in _observers for the earlier defined property.

        def buttonNum(self, value):
            self._buttonNum = value
            for callback in self._observers:
                callback(self._buttonNum)

        def bind_to(self, callback): #This is a function that objects can call to bind to this one.
            self._observers.append(callback) #They give it a callback to run and this object runs it in the setter on updates.

    #Create Objects based on the classes
    input = inputClass()
    wordle = wordleClass(input)


    #Send initial Message
    file = discord.File(fp = mem, filename = 'blank.png')
    await ctx.send("{0}'s Wordle Game:".format(str(ctx.author)[:-5]))
    imgMsg = await ctx.send(file = file)

    #Create Buttons
    x = 26
    buttons = [0] * 28
    for i in range(5):
        view = View()
        for i in range(5):
            buttons[x - 26] = Button(label = letters_list[x], style = discord.ButtonStyle.green)
            view.add_item(buttons[x - 26])
            x += 1
        await ctx.send(view = view)
    #Print last line
    view = View()
    buttons[25] = Button(label = "Z", style = discord.ButtonStyle.green)
    view.add_item(buttons[25])
    buttons[26] = Button(label = "Del", style = discord.ButtonStyle.grey)
    view.add_item(buttons[26])
    buttons[27] = Button(label = "Enter", style = discord.ButtonStyle.grey)
    view.add_item(buttons[27])
    await ctx.send(view = view)

    #Create Button Callbacks
    buttonsCallbacks = [0] * 28
    for i in range(len(buttons)):
        async def callback(interaction, i = i):
            input.buttonNum = i
        buttonsCallbacks[i] = callback
        buttons[i].callback = buttonsCallbacks[i]

def main():
    tracemalloc.start()
    bot.run(token)

if __name__ == "__main__":
    main()
