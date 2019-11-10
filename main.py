# -*- coding: utf-8 -*-

from eventscraper import getEvents
from weather import Weather
from location import Location
import datetime
import sys

# Carga de las API keys
with open("gmaps_api_key.txt") as file_gmaps:
    gmaps_key = file_gmaps.readline()
gmaps_key = gmaps_key.strip()

with open("darksky_api_key.txt") as file_darksky:
    darksky_key = file_darksky.read()
darksky_key = darksky_key.strip()


# Lectura de argumentos
if len(sys.argv)==3:
    arg1 = sys.argv[1].split("-")
    arg2 = sys.argv[2].split("-")
    start_date = datetime.datetime(int(arg1[2]), int(arg1[1]), int(arg1[0]), 0, 0)
    end_date = datetime.datetime(int(arg2[2]), int(arg2[1]), int(arg2[0]), 0, 0)   
else:
    start_date = datetime.datetime.today()
    end_date = start_date + datetime.timedelta(days=5)

# Scraping de los eventos
lagenda_data = getEvents(start_date, end_date)

#Obtención de los datos del municipio
location = Location(gmaps_key)
coordenadasLocalidad=[]
for i in lagenda_data.index:
    coordenadasLocalidad.append(location.getLocation(lagenda_data['location'][i]))

lagenda_data['coordenadasLocalidad'] = coordenadasLocalidad

# Se eliminan las ocurrencias eventos fuera de rango.
# Se han descargado solo los eventos que acontecen en el rango indicado,
# pero para cada uno de ellos se han añadido todos los días en que este tiene lugar.
lagenda_data.to_csv('Datoslagenda_noWeather.csv')
lagenda_data = lagenda_data[lagenda_data.date <= end_date]
lagenda_data = lagenda_data[start_date <= lagenda_data.date]

# Obtención de previsiones meteorológicas
nubosidad=[]
probPrecipitacion=[]
sensTermMax=[]
sensTermMin=[]
temperaturaMax=[]
temperaturaMin=[]
weather = Weather(darksky_key)
for i in lagenda_data.index:
    datosTiempo=weather.getWeather(lagenda_data['coordenadasLocalidad'][i],lagenda_data['date'][i])
    nubosidad.append(datosTiempo['nubosidad'])
    probPrecipitacion.append(datosTiempo['probPrecipitacion'])
    sensTermMax.append(datosTiempo['sensTermMax'])
    sensTermMin.append(datosTiempo['sensTermMin'])
    temperaturaMax.append(datosTiempo['temperaturaMax'])
    temperaturaMin.append(datosTiempo['temperaturaMin'])
    
    
lagenda_data['nubosidad'] = nubosidad
lagenda_data['probPrecipitacion'] = probPrecipitacion
lagenda_data['sensTermMax'] = sensTermMax
lagenda_data['sensTermMin'] = sensTermMin
lagenda_data['temperaturaMax'] = temperaturaMax
lagenda_data['temperaturaMin'] = temperaturaMin

# Actualización del archivo del diccionario de localizaciones 
location.updateDictionaryFile()

# Exportación de datos de eventos
lagenda_data.to_csv('Datoslagenda.csv')
