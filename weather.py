import http.client
import ssl
import json
import datetime

#Usamos la API de la AEMET que nos permite ver la predicción del tiempo en el día en curso hasta un horizonte de 7 días, 
#tomando como parámetro de entrada el municipio. Los datos se actualizan continuamente.

#Por seguridad, mantenemos la clave para poder usar la API en un fichero externo
file_aemet = open("aemet_api_key.txt")
apyKey = file_aemet.readline()
file_aemet.close()


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
    return datos

#Comprobación si existen predicciones disponibles: evalua si una fecha
#de un evento está dentro del rango de predicción que tiene disponible la AEMET
#Se usa como guía la web:
#https://python-para-impacientes.blogspot.com/2014/02/operaciones-con-fechas-y-horas.html    
def fechaRangoPrediccion(fechaEvento):

    #Alcance máximo de predicción ofrecida por la AEMET
    diasMax=datetime.datetime.today().date() + datetime.timedelta(days=6)
    
    #calcula la diferencia de días
    resta=diasMax-fechaEvento
    
    #comprueba que el día que se pide es está dentro del alcance de la
    #predicción proporcionada por AEMET
    if resta.days<7 and resta.days>-1:
        contenido='TRUE'
    else:
        contenido='FALSE'
    
    return contenido

#Datos que queremos presentar/guardar en nuestro repositorio  
def getWeather(codigoMun,fecha):
    
    #Comprobamos si la fecha es válida
    if fechaRangoPrediccion(fecha)=='FALSE':
        datosWeather="Sin datos disponibles de predicción"
    else:
        #se calcula el día objetivo para obtener los datos en forma de índice
        hoy=datetime.datetime.today().date()
        diferencia= fecha - hoy
        resta=diferencia.days+1
        
        #Obtenemos la predicción del municipio de interés
        dat=getMunPrediction(codigoMun)
        
        #Se guardan los datos de la predicción
        datosWeather={'estadoCielo': dat[0]['prediccion']['dia'][resta]['estadoCielo'][0]['descripcion'],
                      'probPrecipitacion':dat[0]['prediccion']['dia'][resta]['probPrecipitacion'][0]['value'],
                      'sensTermMax':dat[0]['prediccion']['dia'][resta]['sensTermica']['maxima'],
                      'sensTermMin':dat[0]['prediccion']['dia'][resta]['sensTermica']['minima'],
                      'temperaturaMax':dat[0]['prediccion']['dia'][resta]['temperatura']['maxima'],
                      'temperaturaMin':dat[0]['prediccion']['dia'][resta]['temperatura']['minima']}

    return datosWeather

# municipio Nombre oficial del municipio del evento.
# fecha Objeto tipo date. Fecha del evento.
# previsión Lista con valores para estado del cielo, lluvia, temperatura...
# API AEMET: https://opendata.aemet.es/centrodedescargas/inicio
