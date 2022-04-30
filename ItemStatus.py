from urllib import request
import requests
import json
from datetime import datetime, date, timedelta
import pandas as pd
import csv
import sys

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



def status_missing(barcode, option):
    path_item = f"item-storage/items?query=barcode={barcode}"
    url_item = OKAPY_URL + path_item
    okapi_headers = {"x-okapi-token": OKAPY_TOKEN,"x-okapi-tenant": OKAPY_TENANT,"content-type": "application/json"}
    req_item = requests.get(url_item, headers=okapi_headers, timeout=40)
    json_str_item = json.loads(req_item.text)  
    for dato_item in json_str_item['items']:
        status = dato_item['status']['name']
        print (status)
        if status != option:
            itemId = dato_item['id']
            path_item2 = f"inventory/items/{itemId}/mark-missing"
            url_item2 = OKAPY_URL + path_item2
            response = requests.post(url_item2,headers=okapi_headers, timeout=40)
            print ('Cambiado a Missing')
        else:
            print ('El item ya tiene el estado Missing')


def status_withdrawn(barcode, option):
    path_item = f"item-storage/items?query=barcode={barcode}"
    url_item = OKAPY_URL + path_item
    okapi_headers = {"x-okapi-token": OKAPY_TOKEN,"x-okapi-tenant": OKAPY_TENANT,"content-type": "application/json"}
    req_item = requests.get(url_item, headers=okapi_headers, timeout=40)
    json_str_item = json.loads(req_item.text)  
    for dato_item in json_str_item['items']:
        status = dato_item['status']['name']
        print (status)
        if status != option:
            itemId = dato_item['id']
            path_item2 = f"inventory/items/{itemId}/mark-withdrawn"
            url_item2 = OKAPY_URL + path_item2
            response = requests.post(url_item2,headers=okapi_headers, timeout=40)
            print ('Cambiado a Withdrawn')
        else:
            print ('El item ya tiene el estado Withdrawn')


def status_unavailable(barcode,option):
    path_item = f"item-storage/items?query=barcode={barcode}"
    url_item = OKAPY_URL + path_item
    okapi_headers = {"x-okapi-token": OKAPY_TOKEN,"x-okapi-tenant": OKAPY_TENANT,"content-type": "application/json"}
    req_item = requests.get(url_item, headers=okapi_headers, timeout=40)
    json_str_item = json.loads(req_item.text)  
    for dato_item in json_str_item['items']:
        status = dato_item['status']['name']
        print (status)
        if status != option:
            itemId = dato_item['id']
            path_item2 = f"inventory/items/{itemId}/mark-unavailable"
            url_item2 = OKAPY_URL + path_item2
            response = requests.post(url_item2,headers=okapi_headers, timeout=40)
            print ('Cambiado a unavailable')
        else:
            print ('El item ya tiene el estado unavailable')


def otro():    
    print('otro estado')


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
    #--------- fin obtención token -----------
    #--------- inicio selección nuevo holding -----------
    print("Missing"+"\n"+"Available"+"\n"+"Unavailable"+"\n"+"Withdrawn")
    option = str(input())

    #--------- lectura archivo Barcode que se mueven -----------
    fileName= "Barcode.xlsx"
    df = pd.read_excel(fileName, engine='openpyxl', dtype=str)
    df = df.apply(lambda x: x.fillna(""))
    totalrows=len(df)
    print(f"INFO ORDERS Total: {totalrows}") 
    reg=0   
    for i, row in df.iterrows():    
        barcode = ""
        barcode=str(row['BARCODE']).strip()
        path = f"item-storage/items?query=barcode={barcode}"
        url= OKAPY_URL + path
        okapi_headers = {"x-okapi-token": OKAPY_TOKEN,"x-okapi-tenant": OKAPY_TENANT,"content-type": "application/json"}
        req = requests.get(url, headers=okapi_headers, timeout=40)
        json_str = json.loads(req.text)
        reg=1+reg
        print ("Caso N: ", reg)
        print (barcode)
        if option == 'Missing':
            statusItem=status_missing(barcode,option)
        elif option == 'Withdrawn':
            statusItem=status_withdrawn(barcode,option)
        elif option == 'Unavailable':
            statusItem=status_unavailable(barcode,option)
        else:
            statusItem=otro()
   
