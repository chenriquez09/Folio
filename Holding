from urllib import request
import requests
import json
from datetime import datetime, date, timedelta
import pandas as pd
    

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
        url_holding = OKAPY_URL + path_holding
        req_holding = requests.get(url_holding, headers=okapi_headers, timeout=40)
        json_str_holding = json.loads(req_holding.text)
        
        for dato_holding in json_str_holding['holdingsRecords']:
            instanceId = dato_holding['instanceId']
            print (dato_holding['instanceId'])
            path_holding2 = f"holdings-storage/holdings?query=instanceId={instanceId}"
            url_holding2 = OKAPY_URL + path_holding2
            req_holding2 = requests.get(url_holding2, headers=okapi_headers, timeout=40)
            json_str_holding2 = json.loads(req_holding2.text)
            for y in json_str_holding2['holdingsRecords']:
                ids_y= {'id':y['id'] ,'effectiveLocationId':y['effectiveLocationId']}
                ids.append(ids_y)
          
    print (ids)
    for z in ids:
        if z['effectiveLocationId'] == option:
            l=dato_item
            l['permanentLocationId']= option
            l['effectiveLocationId']= option
            j_content = l
            idItem = l['id']
            path_item2 = f"item-storage/items/{idItem}"
            url_item2 = OKAPY_URL + path_item2
            okapi_headers = {"x-okapi-token": OKAPY_TOKEN,"x-okapi-tenant": OKAPY_TENANT,"content-type": "application/json"}
            response = requests.put(url_item2, json=j_content, headers=okapi_headers)
            print(response)
                

if __name__ == "__main__":
    #--------- inicio lectura credenciales -----------
  
    #--------- inicio selección nuevo holding -----------
    print("1 VIÑA CG"+"\n"+"2 PRE1 CG"+"\n"+"3 POST CG")
    option = str(input())

    #--------- lectura archivo Barcode que se mueven -----------
    fileName= ""
    df = pd.read_excel(fileName, engine='openpyxl', dtype=str)
    df = df.apply(lambda x: x.fillna(""))
    totalrows=len(df)
    print(f"INFO ORDERS Total: {totalrows}") 
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
        print (barcode)
        locationcode = location(barcode, option)
    
 
