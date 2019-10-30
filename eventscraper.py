# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from urllib.parse import unquote


# Functions to scrape lagenda.org

def getPageSoup(initial_date, end_date):
    # Devuelve un objeto BeautifulSoup de la página de resultados
    # de eventos en dicho rango de fechas.

    # Obtener URL
    urlpart1 = ("https://lagenda.org/programacion/hoy?" +
                "field_fecha_value%5Bmin%5D%5Bdate%5D=")
    urlsep = "%2F"
    urlpart2 = "&field_fecha_value%5Bmax%5D%5Bdate%5D="
    initial_formated_date = (str(initial_date.day)+urlsep
                             + str(initial_date.month)+urlsep
                             + str(initial_date.year))
    end_formated_date = (str(end_date.day)+urlsep +
                         str(end_date.month)+urlsep+str(end_date.year))
    url_lagenda = urlpart1+initial_formated_date+urlpart2+end_formated_date

    # Obtener soup
    lagenda_page = requests.get(url_lagenda)
    soup = BeautifulSoup(lagenda_page.content)
    return(soup)


def getDates(evento_data):
        # Busca todas las fechas en las que sucede un evento
        
        fechas_raw = evento_data.find_all("span",
                                          {"class": "date-display-single"})
        fechas_clean = []
        for fecha in fechas_raw:
            day = int(fecha.string[-8:-6])
            month = int(fecha.string[-5:-3])
            year = int(fecha.string[-2:]) + 2000
            fechas_clean.append(datetime.date(year, month, day))

        rangos_fechas_raw = evento_data.find_all("span",{"class": "date-display-range"}) 
        for rango in rangos_fechas_raw:
            start_date_raw = rango.find(attrs={"class": "date-display-start"})
            end_date_raw = rango.find(attrs={"class": "date-display-end"})

            # Set start date
            day_start = int(start_date_raw.string[-8:-6])
            month_start = int(start_date_raw.string[-5:-3])
            year_start = int(start_date_raw.string[-2:]) + 2000
            start_date = datetime.date(year_start, month_start, day_start)

            # Set end date
            day_end = int(end_date_raw.string[-8:-6])
            month_end = int(end_date_raw.string[-5:-3])
            year_end = int(end_date_raw.string[-2:]) + 2000
            end_date = datetime.date(year_end, month_end, day_end)

            # Set range
            period_length = (end_date-start_date).days
            for i in range(period_length+1):
                fechas_clean.append(start_date+datetime.timedelta(days=i))

        # Sort and remove duplicated
        fechas_clean = sorted(list(set(fechas_clean)))
        return fechas_clean


def scrapEvents(soup):
    # Obtiene información para todos los eventos incluídos
    # en el objeto beautifulsoup.
    
    eventos = soup.find_all("h4", {"class": "title"})

    # Obtener datos para cada evento
    tabla_eventos_soups = []
    for evento in eventos:
        url_event = "https://www.lagenda.org" + evento.parent.a['href']
        
        if (url_event.split("/")[3] == "programacion"):
            evento_page = requests.get(url_event)
            evento_soup = BeautifulSoup(evento_page.content)
            tabla_eventos_soups.append([evento_soup, url_event])

    tabla_eventos = []
    for evento in tabla_eventos_soups:
        evento_data = evento[0].find("div", {"class": "summary entry-summary"})
        url_event = evento[1]
        fechas = getDates(evento_data)
        title = evento_data.find_all('h1', {"itemprop": "name"})[0].span.string

        # Location
        enlaces_evento = evento_data.find_all('a')
        for enlace in enlaces_evento:
            palabras_enlace = []
            palabras_enlace = enlace.get('href').split("/")
            if ("lugares" in palabras_enlace):
                location_area = unquote(palabras_enlace[2])
                location = enlace.string
                location = (location + ", " +
                            location_area.replace("-", " "))
            
            # Category    
            elif ("categoria" in palabras_enlace):
                    category = unquote(palabras_enlace[2]).replace("-", " ")

        # Create one copy of the event per day the event happens
        for i in range(len(fechas)):
            tabla_eventos.append([title, fechas[i], location, category,
                                 url_event])

    # Convertir la tabla a un dataframe de Pandas
    data = pd.DataFrame(tabla_eventos, columns=["title", "date",
                                                "location", "category", "url"])
    return(data)

def getEvents(initial_date, end_date):
    # initial_date Objeto tipo date. Fecha de inicio del periodo sobre el
    # que queremos ver eventos.
    # end_date Objeto tipo date. Fecha final de dicho periodo.
    # data Dataframe de pandas con los datos sin procesar. No incluye
    # meteorología ni los lugares no han sido proecsador por getProperName()
    lagenda_soup = getPageSoup(initial_date, end_date)
    data = scrapEvents(lagenda_soup)
    return(data)
