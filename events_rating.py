#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

class Event_rating():
    filters_dic = {}
    def __init__(self):
        with open("event_filters.json") as file_filters:
            self.filters_dic = json.load(file_filters)

    def rateEvent(self, event):
        event_points = 0
        
        for filtro in self.filters_dic.keys():
            campos = self.filters_dic[filtro]["campos"]
            palabras = self.filters_dic[filtro]["palabras"]
            puntos = self.filters_dic[filtro]["puntos"]
            for campo in campos:
                for palabra in palabras:
                    if palabra in str(event[campo]):
                        event_points = event_points + puntos
    
        return(event_points)
