import pandas as pd
import os
import requests

#DataFrame de Cartas.
    #Nombre
    #Mana Cost
    #Desc
    #God

dataFrame = pd.DataFrame({'Name': pd.Series(dtype='str'),
                          'Mana_Cost': pd.Series(dtype='int'),
                          'Description': pd.Series(dtype='str'),
                          'Quantity': pd.Series(dtype='int'),
                          'GOD': pd.Series(dtype='str'),
                          'Proto_Code': pd.Series(dtype='int'),
                          'Price': pd.Series(dtype='float')
                        })


#Params: fileName - str
#Extract data from the CSV file.
def extractData(fileName):
    path = os.path.dirname(os.path.abspath(__file__))
    data = pd.read_csv(path +'\\' + fileName, delimiter=",", header=0, names=['Nombre Carta', 'Cantidad'], encoding='windows-1252')
    formatted = dataFrame
    formatted['Name'] = data['Nombre Carta']
    formatted['Cantidad'] = data['Cantidad']
    return formatted

#Params: Name - str
#Get the proto code of a Card from its name.
def getProto(name):
    #.........
    return

#@Params: name, str, quantity, int, GuDeck, DataFrame
#Fill all the data of a card from it's name calling GODS / IMX API.
def getDataCard(name, quantity):
    #data = dataframe nuestro
    #............
    return

#@Params: name - string
#Get Price of a Card from
def getPrecio(proto):
     #...............
     return

#@Params: proto - int, days - int
#Get the number of cards sold in the last defined days.
def getSalesVolume(proto, days):
    #.........
    return

#_________________

data = extractData('ole.csv')
data.dropna(subset=['Name'],inplace=True)
print(data.sort_values(by="Cantidad",ascending=False).head(20))
print(data['Cantidad'].sum())