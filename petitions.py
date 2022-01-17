import pandas as pd
import os

import json
import requests

import urllib.parse

#DataFrame de Cartas.
    #Nombre
    #Mana Cost
    #Desc
    #God

imx_api_url = "https://api.x.immutable.com/v1"
imx_api_headers = {"Accept": "application/json"}

dataFrame = pd.DataFrame({'Name': pd.Series(dtype='str'),
                          'Mana_Cost': pd.Series(dtype='int'),
                          'Description': pd.Series(dtype='str'),
                          'Quantity': pd.Series(dtype='int'),
                          'GOD': pd.Series(dtype='str'),
                          'Price': pd.Series(dtype='float'),
                          'Set': pd.Series(dtype='str'),
                          'Tribe': pd.Series(dtype='str'),
                          'Attack': pd.Series(dtype='int'),
                          'Health': pd.Series(dtype='int'),
                          'Rarity': pd.Series(dtype='str')
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

#@Params: name - string
#Get list of cards in json format by name
def getCardList(name):
    print("Recopilando información de los primeros 200 resultados...")
    url = imx_api_url + "/assets/?page_size=200&sell_orders=true&buy_orders=true&collection=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c&name=" + name + "&order_by=sell-orders&status=imx"
    response = requests.request("GET", url, headers=imx_api_headers)
    input_dict = json.loads(response.text)
    cursor = input_dict['cursor']
    output_json = json.dumps(input_dict, indent=4)
    tokens_id_list = []
    for items in input_dict['result']:
        tokens_id_list.append(items['token_id'])
    while True:
        print("Recopilando información de los siguientes 200 resultados...")
        url_aux = "https://api.x.immutable.com/v1/assets/?page_size=200&sell_orders=true&buy_orders=true&collection=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c&name=" + name + "&order_by=sell-orders&status=imx&cursor=" + cursor

        response_aux = requests.request("GET", url_aux, headers=imx_api_headers)
        input_dict = json.loads(response_aux.text)

        if (input_dict['cursor']):
            cursor = input_dict['cursor']
        else:
            break

        for items in input_dict['result']:
            if (items['token_id']) in tokens_id_list:
                break
            tokens_id_list.append(items['token_id'])

        #output_dict = [x for x in input_dict['result'] if x['orders'] != {}]
        output_jsonaux = json.dumps(input_dict, indent=4)
        output_json += output_jsonaux

    return

#DEPRECATED
#Params: Name - str
#Get the proto code of a Card from its name.
def getProto(name):
    #.........
    return

#@Params: name, str, quantity, int, GuDeck, DataFrame
#Fill all the data of a card from it's name calling GODS / IMX API.
def getDataCard(name, quantity):
    url = imx_api_url + "/assets/?page_size=1&sell_orders=true&buy_orders=true&collection=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c&name=" + name + "&order_by=sell-orders&status=imx"
    response = requests.request("GET", url, headers=imx_api_headers)
    input_dict = json.loads(response.text)
    auxDF = []    # input_dict['result']
        #input_dict['result']['metadata']['name']
    # input_dict['cursor']
    #Effect empty are null
    efecto = ""
    try:
        if len(input_dict['result']) > 0:
            cartika = input_dict['result'][0]['metadata']
            print("[GetDataCard] Recopilando información de " + cartika['name'])
            efecto = cartika['effect']
            try:
                auxDF = [cartika['name'], cartika['mana'], efecto, quantity, cartika['god'], 0, cartika['set'], cartika['tribe'], cartika['attack'], cartika['health'], cartika['rarity']]
            except Exception as e:
                print("[GetDataCard] error ", e, input_dict['result'])
                cartika = input_dict['result'][0]['metadata']
                efecto = cartika['effect']
                auxDF = [cartika['name'], cartika['mana'], efecto, quantity, cartika['god'], 0, cartika['set'], 'nope', 0, 0, cartika['rarity']]
        else:
            print("[GetDataCard] No resultado", input_dict)

            cartika = False
        return auxDF
    except Exception as ex:
        print("[GetDataCard] A chuparla con", name, ex, input_dict)
        return auxDF

#@Params: name, str, quantity, int, GuDeck, DataFrame
#Fill all the data of a card from it's name calling GODS / IMX API.
def getDataCards(name, quantity):
    print("Recopilando información de los primeros 200 resultados...")
    url = imx_api_url + "/assets/?page_size=" + quantity + "&sell_orders=true&buy_orders=true&collection=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c&name=" + name + "&order_by=sell-orders&status=imx"
    response = requests.request("GET", url, headers=imx_api_headers)
    input_dict = json.loads(response.text)
    cursor = input_dict['cursor']
    output_json = json.dumps(input_dict, indent=4)
    tokens_id_list = []
    for items in input_dict['result']:
        tokens_id_list.append(items['token_id'])


    # input_dict['result']
        #input_dict['result']['metadata']['name']
    # input_dict['cursor']

    #print("GOD: ",input_dict['result']['metadata']['god'])
    #print("MANA: ",input_dict['result']['metadata']['mana'])
    #print("DESCRIPCION: ",input_dict['result']['metadata']['effect'])
    #print("CALIDAD: ",input_dict['result']['metadata']['quality'])
    #print("RAREZA: ",input_dict['result']['metadata']['rarity'])
    #print("SET: ", input_dict['result']['metadata']['set'])

    if(quantity>199):
        while True:
            print("Recopilando información de los siguientes 200 resultados...")
            url_aux = "https://api.x.immutable.com/v1/assets/?page_size=200&sell_orders=true&buy_orders=true&collection=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c&name=" + name + "&order_by=sell-orders&status=imx&cursor=" + cursor

            response_aux = requests.request("GET", url_aux, headers=imx_api_headers)
            input_dict = json.loads(response_aux.text)

            if (input_dict['cursor']):
                cursor = input_dict['cursor']
            else:
                break

            for items in input_dict['result']:
                if (items['token_id']) in tokens_id_list:
                    break
                tokens_id_list.append(items['token_id'])

            # output_dict = [x for x in input_dict['result'] if x['orders'] != {}]
            output_jsonaux = json.dumps(input_dict, indent=4)
            output_json += output_jsonaux
            ############################

    return

#@Params: name - string
#Get Price of a Card from
def getCardsListed(name):
    print("Recopilando información de los primeros 200 resultados...")
    url = imx_api_url + "/assets/?page_size=200&sell_orders=true&buy_orders=true&collection=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c&name=" + name + "&order_by=sell-orders&status=imx"
    response = requests.request("GET", url, headers=imx_api_headers)
    input_dict = json.loads(response.text)
    cursor = input_dict['cursor']
    output_dict = [x for x in input_dict['result'] if x['orders'] != {}]
    output_json = json.dumps(output_dict, indent=4)
    tokens_id_list = []
    for items in input_dict['result']:
        tokens_id_list.append(items['token_id'])
    while True:
        print("Recopilando información de los siguientes 200 resultados...")
        url_aux = "https://api.x.immutable.com/v1/assets/?page_size=200&sell_orders=true&buy_orders=true&collection=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c&name=" + name + "&order_by=sell-orders&status=imx&cursor=" + cursor

        response_aux = requests.request("GET", url_aux, headers=imx_api_headers)
        input_dict = json.loads(response_aux.text)

        if (input_dict['cursor']):
            cursor = input_dict['cursor']
        else:
            break

        for items in input_dict['result']:
            if (items['token_id']) in tokens_id_list:
                break
            tokens_id_list.append(items['token_id'])

        output_dict = [x for x in input_dict['result'] if x['orders'] != {}]
        output_jsonaux = json.dumps(output_dict, indent=4)
        output_json += output_jsonaux

    return

#@Params: proto - int, days - int
#Get the number of cards sold in the last defined days.
def getSalesVolume(proto, days):
    #.........
    return

#@Params:   direction           - str
#           include_fees        - str(true/false)
#           order_by            - str               =buy_quantity
#           page_size           - int               =200
#           sell_token_address  - str               =0xacb3c6a43d15b907e8433077b6d38ae40936fe2c
#           sell_token_type     - str               =ERC721
#           status              - str               =active
#           sell_token_name     - str               =Moonbeam
#           sell_metadata       - json              =%7B%22quality%22%3A%5B%22Diamond%22%5D%7D&buy_token_type=ET

#Get others from a card sorted by buying quantity
#direction ---------(str) (default) "asc" / "dsc"
#include_fees ------(str) (default) "true" / "false"
#order_by ----------(str) (default) "buy_quantity" /  /  /  /
#page_size ---------(str) (default) 200
#sell_token_address-(str) (default) "0xacb3c6a43d15b907e8433077b6d38ae40936fe2c" -> coleccion GU
#sell_token_type ---(str) (default) "ERC721"
#status ------------(str) (default) "active"
#sell_token_name ---(str) (default) "Moonbeam"
#sell_metadata -----(str) (default) None / {
#                 "name": "BeastMode by XCOPY - Core Crypto 2021 (146/150)",
#                 "uuid": "4a8dea3f-128d-4774-a04e-ca7176af09b6",
#                 "cardId": 22892,
#                 "signed": false,
#                 "cache_for": 600,
#                 "image_url": "https://cdn2.kolectiv.gg/card/render/34/117/402x670/4a8dea3f-128d-4774-a04e-ca7176af09b6.png",
#                 "mintNumber": 146,
#                 "totalMinted": 150,
#                 "external_url": "https://kolectiv.gg/asset/4a8dea3f-128d-4774-a04e-ca7176af09b6",
#                 "cardTemplateId": 117
#             },
#buy_token_type ----(str) (default) "ETH" / "ERC20" (Gods) / "ERC721"
# ToDo: investigate posibilitys: - order_by, sell_token_type, buy_token_type,
#     - Check the possibility of receive X orders and get the price by the mean of all of them
def getOrders(direction= "asc",
              include_fees= "true",
              order_by= "buy_quantity",
              page_size= "1",
              sell_token_address= "0xacb3c6a43d15b907e8433077b6d38ae40936fe2c",
              sell_token_type= "ERC721",
              status= "active",
              sell_token_name= "Moonbeam",
              sell_metadata= "",
              buy_token_address= "0xccc8cb5229b0ac8069c51fd58367fd1e622afd97"):

    sell_metadata = urllib.parse.quote('{"quality":["Meteorite"]}')

    url = "https://api.x.immutable.com/v1/orders?" \
          "direction=" + direction+\
          "&include_fees=" + include_fees+ \
          "&order_by=" + order_by+ \
          "&page_size=" + page_size+ \
          "&sell_token_address=" + sell_token_address+ \
          "&sell_token_type=" + sell_token_type+ \
          "&status=" + status+ \
          "&sell_token_name=" + sell_token_name+ \
          "&sell_metadata=" + sell_metadata+ \
          "&buy_token_address=" + buy_token_address

    response = requests.get(url)
    data = response.json()
    data = data["result"]
    output_jsonaux = json.dumps(data, indent=4)
    GODS_price = 0

    print(output_jsonaux)
    if data != []:
        print("Data lleno")
        print(data)
        GODS_price = float(data[0]["buy"]["data"]["quantity"])/pow(10,float(data[0]["buy"]["data"]["decimals"]))
    else:
        print("DataVacio en GetOrders")

    buy_token_address = "ETH"
    url = "https://api.x.immutable.com/v1/orders?" \
          "direction=" + direction + \
          "&include_fees=" + include_fees + \
          "&order_by=" + order_by + \
          "&page_size=" + page_size + \
          "&sell_token_address=" + sell_token_address + \
          "&sell_token_type=" + sell_token_type + \
          "&status=" + status + \
          "&sell_token_name=" + sell_token_name + \
          "&sell_metadata=" + sell_metadata + \
          "&buy_token_type=" + buy_token_address

    response = requests.get(url)
    data = response.json()
    data = data["result"]
    ETH_price = 0
    if len(data) > 0:
        ETH_price = float(data[0]["buy"]["data"]["quantity"])/pow(10,float(data[0]["buy"]["data"]["decimals"]))
    #print(data[0]["buy"]["data"]["quantity"])


    return GODS_price, ETH_price





#_________________
getOrders()

data = extractData('ole.csv')
data.dropna(subset=['Name'],inplace=True)

ojalases = []
count = 0
for item in data.itertuples():
    count+=1
    if len(item) > 0:
        print("____________")
        asd = getDataCard(item.Name, item.Cantidad)
        priceG, priceEth = getOrders(sell_token_name = item.Name)
        print("Nombre: " + item.Name)
        print("Price ETh: " + str(priceEth) + "  Price GODS: "+  str(priceG))
        print("Longitud asd: ", len(asd), )
        print("Contenido asd: ", asd)

        asd.append(priceG)
        asd.append(priceEth)
        if type(asd) != None and len(asd)>2:
          ojalases.append(asd)
          print(ojalases)
        print("Long ojalases: ", len(ojalases))
    print("____________")

yaves = pd.DataFrame(ojalases)
pd.DataFrame(yaves).to_csv('final.csv')
print("=============")
print(yaves)
print("sefini")
print(count)