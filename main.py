#Import Libraries
import discord
import tracemalloc
import csv
import random
import string
import time
import io
import asyncio
import nest_asyncio
import IPython
import math
from discord.ui import Button, View
from discord.ext import commands
from PIL import Image

#Infrastructure
with open('token.txt') as tkn:
    token = tkn.readlines()[0]
bot = commands.Bot(command_prefix = '=')
nest_asyncio.apply()

#Commands
@bot.command()
async def learn(ctx):
    await ctx.send("Wordle is a very simply game to play.", file = discord.File("Images/Tutorial.jpg"))

@bot.command()
async def wordle(ctx):

    #Create the thread the game is played in
    threadName = "{0}'s Wordle Game".format(str(ctx.author)[:-5])
    #thread = 0
    try: thread = await ctx.message.channel.create_thread(name = threadName, message = ctx.message, auto_archive_duration = 60)
    except: await ctx.send("You cannot initiate a game of Wordle outside of a channel!")
    await thread.send(content = "Test Message")

    #Create the Blank Image and saves to memory
    img = Image.open("Images/WordleTemplate.jpeg")
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

    #Determines the answer word
    answer = answer_words_list[random.randrange(len(answer_words_list))]
    print(answer)

    #Send initial message
    file = discord.File(fp = mem, filename = 'blank.png')
    imgMsg = await thread.send("{0}'s Wordle Game:".format(str(ctx.author)[:-5]))

    #Function Definition
    def runAsync(coroutine):
        task = asyncio.create_task(coroutine)
        asyncio.get_running_loop().run_until_complete(task)
        return task.result()

    async def editMsgImg(newImg):
        mem = io.BytesIO()
        newImg.save(mem, format='PNG')
        mem.seek(0)
        file = discord.File(fp = mem, filename = 'blank.png')
        await imgMsg.edit(file = file)
        return True

    async def shutdownThread(secs):
        time.sleep(secs)
        await thread.delete()

    #Add the image to the initial message
    await editMsgImg(img)

    #Create Buttons
    x = 26
    buttons = [0] * 29
    buttonMsgs = []
    for i in range(5):
        view = View()
        for i in range(5):
            buttons[x - 26] = Button(label = letters_list[x], style = discord.ButtonStyle.gray)
            view.add_item(buttons[x - 26])
            x += 1
        buttonMsg = await thread.send(view = view)
        buttonMsgs.append(buttonMsg)
    #Print last line
    view = View()
    buttons[25] = Button(label = "Z", style = discord.ButtonStyle.gray)
    view.add_item(buttons[25])
    buttons[26] = Button(label = "Delete", style = discord.ButtonStyle.gray)
    view.add_item(buttons[26])
    buttons[27] = Button(label = "Enter", style = discord.ButtonStyle.gray)
    view.add_item(buttons[27])
    buttons[28] = Button(label = "Quit", style = discord.ButtonStyle.gray)
    view.add_item(buttons[28])
    buttonMsg = await thread.send(view = view)
    buttonMsgs.append(buttonMsg)

    #Create  dictionary containing letters and their status
    letterStatus = [-1] * 29

    async def editButton(buttonNum, hitStat):
        if letterStatus[buttonNum] < hitStat:
            letterStatus[buttonNum] = hitStat
            buttonRow = math.trunc((buttonNum / 5))
            rowLetterStatus = []
            view = View.from_message(buttonMsgs[buttonRow])
            for i in range(len(view.children)): #glitch caused with letter z because adding quit button increased length of view.children
                rowLetterStatus.append(letterStatus[(buttonRow * 5) + i])
            for i in range(len(rowLetterStatus)):
                if rowLetterStatus[i] == 2:
                    view.children[i].style = discord.ButtonStyle.green
                elif rowLetterStatus[i] == 1:
                    view.children[i].style = discord.ButtonStyle.blurple
                elif rowLetterStatus[i] == 0:
                    view.children[i].style = discord.ButtonStyle.red
                view.children[i].callback = buttonsCallbacks[((buttonRow) * 5) + i] #Binds the new buttons to their callback
            await buttonMsgs[buttonRow].edit(view = view)
            return True
        else: pass


    #Create Wordle Class
    class wordleClass(object):
        def __init__(self, input):
            self.input = input
            self.input.bind_to(self.advanceWordle)
            self.gameRow = 1
            self.img = img
            self.word = []
            self.game = True

        def advanceWordle(self, buttonNum):
            if self.game == True:
                global buttonID
                if buttonNum < 26:
                    buttonID = letters_list[buttonNum].upper()
                elif buttonNum == 26:
                    buttonID = "Delete"
                elif buttonNum == 27:
                    buttonID = "Enter"
                elif buttonNum == 28:
                    buttonID = "Quit"
                if len(self.word) == 5 and ''.join(self.word) in guess_words_list and buttonID == 'Enter':
                    checkWord = ''.join(self.word)
                    hits = wordle.compare(checkWord)
                    for i in range(len(hits)):
                        runAsync(editButton(letters_list.index(self.word[i]), hits[i]))
                    self.word = []
                    if 0 not in hits and 1 not in hits: #Win Condition
                        runAsync(imgMsg.edit(content = "Congratulations: You got the Wordle in {0} attempts!".format(self.gameRow)))
                        runAsync(shutdownThread(15))
                        thread.send("This thread will delete in 15 seconds! Make sure to save your wordle!")
                        self.game = False
                    wordle.returnGuess(hits, checkWord, self.gameRow)
                    self.gameRow += 1
                    if self.gameRow == 7:
                        runAsync(imgMsg.edit(content = "You did not get the Wordle. It was {0}".format(answer.upper())))
                        self.game = False
                        runAsync(shutdownThread(5))
                        return
                elif buttonID in letters_list and len(self.word) < 5:
                    self.word.append(buttonID.lower())
                    letterImg = wordle.createLetterImg("Gray", buttonID)
                    self.img= wordle.addLetter(len(self.word), self.gameRow, letterImg)
                elif buttonID == 'Delete' and len(self.word) > 0:
                    self.word.pop()
                    letterImg = Image.open("Images/Tiles/Wordle Blank/blank.jpeg")
                    self.img= wordle.addLetter(len(self.word) + 1, self.gameRow, letterImg)
                elif buttonID == 'Quit':
                    runAsync(imgMsg.edit(content = "You gave up on your Wordle! It was {0}".format(answer.upper())))
                    self.game = False
                    runAsync(shutdownThread(5))
                    return
                runAsync(editMsgImg(self.img))
            else: pass

        def createLetterImg(self, color, letter):
            letterImg = Image.open("Images/Tiles/Wordle {0}/{1}.jpeg".format(color, letter))
            letterImg = letterImg.resize((77,76))
            return letterImg

        def addLetter(self, column, row, letterImg):
            x = (column - 1) * 87 + 38
            y = (row - 1) * 87 + 43 + round((row * 0.55))
            self.img.paste(letterImg, (x,y))
            return img

        def compare(self, word):
            checkWord = list(answer)
            guess = list(word)
            hits = []
            for i in range(len(word)):
                if guess[i] == checkWord[i]:
                    guess[i] = 0
                    checkWord[i] = 0
                    hits.append(2)
                else:
                    hits.append(0)
            for i in range(len(word)):
                if hits[i] != 2 and guess[i] in checkWord:
                    hits[i] = 1
                    checkWord[checkWord.index(guess[i])] = 0
                    guess[i] = 0
            return hits

        def returnGuess(self, hits, guess, cycle):
            for i in range(len(hits)):
                if hits[i] == 2:
                    letterImg = wordle.createLetterImg("Green", guess[i].upper())

                elif hits[i] == 1:
                    letterImg = wordle.createLetterImg("Yellow", guess[i].upper())
                else:
                    letterImg = wordle.createLetterImg("Gray", guess[i].upper())
                self.img= wordle.addLetter(i + 1, cycle, letterImg)

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

    #Create Button Callbacks
    buttonsCallbacks = [0] * 29
    for i in range(len(buttons)):
        async def callback(interaction, i = i):
            if interaction.user.id == ctx.message.author.id:
                input.buttonNum = i
        buttonsCallbacks[i] = callback
        buttons[i].callback = buttonsCallbacks[i]

def main():
    tracemalloc.start()
    bot.run(token)

if __name__ == "__main__":
    main()
