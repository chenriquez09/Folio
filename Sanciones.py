from urllib import request
import requests
import json
import time
from datetime import datetime, date, timedelta

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
        #print (url)
        req = requests.post(url, json=userpass, headers=okapi_headers,timeout=10)
        token= req.headers['x-okapi-token']
        #print (token)
        return(token)
    except ValueError:
        print("General Error on Post:"+req.text+"\nError Number: "+req.status_code)

#----------------------------Fin obtención del token-------------------------

def actualizar_bloqueo(id_user, fecha_exp, tipo_user, id_bloqueo, tipo_user_name):    
    path3 = f"manualblocks/{id_bloqueo}" 
    a1=timedelta(1)
    fecha_susp3= fecha_exp + a1
    fecha_susp4= datetime.strftime(fecha_susp3,"%Y-%m-%d")
    url3= OKAPY_URL + path3
    if tipo_user != "72fb3061-2abd-41aa-b1dd-8b2170f7159a" and tipo_user != "9d2496ba-1ef5-4343-881f-118082d36135"  and tipo_user != "d45f2c1f-4619-40a3-a1da-ff3007d2d911":
        print ("-------------------Inicio modificación bloqueo-------------------")
        payload = {
            "type": "Automatica",
            "desc": "Sanción automática por morosidad",
            "code": "SAN_AUT",
            "expirationDate": f"{fecha_susp4}",
            "borrowing": True,
            "renewals": True,
            "requests": True,
            "userId": f"{id_user}",
            "id": f"{id_bloqueo}"
        }
        okapi_headers = {"x-okapi-token": OKAPY_TOKEN,"x-okapi-tenant": OKAPY_TENANT,"content-type": "application/json"}
        response = requests.put(url3, json=payload, headers=okapi_headers)
        print("suspensión modificada!!")
        print ("Nueva fecha expiración bloqueo",fecha_susp4)
        print ("-------------------Fin modificación bloqueo-------------------\n")
    else:
        print("1.No se puede bloquear es: ",tipo_user_name,"\n")
        print("-----------fin--------------\n")    


def crear_bloqueo(id_user, fecha_susp, tipo_user, tipo_user_name):
    path2 = f"manualblocks"     
    fecha_susp2= datetime.strftime(fecha_susp,"%Y-%m-%d")
    url2= OKAPY_URL + path2
    if tipo_user != "72fb3061-2abd-41aa-b1dd-8b2170f7159a" and tipo_user != "9d2496ba-1ef5-4343-881f-118082d36135"  and tipo_user != "d45f2c1f-4619-40a3-a1da-ff3007d2d911":
        print ("-------------------Inicio creación bloqueo-------------------")
        payload = {
            "type": "Automatica",
            "desc": "Sanción automática por morosidad",
                "code": "SAN_AUT",
            "patronMessage": "Sanción automática por morosidad",
            "expirationDate": f"{fecha_susp2}",
            "borrowing": True,
            "renewals": True,
            "requests": True,
            "userId": f"{id_user}"
        }
        print("suspendido!!")
        okapi_headers = {"x-okapi-token": OKAPY_TOKEN,"x-okapi-tenant": OKAPY_TENANT,"content-type": "application/json"}
        response = requests.post(url2, json=payload, headers=okapi_headers)
        print ("-------------------Fin creación bloqueo-------------------")
    else:
        print("2.No se puede bloquear es: ",tipo_user_name,"\n")
        print("-----------fin--------------\n")   

def users_morosos():
    status = "Open"
    path = f"circulation/loans?limit=9999&query=status={status}"
    url= OKAPY_URL + path
    okapi_headers = {"x-okapi-token": OKAPY_TOKEN,"x-okapi-tenant": OKAPY_TENANT,"content-type": "application/json"}
    req = requests.get(url, headers=okapi_headers, timeout=40)
    json_str = json.loads(req.text)
    reg=0
    for dato in json_str['loans']:
        print ("-------------------Inicio get morosos-------------------")
        print("user:",reg)
        reg+=1
        fecha_ven = dato['dueDate']
        fecha_ven2= fecha_ven[0:10]
        fecha_act = datetime.now()
        fecha_vencimiento = datetime.strptime(fecha_ven2,"%Y-%m-%d")
        if fecha_vencimiento < fecha_act:
            print("Moroso!!!")
            id_user = dato['userId']
            rut_user= dato['borrower']['barcode']
            tipo_user= dato['patronGroupAtCheckout']['id']
            tipo_user_name= dato['patronGroupAtCheckout']['name']
            delta = fecha_act - fecha_vencimiento
            print("Fecha vencimiento: ", fecha_vencimiento)
            print("Cantidad dias atraso: ", delta)
            print("Rut: ", rut_user)
            print("Tipo de usuario: ", tipo_user_name)
            fecha_susp = fecha_act + delta        
            path_bloqueo = f"manualblocks?query=userId={id_user}"
            url_bloqueo = OKAPY_URL + path_bloqueo
            req_bloqueo = requests.get(url_bloqueo, headers=okapi_headers, timeout=40)
            json_str_bloqueo = json.loads(req_bloqueo.text)
            a1=json_str_bloqueo['totalRecords']
            if a1>0:
                for x in json_str_bloqueo['manualblocks']:
                    if x['code']=="SAN_AUT":
                        dato1=x
                        code_bloqueo = dato1['code']     
                        if code_bloqueo == "SAN_AUT":
                            id_bloqueo = dato1['id']
                            fecha_exp_sw1 = dato1['expirationDate']
                            fecha_exp_sw2 = fecha_exp_sw1[0:10]
                            fecha_exp = datetime.strptime(fecha_exp_sw2,"%Y-%m-%d")
                            print("fn_actualizar_bloqueo, bloqueoId: ",id_bloqueo)
                            print ("-------------------fin get morosos-------------------\n")
                            actualizar_bloqueo(id_user, fecha_exp, tipo_user, id_bloqueo, tipo_user_name)
            else:
                print("fn_crear_bloquear")
                print ("-------------------fin get morosos-------------------\n")
                crear_bloqueo(id_user, fecha_susp, tipo_user, tipo_user_name)
        else:
            print("No es moroso")

if __name__ == "__main__":
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
    users_morosos()
