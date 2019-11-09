# -*- coding: utf-8 -*-

import csv
import json
import geocoder

def getPostalCode(location_name):
    # Recibe un objeto string con el nombre de un lugar de Canarias.
    # Devuelve un objeto int con el código postal de dicho lugar.
    postal_code = 0
    
    # Comprueba si ya tenemos almacenado el código postal del lugar.
    if location_name in saved_locations.keys():
        postal_code = saved_locations[location_name]
    else:
        # Utiliza la API de GoogleMaps para obtener información sobre el lugar.
        geocode_area = geocoder.google(location_name + ", Islas Canarias",
                                         key=gmaps_key, components="country:ES")
        # Cuando un lugar abarca varios códigos postales, Google Maps no
        # devuelve este campo. Por eso repetimos la búsqueda con las
        # coordenadas centrales del lugar.
        geocode_point = geocoder.google(geocode_area.latlng, key=gmaps_key,
                                        method="reverse", components="country:ES")
        postal_code = int(geocode_point.postal)
        saved_locations.update({location_name: postal_code})
    
    return(postal_code)

def getMunicipalityCode(location_name):
    # Recibe objeto string con el nombre de un lugar de Canarias.
    # Devuelve un objeto int con el código que AEMET da al municipio
    # del evento.
    # Si no encuentra la localización correctamente devuelve el valor 0.
    location_code = 0
    postal_code = getPostalCode(location_name)
    
    if postal_code in codes_dic.keys():
        location_code = codes_dic[postal_code]
    
    
    return(location_code)
    

def getCodesDictionary():
    # Crea un diccionario que relaciona códigos postales con el código de su
    # municipio según la clasificación del INE y AEMET.
    # Utiliza como fuente de datos una tabla del proyecto de GitHub
    # ds-codigos-postales-ine-es de Íñigo Flores y Pablo Castellano.
    with open("codigos_postales_municipios.csv") as file:
        codes_csv = csv.reader(file)
        codes_dic = {}
        next(codes_csv, None) # Skips header
        for line in codes_csv:
            # Selecciona sólo los códigos postales de Canarias.
            if (line[0][0:2]=='38' or line[0][0:2]=='35'):
                codes_dic[int(line[0])] = int(line[1])
        
        # Add code 0 to manage erros getting location.
        codes_dic[0] = 0
    return(codes_dic)

# Crea el objeto gmaps para trabajar con la API de Google Maps
with open("gmaps_api_key.txt") as file_gmaps:
    gmaps_key = file_gmaps.readline()
#gmaps = googlemaps.Client(key=gmaps_key)

# Crea el diccionario de códigos postales y códigos de municipios.
codes_dic = getCodesDictionary()

# Carga un diccionario con los códigos de barras de cada localización para
# reducir las peticiones a la API de Google Maps. Cuando getPostalCode() no
# encuentra un lugar en este diccionario descarga la información de Google
# Maps y la añade al diccionario.
with open("lugares_codigos_postales.json") as file_lugares:
    saved_locations = json.load(file_lugares)