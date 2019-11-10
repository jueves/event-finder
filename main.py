# -*- coding: utf-8 -*-

from eventscraper import getEvents
from weather import Weather
from location import Location
import datetime

# Carga de las API keys
# Cada usuario ha de tener sus propias claves. En este caso, para la práctica se adjuntan en el documento que se sube la web
with open("gmaps_api_key.txt") as file_gmaps:
    gmaps_key = file_gmaps.readline()
gmaps_key = gmaps_key.strip()

with open("darksky_api_key.txt") as file_darksky:
    darksky_key = file_darksky.read()
darksky_key = darksky_key.strip()



# Fechas para hacer el test. Tener en cuenta que el rango de predicción de la AEMET es de 7 días
dummy_date1 = datetime.date(2019, 11, 10)
dummy_date2 = datetime.date(2019, 11, 11)

# Scraping de los eventos
legenda_data = getEvents(dummy_date1, dummy_date2)

#Obtención de los datos del municipio
location = Location(gmaps_key)
codigoMunicipio=[]
for i in range(len(legenda_data)):
    codigoMunicipio.append(location.getLocation(legenda_data['location'][i]))

legenda_data['codigoMunicipio'] = codigoMunicipio

# Crear un bucle para obtener los datos del código del municipio y, 
# con ese código, junto con la fecha del evento, obtener los datos de la 
# predicción para ese día
estadoCielo=[]
probPrecipitacion=[]
sensTermMax=[]
sensTermMin=[]
temperaturaMax=[]
temperaturaMin=[]
weather = Weather(darksky_key)
for i in range(len(legenda_data)):
    datosTiempo=weather.getWeather(legenda_data['codigoMunicipio'][i],legenda_data['date'][i])
    estadoCielo.append(datosTiempo['estadoCielo'][i])
    probPrecipitacion.append(datosTiempo['probPrecipitacion'][i])
    sensTermMax.append(datosTiempo['sensTermMax'][i])
    sensTermMin.append(datosTiempo['sensTermMin'][i])
    temperaturaMax.append(datosTiempo['temperaturaMax'][i])
    temperaturaMin.append(datosTiempo['temperaturaMin'][i])    
    
    
legenda_data['estadoCielo'] = estadoCielo
legenda_data['probPrecipitacion'] = probPrecipitacion
legenda_data['sensTermMax'] = sensTermMax
legenda_data['sensTermMin'] = sensTermMin
legenda_data['temperaturaMax'] = temperaturaMax
legenda_data['temperaturaMin'] = temperaturaMin

# Actualiza el archivo del diccionario de localizaciones 
location.updateDictionaryFile()

#guardar los datos en un documento .csv
legenda_data.to_csv('DatosLegenda.csv')
