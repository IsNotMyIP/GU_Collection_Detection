import cv2
import numpy as np
import os
import pytesseract
import time
import re
import pandas as pd
from mss import mss


pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
TESSDATA_PREFIX = 'C:/Program Files/Tesseract-OCR'


class Collection:
    def __init__(self):
        self.cards = []
        self.len = len(self.cards)

    def append(self, padentro):
        self.cards.append(padentro)
        self.len = len(self.cards)

    def areas(self):
        for card in self.cards:
            print(card.area())

    def cleanAreas(self, limit):
        aux = []
        for i in range(0, len(self.cards)):
            if self.cards[i].area() > limit:
                aux.append(self.cards[i])
        self.cards = aux
        self.len = len(self.cards)

    def drawCollection(self, img):
        for card in self.cards:
            card.draw(img)

    def drawNames(self, img):
        for card in self.cards:
            card.drawName(img)

    def getNamesCards(self, img):
        for card in self.cards:
            card.drawName(img)
            card.getName(img)

    def printNames(self):
        for card in self.cards:
            print(card.name, "  ", card.quantity)

    def getInfo(self):
        empty = 0
        for card in self.cards:
            if card.name == '':
                empty += 1
        print("__________________")
        print("Info")
        print("Cartas almacenadas: " + str(self.len))

        print("Cartas sin nombre: " + str(empty))
        print("La lista de nombre de cartas conseguidas es: ")
        self.printNames()
        self.closing()

    def closing(self):
        aux = []
        for card in self.cards:
            aux.append([card.name, card.quantity])
        export = np.asarray(aux)
        pd.DataFrame(export).to_csv('ole.csv')

class Card:
    def __init__(self, x, y, w, h):
        self.width, self.height = w, h  # Width and height of card
        self.x, self.y = x, y  # Array of coordinates
        self.name = ''
        self.name_width = 120
        self.name_height = 30
        self.name_x = int(x + (self.width / 2) - (self.name_width / 2))
        self.name_y = int(y + ((self.height * 0.632) - (self.name_height / 2)))

        self.quantity = 1
        self.q_x = int(self.x-5 +(self.width/2))
        self.q_y = int(self.y+self.height)
        self.q_w, self.q_h = 20, 25

    def area(self):
        return self.width * self.height

    def draw(self, img):
        cv2.rectangle(img, (self.x, self.y), (self.x + self.width, self.y + self.height), (0, 255, 0), 2)

    def drawName(self, img):
        # cv2.putText(img, 'hola', (self.name_x, self.name_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1,2)
        cv2.rectangle(img, (self.name_x, self.name_y), (self.name_x + self.name_width, self.name_y + self.name_height),
                      (0, 0, 255), 1)
        cv2.rectangle(img, (self.q_x, self.q_y), (self.q_x + self.q_w, self.q_y + self.q_h),
                      (255, 0, 0), 1)

    def getName(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Performing OTSU threshold

        ret, thresh1 = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
        ret, thresh2 = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

        cropped = thresh1[self.name_y:self.name_y + self.name_height, self.name_x:self.name_x + self.name_width]
        numed = thresh2[self.q_y:self.q_y+self.q_h, self.q_x:self.q_x+self.q_w]
        self.name = pytesseract.image_to_string(cropped, lang='eng')

        self.quantity = pytesseract.image_to_string(numed, config="--psm 6 digits")


def dummyData():
    path = os.path.dirname(os.path.abspath(__file__))
    image = cv2.imread(path + '/Assets/Screen2.PNG')
    return image


def analyzeImage(img, deck, pic):
    bluried = cv2.GaussianBlur(img, (7, 7), 0)
    # b, g, r = cv2.split(bluried)
    bluried[:, :, 0] = 0
    bluried[:, :, 1] = 0
    gris = cv2.cvtColor(bluried, cv2.COLOR_BGR2GRAY)
    th, threshed3 = cv2.threshold(gris, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(threshed3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    GUS = Collection()
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        aux = Card(x, y, w, h)
        if aux.area() > 20000:
            helpo = Card(x, y, w, h)
            if pic:
                if re.match(r"\w+", str(helpo.getName(img))):
                    GUS.append(helpo)
                    deck.append(helpo)

        # if aux.area() > 20000:
        #     deck.append(Card(x,y,w,h))
        #     GUS.append(Card(x,y,w,h))

    return GUS

if __name__ == '__main__':

    bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

    sct = mss()

    nowTime = time.time()
    checkerTime = time.time()
    fps = 0
    showFPS = 1
    checkeatorPS = 2

    Gudeck = Collection()
    elbueno = Collection()
    checko = False

    while True:
        sct_img = sct.grab(bounding_box)
        screen = np.array(sct_img, 'uint8')

        ojo = analyzeImage(screen, Gudeck, checko)
        ojo.len = len(ojo.cards)
        ojo.drawCollection(screen)
        ojo.drawNames(screen)

        cv2.imshow("hoho", screen)

        # ojo.printNames()
        elbueno.cards += ojo.cards
        elbueno.len = len(elbueno.cards)

        fps += 1
        if (time.time() - nowTime) > showFPS:
            print("FPS: ", fps / (time.time() - nowTime))
            fps = 0
            if checko:
                checko = False
            print("Long aux: ", ojo.len)
            nowTime = time.time()

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            elbueno.getInfo()
            break
        elif (cv2.waitKey(1) & 0xFF) == ord('l'):
            print("fotiko")
            checko = True