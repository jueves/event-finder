# -*- coding: utf-8 -*-

from eventscraper import getEvents
from location import Location
from events_rating import Event_rating
import datetime
import sys

# Creates dictionary of arguments
args_dic = {}
for argument in sys.argv:
    arg_list = argument.split("=")
    if len(arg_list) == 2:
        args_dic.update({arg_list[0]: arg_list[1]})

# Sets variables from arguments
valid_modes = ["multiloc", "laguna"]
if "mode" in args_dic.keys():
    if args_dic["mode"] in valid_modes:
        program_mode = args_dic["mode"]
    else:
        print("Invalid mode. Running in Laguna mode.")
        program_mode = "laguna"
else:
    program_mode = "laguna"

if "days" in args_dic.keys():
    if args_dic["days"] in range(30):
        days_to_get = args_dic["days"]
    else:
        print("Invalid day range. Getting 5 days by default.")
        days_to_get = 5
else:
    days_to_get = 5

start_date = datetime.datetime.today()
end_date = start_date + datetime.timedelta(days=days_to_get)

# Scraping de los eventos
lagenda_data = getEvents(start_date, end_date, program_mode)

# Get locations
if program_mode == "multiloc":
    location = Location()
    locality=[]
    for i in lagenda_data.index:
        locality.append(location.getLocation(lagenda_data['location'][i]))

elif program_mode == "laguna":
    locality=["La Laguna"]*lagenda_data.shape[0]

lagenda_data['locality'] = locality

# Se eliminan las ocurrencias eventos fuera de rango.
# Se han descargado solo los eventos que acontecen en el rango indicado,
# pero para cada uno de ellos se han añadido todos los días en que este tiene lugar.
lagenda_data.to_csv('Datoslagenda_FULL.csv')
lagenda_data = lagenda_data[lagenda_data.date <= end_date]
lagenda_data = lagenda_data[start_date <= lagenda_data.date]

# Filtrado
rating = []
rater = Event_rating()
for index, evento in lagenda_data.iterrows():
    rating.append(rater.rateEvent(evento))
lagenda_data['rating'] = rating

lagenda_data.nlargest(20, "rating").to_csv("top20.csv")

lagenda_data[lagenda_data.rating > 0].to_csv("positivos.csv")

# Actualización del archivo del diccionario de localizaciones 
if program_mode=="multiloc":
    location.updateDictionaryFile()

# Exportación de datos de eventos
lagenda_data.to_csv('Datoslagenda.csv')
