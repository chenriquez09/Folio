from urllib import request
import requests
import json
from datetime import datetime, date, timedelta
import pandas as pd

def token():
    pathPattern = "authn/login"
    try:
        u=okapi_user
        p=okapy_password
        pathPattern=pathPattern
        userpass={
                  "username":u,
                  "password":p
                 }
        okapi_headers = {"x-okapi-tenant": OKAPY_TENANT,"content-type": "application/json", "accept": "application/json"}
        path = pathPattern
        url = OKAPY_URL + path
        req = requests.post(url, json=userpass, headers=okapi_headers,timeout=10)
        token= req.headers['x-okapi-token']
        return(token)
    except ValueError:
        print("General Error on Post:"+req.text+"\nError Number: "+req.status_code)
#----------------------------Fin obtención del token-------------------------

def location(barcode, option):
    path_item = f"item-storage/items?query=barcode={barcode}"
    url_item = OKAPY_URL + path_item
    okapi_headers = {"x-okapi-token": OKAPY_TOKEN,"x-okapi-tenant": OKAPY_TENANT,"content-type": "application/json"}
    req_item = requests.get(url_item, headers=okapi_headers, timeout=40)
    json_str_item = json.loads(req_item.text)  
    ids =[]
    for dato_item in json_str_item['items']:
        holdingId = dato_item['holdingsRecordId']
        path_holding = f"holdings-storage/holdings?query=id={holdingId}"
        print ("El HoldingID es: ", holdingId)
        url_holding = OKAPY_URL + path_holding
        req_holding = requests.get(url_holding, headers=okapi_headers, timeout=40)
        json_str_holding = json.loads(req_holding.text)
        
        for dato_holding in json_str_holding['holdingsRecords']:
            instanceId = dato_holding['instanceId']
            print ("El Id de la instancia es: ",dato_holding['instanceId'])
            path_holding2 = f"holdings-storage/holdings?query=instanceId={instanceId}"
            url_holding2 = OKAPY_URL + path_holding2
            req_holding2 = requests.get(url_holding2, headers=okapi_headers, timeout=40)
            json_str_holding2 = json.loads(req_holding2.text)
            for y in json_str_holding2['holdingsRecords']:
                ids_y= {'id':y['id'] ,'effectiveLocationId':y['effectiveLocationId']}
                ids.append(ids_y)

    print ("El título tiene los siguientes holdings: ",ids[1])
    createHoldingsId =ids[0]
    for z in ids:
        if z['effectiveLocationId'] == option:
            print('if')
            moveItem=mover_de_holdings(option,dato_item,z)
        else:
            print ('else')
            createHolding=crear_holdings (createHoldingsId,option)



def crear_holdings(createHoldingsId,option):
    holdings = f"holdings-storage/holdings/{createHoldingsId['id']}"
    url_createHolding = OKAPY_URL + holdings
    okapi_headers = {"x-okapi-token": OKAPY_TOKEN,"x-okapi-tenant": OKAPY_TENANT,"content-type": "application/json"}
    req_holding = requests.get(url_createHolding, headers=okapi_headers, timeout=40)
    json_str_holding = json.loads(req_holding.text)
    l=json_str_holding
    l_id = l['id']
    l_holdingsTypeId = l['holdingsTypeId']
    l_callNumberTypeId = l['callNumberTypeId']
    l_callNumber = l['callNumber']
    l_callNumberSuffix = l['callNumberSuffix']
    payload = {
            "id":[],
            "_version":[],
			"hrid": [],
			"holdingsTypeId": f"{l_holdingsTypeId}",
			"formerIds": [],
			"instanceId": f"{l_id}",
			"permanentLocationId": f"{option}",
			"effectiveLocationId": f"{option}",
            "electronicAccess": [],
			"callNumberTypeId": f"{l_callNumberTypeId}",
			"callNumber": f"{l_callNumber}",
			"callNumberSuffix": f"{l_callNumberSuffix}",
            "notes": [],
			"holdingsStatements": [],
			"holdingsStatementsForIndexes": [],
			"holdingsStatementsForSupplements": [],
			"discoverySuppress": False,
            "statisticalCodeIds": [],
			"holdingsItems": [],
			"bareHoldingsItems": []
    } 
    url_holding = f"holdings-storage/holdings"
    okapi_headers = {"x-okapi-token": OKAPY_TOKEN,"x-okapi-tenant": OKAPY_TENANT,"content-type": "application/json"}
    response = requests.post(url_holding, json=payload, headers=okapi_headers)
    print (response)


def mover_de_holdings(option,dato_item,z):    
    l=dato_item
    l['permanentLocationId']= option
    l['effectiveLocationId']= option
    l['holdingsRecordId']= z['id']
    j_content = l
    idItem = l['id']
    path_item2 = f"item-storage/items/{idItem}"
    url_item2 = OKAPY_URL + path_item2
    okapi_headers = {"x-okapi-token": OKAPY_TOKEN,"x-okapi-tenant": OKAPY_TENANT,"content-type": "application/json"}
    response = requests.put(url_item2, json=j_content, headers=okapi_headers)
    print (str(response.status_code))
    print(response)


if __name__ == "__main__":
    #--------- inicio lectura credenciales -----------
    dic=dic= {}
    f = open("uai_credenciales.json",)
    cred = json.load(f)
    for i in cred['okapi']:
        dic=i
    f.close()
    okapi_user = dic['user']
    okapy_password = dic['password']
    OKAPY_TENANT=dic['x_okapi_tenant']
    OKAPY_URL= dic['x_okapi_url']
    OKAPY_TOKEN = token()
    
    #--------- inicio selección nuevo location -----------
    print("Ingresa el Id location: ")
    option = str(input())

    #--------- lectura archivo Barcode que se mueven -----------
    fileName= "Barcode.xlsx"
    df = pd.read_excel(fileName, engine='openpyxl', dtype=str)
    df = df.apply(lambda x: x.fillna(""))
    totalrows=len(df)
    print(f"Cantidad de barcodes: {totalrows}") 
    reg=0   
    for i, row in df.iterrows():    
        barcode=str(row['BARCODE'])
        path = f"item-storage/items?query=barcode={barcode}"
        url= OKAPY_URL + path
        okapi_headers = {"x-okapi-token": OKAPY_TOKEN,"x-okapi-tenant": OKAPY_TENANT,"content-type": "application/json"}
        req = requests.get(url, headers=okapi_headers, timeout=40)
        json_str = json.loads(req.text)
        reg=1+reg
        print ("Caso N: ", reg)
        print ("Barcode: ", barcode)
        locationcode = location(barcode, option)
    
 
