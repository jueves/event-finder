# -*- coding: utf-8 -*-

import googlemaps
import csv
import requests

def getPostalCode(location_name):
    # Recibe un objeto string con el nombre de un lugar de Canarias.
    # Devuelve un objeto int con el código postal de dicho lugar.
    location_name += ", Islas Canarias"
    
    # Utiliza la API de GoogleMaps para obtener información sobre el lugar.
    geocode_result = gmaps.geocode(location_name)
    
    postal_code = 0
    for level in geocode_result[0]['address_components']:
        if (level['types']==['postal_code']):
            postal_code = int(level['long_name'])
            break
    return(postal_code)

def getMunicipalityCode(location_name):
    # Recibe objeto string con el nombre de un lugar de Canarias.
    # Devuelve un objeto int con el código que AEMET da al municipio
    # del evento.
    # Si no encuentra la localización correctamente devuelve el valor 0.
    postal_code = getPostalCode(location_name)
    location_code = codes_dic[postal_code]
    return(location_code)
    

def getCodesDictionary():
    # Crea un diccionario que relaciona códigos postales con el código de su
    # municipio según la clasificación del INE y AEMET.
    # Utiliza como fuente de datos una tabla del proyecto de GitHub
    # ds-codigos-postales-ine-es de Íñigo Flores y Pablo Castellano.
    codes_file_url = "https://github.com/inigoflores/ds-codigos-postales-ine-es/raw/master/data/codigos_postales_municipios.csv"
    with requests.Session() as s:
        codes_raw = s.get(codes_file_url)
        codes_decoded = codes_raw.content.decode('utf-8')
        codes_csv = csv.reader(codes_decoded.splitlines())
        codes_dic = {}
        next(codes_csv, None) # Skips header
        for line in codes_csv:
            codes_dic[int(line[0])] = int(line[1])
        
        # Add code 0 to manage erros getting location.
        codes_dic[0] = 0
        return(codes_dic)

# Crea el objeto gmaps para trabajar con la API de Google Maps
file_gmaps = open("gmaps_api_key.txt")
gmaps_key = file_gmaps.readline()
file_gmaps.close()
gmaps = googlemaps.Client(key=gmaps_key)

# Crea el diccionario de códigos postales y códigos de municipios.
codes_dic = getCodesDictionary()