# -*- coding: utf-8 -*-

import json
import geocoder


class Location:
    saved_locations = {}
    nominatim_server_url = ""
    def __init__(self, nominatim_server_url="http://magratea.lan:8099"):
        with open("lugares_guardados.json") as file_lugares:
            self.nominatim_server_url = nominatim_server_url
            self.saved_locations = json.load(file_lugares)
    
    # Más info
    # https://nominatim.org/
    # Container info: https://hub.docker.com/r/mediagis/nominatim

    def getLocation(self, location_name):
        locality_name = ""
        if location_name in self.saved_locations.keys():
            locality_name = self.saved_locations[location_name]
        elif isinstance(location_name, str):
            geocode_point = geocoder.osm(location_name + ", Canary Islands, Spain",
                                         url=self.nominatim_server_url)
            if (hasattr(geocode_point, "city") and type(geocode_point.city)!=type(None)):
                locality_name = geocode_point.json["city"]
                self.saved_locations.update({location_name: locality_name})
            elif (hasattr(geocode_point, "town") and type(geocode_point.town)!=type(None)):
                locality_name = geocode_point.json["town"]
                self.saved_locations.update({location_name: locality_name})
        return(locality_name)
        
    def updateDictionaryFile(self):
        # Exports dictionary to json file.
        json_locations_dic = json.dumps(self.saved_locations)
        with open("lugares_guardados.json","w") as file:
            file.write(json_locations_dic)

    def getDictionary(self):
        return(self.saved_locations)
        
