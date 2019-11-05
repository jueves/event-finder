# -*- coding: utf-8 -*-

import googlemaps
import csv
import requests

def getPostalCode(location_name):
    location_name += ", Islas Canarias"
    geocode_result = gmaps.geocode(location_name)
    postal_code = 0
    for level in geocode_result[0]['address_components']:
        if (level['types']==['postal_code']):
            postal_code = int(level['long_name'])
            break
    return(postal_code)

def getMunicipalityCode(location_name):
    postal_code = getPostalCode(location_name)
    location_code = codes_dic[postal_code]
    return(location_code)
    

def getCodesDictionary():
    codes_file_url = "https://github.com/inigoflores/ds-codigos-postales-ine-es/raw/master/data/codigos_postales_municipios.csv"
    with requests.Session() as s:
        codes_raw = s.get(codes_file_url)
        codes_decoded = codes_raw.content.decode('utf-8')
        codes_csv = csv.reader(codes_decoded.splitlines())
        codes_dic = {}
        next(codes_csv, None) # Skips header
        for line in codes_csv:
            codes_dic[int(line[0])] = int(line[1])
        return(codes_dic)

file_gmaps = open("gmaps_api_key.txt")
gmaps_key = file_gmaps.readline()
file_gmaps.close()
gmaps = googlemaps.Client(key=gmaps_key)

codes_dic = getCodesDictionary()