# -*- coding: utf-8 -*-

import json
import geocoder

def getLocation(location_name):
    # Recibe un objeto string con el nombre de un lugar de Canarias.
    # Devuelve una lista con las coordenadas de la localdiad del lugar.
    geolocation = [0]
    
    # Comprueba si ya tenemos almacenado el código postal del lugar.
    if location_name in saved_locations.keys():
        geolocation = saved_locations[location_name]
    else:
        # Utiliza la API de GoogleMaps para obtener información sobre el lugar.
        geocode_point = geocoder.google(location_name + ", Islas Canarias",
                                         key=gmaps_key, components="country:ES")
        
        # Con objeto de reducir los valores del diccionario se buscan las coordenadas
        # centrales de la localidad
        geocode_locality = geocoder.google(geocode_point.locality+ ", Islas Canarias",
                                        key=gmaps_key, components="country:ES")
        
        geolocation = geocode_locality.latlng
        
        # Redondeamos las coordenadas.
        # Dos decimales permiten definir un punto con aprox 1km de error,
        # lo cual es sobradamente suficiente para una predicción meteorológica.
        geolocation = [round(geolocation[0], 2), round(geolocation[1], 2)]
        saved_locations.update({location_name: geolocation})
    
    return(geolocation)

# Carga un diccionario con las coordenadas de la localidad de lugares donde
# se realizan eventos.
# Esto permite reducir las peticiones a la API de Google Maps.
# Cuando getLocation() no encuentra un lugar en este diccionario descarga
# la información de Google Maps y la añade.
with open("lugares_guardados.json") as file_lugares:
    saved_locations = json.load(file_lugares)