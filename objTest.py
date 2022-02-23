class inputClass(object):
    def __init__(self):
        self._buttonNum = 0
        self._observers = []

    @property
    def buttonNum(self):
        return self._buttonNum

    @buttonNum.setter
    def buttonNum(self, value):
        self._buttonNum = value
        for callback in self._observers:
            print('announcing change')
            callback(self._buttonNum)
    def bind_to(self, callback):
        self._observers.append(callback)
        print('bound')
class WordleClass(object):
    def __init__(self, input):
        self.input = input
        self.input.bind_to(self.advanceWordle)
        self.variable = self.input._buttonNum
    def advanceWordle(self, buttonNum):
        #print(buttonNum)
        print("wordle advanced")
if __name__ == '__main__':
    data = inputClass()
    wordle = WordleClass(data)
    print(wordle.variable)
    data.buttonNum = 1.0
    print(wordle.variable)
