# -*- coding: utf-8 -*-

from eventscraper import getEvents
from weather import getWeather
from location import getMunicipalityCode
import datetime
"""
# Carga de las API keys
# Cada usuario ha de tener sus propias claves. En este caso, para la práctica se adjuntan en el documento que se sube la web
file_aemet = open("aemet_api_key.txt")
aemet_key = file_aemet.readline()
file_aemet.close()
file_gmaps = open("gmaps_api_key.txt")
gmaps_key = file_gmaps.readline()
file_gmaps.close()
"""
aemet_key = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqdmVsYXpxdWV6bkB1b2MuZWR1IiwianRpIjoiZjQ3Yzk4Y2QtZjE2MS00MDE5LThjMmItZDRiNmRjYmE3Zjg3IiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE1NzIzNzYyNTgsInVzZXJJZCI6ImY0N2M5OGNkLWYxNjEtNDAxOS04YzJiLWQ0YjZkY2JhN2Y4NyIsInJvbGUiOiIifQ.6NfCcBqhSlDQNCbMtmwsSkIjkR3vMbjS6U8czA9DjAk'
gmaps_key = 'AIzaSyDvR9SKBE7-LEN6_boq6RLZuGqpJ66O-2Q'


# Fechas para hacer el test. Tener en cuenta que el rango de predicción de la AEMET es de 7 días
dummy_date1 = datetime.date(2019, 11, 10)
dummy_date2 = datetime.date(2019, 11, 11)

# Scraping de los eventos
legenda_data = getEvents(dummy_date1, dummy_date2)

#Obtención de los datos del municipio
codigoMunicipio=[]
for i in range(len(legenda_data)):
    codigoMunicipio.append(getMunicipalityCode(legenda_data['location'][i]))

legenda_data['codigoMunicipio'] = codigoMunicipio

#Obtención de los datos de la predicción
estadoCielo=[]
probPrecipitacion=[]
sensTermMax=[]
sensTermMin=[]
temperaturaMax=[]
temperaturaMin=[]
for i in range(len(legenda_data)):
    datosTiempo=getWeather(legenda_data['codigoMunicipio'][i],legenda_data['date'][i])
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
"""
# Crear un bucle para obtener los datos del código del municipio y, 
# con ese código, junto con la fecha del evento, obtener los datos de la 
# predicción para ese día
legenda_data['codigoMun'] = 0
for i in range(len(legenda_data['codigoMun'])):
    legenda_data['codigoMun'][i]=getMunicipalityCode(legenda_data['location'][i])
    legenda_data['datosPrediccion'][i]=getWeather(legenda_data['codigoMun'][i],legenda_data['date'][i])

print(legenda_data[0])

#guardar los datos en un documento .csv
legenda_data.to_csv('DatosLegenda.csv')
"""