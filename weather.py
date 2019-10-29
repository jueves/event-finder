# -*- coding: utf-8 -*-

file_aemet = open("aemet_api_key.txt")
aemet_key = file_aemet.readline()
file_aemet.close()

def getWeather(municipio, fecha):
    return prevision
# municipio Nombre oficial del municipio del evento.
# fecha Objeto tipo date. Fecha del evento.
# previsión Lista con valores para estado del cielo, lluvia, temperatura...
# API AEMET: https://opendata.aemet.es/centrodedescargas/inicio