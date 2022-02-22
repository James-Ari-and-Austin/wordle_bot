from PIL import Image, ImageShow, ImageFont

def createLetterImg(color, letter):
    letterImg = Image.open("Images/Tiles/Wordle {0}/{1}.jpeg".format(color, letter))
    letterImg = letterImg.resize((77,76))
    return letterImg

def addLetter(column, row, img, letterImg):
    x = (column - 1) * 87 + 38
    y = (row - 1) * 87 + 43 + round((row * 0.55))
    img.paste(letterImg, (x,y))
    return img

def main():
    img = Image.open("Images/WordleTemplate.jpeg")
    letterImg = createLetterImg('Green', 'b')
    img = addLetter(4, 5, img, letterImg)
    ImageShow.show(img)

if __name__ == '__main__':
    main()
