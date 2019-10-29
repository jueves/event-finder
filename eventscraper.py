# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# Functions to scrape lagenda.org
def getEventsURL(initial_date, end_date):
    urlpart1="https://lagenda.org/programacion/hoy?field_fecha_value%5Bmin%5D%5Bdate%5D="
    urlsep="%2F"
    urlpart2="&field_fecha_value%5Bmax%5D%5Bdate%5D="
    initial_formated_date = str(initial_date.day)+urlsep+str(initial_date.month)+urlsep+str(initial_date.year)
    end_formated_date = str(end_date.day)+urlsep+str(end_date.month)+urlsep+str(end_date.year)
    #https://lagenda.org/programacion/hoy?field_fecha_value%5Bmin%5D%5Bdate%5D=30%2F10%2F2019&field_fecha_value%5Bmax%5D%5Bdate%5D=01%2F11%2F2019   
    return urlpart1+initial_formated_date+urlpart2+end_formated_date

def getEvents(initial_date, end_date):
    # initial_date Objeto tipo date. Fecha de inicio del periodo sobre el que queremos ver eventos.
    # end_date Objeto tipo date. Fecha final de dicho periodo.
    # data Dataframe de pandas con los datos sin procesar. No incluye meteorología
    # ni los lugares no han sido proecsador por getProperName()
    
    # Captura la página entera
    url_lagenda = getEventsURL(initial_date, end_date)   
    lagenda_page = requests.get(url_lagenda)
    soup = BeautifulSoup(lagenda_page.content)

    # Las etiquetas h4 con class="title" contienen los títulos de los eventos
    eventos = soup.find_all("h4", {"class": "title"})

    # Tabla con nombres y títulos de eventos
    tabla_eventos = []
    for evento in eventos:
        name = evento.a.string
        full_event = evento.parent    # Categoría que contiene todo el evento.
        categ = full_event.find("div", {"class": "post-category"}).a.string
        tabla_eventos.append([name, categ])

    # Convertir la tabla a un dataframe de Pandas
    data = pd.DataFrame(tabla_eventos, columns=["Nombre", "Categoría"])
    return data