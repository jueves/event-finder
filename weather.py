# -*- coding: utf-8 -*-

import http.client
import ssl
import json
from datetime import date, timedelta

#Usamos la API de la AEMET que nos permite ver la predicción del tiempo en el día en curso hasta un horizonte de 7 días, 
#tomando como parámetro de entrada el municipio. Los datos se actualizan continuamente.

#Por seguridad, mantenemos la clave para poder usar la API en un fichero externo
file_aemet = open("aemet_api_key.txt")
apyKey = file_aemet.readline()
file_aemet.close()

#Alternativa, pasar la APIKEY por parametro, comentar las líneas anteriores y desconmentar la siguiente
"""
apyKey='pegar la clave'
"""

#Código para usar la API de la AEMET
def getMunPrediction(codigoMun):
    #Petición de acceso a la API
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    conn = http.client.HTTPSConnection("opendata.aemet.es", context = context)
    headers = {'cache-control': "no-cache"}
    conn.request("GET", f"/opendata/api/prediccion/especifica/municipio/diaria/{codigoMun}/?api_key={apyKey}", headers=headers, )
    res = conn.getresponse()
    data = res.read().decode('utf-8','ignore')
    data = json.loads(data)

    #Guardando los datos tipo json referentes al municipio elegido
    conn.request("GET", data['datos'], headers=headers, )
    res= conn.getresponse()
    datos = res.read().decode('utf-8','ignore')
    datos= json.loads(datos)
    return(datos)

#Comprobación si existen predicciones disponibles
def fechaRangoPrediccion():
    #Evalua si una fecha de un evento está dentro del rango de predicción
    #que tiene disponible la AEMET
    #encontré la siguiente pagina para hacer el caso
    #https://python-para-impacientes.blogspot.com/2014/02/operaciones-con-fechas-y-horas.html
    hoy=date.today()
    diasMax=hoy + timedelta(days=6)
    #calcula la diferencia de días
    resta=diasMax-hoy
    #comprueba que el día que se pide es está dentro del alcance de la
    #predicción proporcionada por AEMET
    if resta.days<7 and resta.days>-1:
        contenido='TRUE'
    else:
        contenido='FALSE'
    return contenido

#Datos que queremos presentar/guardar en nuestro repositorio  
def getWeather(codigoMun):
    #Obtener la tempetara máxima y mínima para el día de la consulta
    if fechaRangoPrediccion()=='FALSE':
        print("Sin datos disponibles de predicción")
    else:
        dat=getMunPrediction(codigoMun)
        print('Temperatura máxima: ', dat[0]['prediccion']['dia'][0]['temperatura']['maxima'])
        print('Temperatura mínima: ', dat[0]['prediccion']['dia'][0]['temperatura']['minima'])
    return
#vista previa para el municipio de la Laguna
municipio='38023'
getWeather(municipio)
# municipio Nombre oficial del municipio del evento.
# fecha Objeto tipo date. Fecha del evento.
# previsión Lista con valores para estado del cielo, lluvia, temperatura...
# API AEMET: https://opendata.aemet.es/centrodedescargas/inicio
