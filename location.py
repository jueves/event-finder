# -*- coding: utf-8 -*-

import json
import geocoder


class Location:
    saved_locations = {}
    def __init__(self, gmaps_key):
        self.gmaps_key = gmaps_key
        
        # Carga el diccionario con las coordenadas de la localidad de lugares donde
        # se realizan eventos.
        with open("lugares_guardados.json") as file_lugares:
            self.saved_locations = json.load(file_lugares)
    
    def getLocation(self, location_name):
        # Recibe un objeto string con el nombre de un lugar de Canarias.
        # Devuelve una lista con las coordenadas de la localdiad del lugar.
        geolocation = [0]
        
        # Comprueba si ya tenemos almacenado el código postal del lugar.
        if location_name in self.saved_locations.keys():
            geolocation = self.saved_locations[location_name]
        elif isinstance(location_name, str):
            # Utiliza la API de GoogleMaps para obtener información sobre el lugar.
            geocode_point = geocoder.google(location_name + ", Islas Canarias",
                                             key=self.gmaps_key, components="country:ES")
            
            # Con objeto de reducir los valores del diccionario se buscan las coordenadas
            # centrales de la localidad
            if hasattr(geocode_point, "locality") and isinstance(geocode_point.locality, str):
                geocode_locality = geocoder.google(geocode_point.locality+ ", Islas Canarias",
                                                key=self.gmaps_key, components="country:ES")
                
                geolocation = geocode_locality.latlng
                
                # Redondeamos las coordenadas.
                # Dos decimales permiten definir un punto con aprox 1km de error,
                # lo cual es sobradamente suficiente para una predicción meteorológica.
                geolocation = [round(geolocation[0], 2), round(geolocation[1], 2)]
                self.saved_locations.update({location_name: geolocation})
        
        return(geolocation)
        
    def updateDictionaryFile(self):
        # Exports dictionary to json file.
        json_locations_dic = json.dumps(self.saved_locations)
        with open("lugares_guardados.json","w") as file:
            file.write(json_locations_dic)

    def getGmapsKey(self):
        return(self.gmaps_key)
    
    def setGmapsKey(self, gmaps_key):
        self.gmaps_key(gmaps_key)
        
    def getDictionary(self):
        return(self.saved_locations)