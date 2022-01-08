import pandas as pd
import os
import requests

import json
import requests

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
    try:
        if len(input_dict['result']) > 0:
            cartika = input_dict['result'][0]['metadata']
            print("Recopilando información de " + cartika['name'])
            try:
                auxDF = [cartika['name'], cartika['mana'], cartika['effect'], quantity, cartika['god'], 0, cartika['set'], cartika['tribe'], cartika['attack'], cartika['health'], cartika['rarity']]
            except:
                print("error")
                auxDF =[]
        else:
            cartika = False
        return auxDF
    except:
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

#_________________

data = extractData('ole.csv')
data.dropna(subset=['Name'],inplace=True)
print(data.sort_values(by="Cantidad",ascending=False).head(20))
print(data['Cantidad'].sum())
print(data.columns)


ojalases = []
for item in data.itertuples():

    asd = getDataCard(item.Name, item.Quantity)
    print(asd)

    if type(asd) != None:
        ojalases.append(asd)
        print(ojalases)
    print("____________")
    print(ojalases)


print("sefini")