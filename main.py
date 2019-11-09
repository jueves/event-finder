# -*- coding: utf-8 -*-

from eventscraper import getEvents
from weather import getWeather
from location import getMunicipalityCode
import datetime
# Carga de las API keys
# Cada usuario ha de tener sus propias claves. En este caso, para la práctica se adjuntan en el documento que se sube la web
file_aemet = open("aemet_api_key.txt")
aemet_key = file_aemet.readline()
file_aemet.close()
file_gmaps = open("gmaps_api_key.txt")
gmaps_key = file_gmaps.readline()
file_gmaps.close()

# Fechas para hacer el test. Tener en cuenta que el rango de predicción de la AEMET es de 7 días
dummy_date1 = datetime.date(2019, 11, 9)
dummy_date2 = datetime.date(2019, 11, 12)

legenda_data = getEvents(dummy_date1, dummy_date2)

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
