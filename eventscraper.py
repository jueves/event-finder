# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from urllib.parse import unquote
import re

# Functions to scrape lagenda.org

def getPageSoup(initial_date, end_date, mode="laguna"):
    # Devuelve un objeto BeautifulSoup de la página de resultados
    # de eventos en dicho rango de fechas.

    # Obtener URL
    urlsep = "%2F"
    initial_formated_date = (str(initial_date.day)+urlsep
                             + str(initial_date.month)+urlsep
                             + str(initial_date.year))
    end_formated_date = (str(end_date.day)+urlsep +
                         str(end_date.month)+urlsep+str(end_date.year))
    
    # Sets diferent urls depending on selected running mode
    if mode=="multiloc":
        urlpart1 = ("https://lagenda.org/programacion/hoy?field_fecha_value%5Bmin%5D%5Bdate%5D=")
        urlpart2 = "&field_fecha_value%5Bmax%5D%5Bdate%5D="
        url_lagenda = urlpart1+initial_formated_date+urlpart2+end_formated_date
    elif mode=="laguna":
        urlpart1 = "https://lagenda.org/programacion/contra-poesia-ante-la-represion-2dic16?field_fecha_value[min][date]="
        urlpart2 = "&field_fecha_value[max][date]="
        urlpart3 = "&field_fecha_continua_value[value][date]="
        urlpart4 = "&lugar=1067&categoria=All"
        url_lagenda = (urlpart1+initial_formated_date+urlpart2+end_formated_date
                       +urlpart3+initial_formated_date+urlpart4)
    
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
           fechas_clean.append(cleanDateTime(fecha))

        rangos_fechas_raw = evento_data.find_all("span",{"class": "date-display-range"}) 
        for rango in rangos_fechas_raw:
            start_date_raw = rango.find(attrs={"class": "date-display-start"})
            end_date_raw = rango.find(attrs={"class": "date-display-end"})

            # Set start date
            start_date = cleanDateTime(start_date_raw, True)
            # Set end date
            end_date = cleanDateTime(end_date_raw, True)
            # Get weekdays
            week_days = getWeekDays(rango)
            # Set range
            period_length = (end_date-start_date).days
                       
            for i in range(period_length+1):
                this_date = start_date+datetime.timedelta(days=i)
                if (this_date.weekday() in week_days):
                    fechas_clean.append(this_date)

        # Sort and remove duplicated
        fechas_clean = sorted(list(set(fechas_clean)))
        return fechas_clean

def getWeekDays(rango):
    # Recibe el bloque de HTML que incluye los días de la semana que se celebra
    # el evento y devuelve una lista con dichos días en formato numérico.
    # Ej: "Lunes, miércoles y viernes" => [0, 2, 4]
    
    text = str(rango.parent.next_sibling).lower()
    semana = {"lunes":0, "martes":1, "miércoles":2, "miercoles":2, "jueves":3,
              "viernes":4, "sábado":5, "sabado":5, "domingo":6}
    dias_evento = []
    # Días sueltos
    for dia in semana:
        dia_encontrado = re.findall(dia, text)
        if (len(dia_encontrado)>0):
            dias_evento.append(semana[dia_encontrado[0]])
    
    # Rangos de días
    for dia1 in semana:
        for dia2 in semana:
            rango_a_buscar = dia1+" a "+dia2
            rango_encontrado = re.findall(rango_a_buscar, text)
            if (len(rango_encontrado)>0):
                for i in range(semana[dia1], semana[dia2]):
                    dias_evento.append(i)
    
    # Si no se mencionan días, elegir todos.
    if (len(dias_evento)==0):
        dias_evento = [0, 1, 2, 3, 4, 5, 6]
    
    # Eliminar repetidos
    dias_evento = sorted(list(set(dias_evento))) 
    return(dias_evento)

def cleanDateTime(fecha_raw, is_range=False):
            # Recibe el bloque de HTML que incluye la fecha y hora del evento
            # y los devuelve en forma de objeto datetime.
            
            day = int(fecha_raw.string[-8:-6])
            month = int(fecha_raw.string[-5:-3])
            year = int(fecha_raw.string[-2:]) + 2000                    
            
            # Busca un rango de horas o una hora suelta
            hora_block = ""
            if (is_range):
                hora_block = str(fecha_raw.parent.parent.next_sibling)
            else:
                hora_block = str(fecha_raw.parent.next_sibling)
            
            hora_range_raw = re.findall(r"[0-2][0-9]:[0-5][0-9] a [0-2][0-9]:[0-5][0-9]", hora_block)
            hora_raw = re.findall(r"[0-2][0-9]:[0-5][0-9]", hora_block)
            
            # Si sólo hay una hora, o un rango de hora, escoge la primera hora.
            if (len(hora_raw)==1 or len(hora_range_raw)==1):
                hora = [int(hora_raw[0][0:2]), int(hora_raw[0][3:5])]
            else:
                hora = [0, 0]
                
            fecha_clean = datetime.datetime(year, month, day, hora[0], hora[1])
            return(fecha_clean)
    

def scrapEvents(soup):
    # Obtiene información para todos los eventos incluídos
    # en el objeto beautifulsoup.
    
    eventos = soup.find_all("h4", {"class": "title"})

    # Se crea una tabla con un objeto tipo BeautifulSoup para cada evento
    # y su url correspondiente.
    tabla_eventos_soups = []
    for evento in eventos:
        url_event = "https://www.lagenda.org" + evento.parent.a['href']
        
        if (url_event.split("/")[3] == "programacion"):
            evento_page = requests.get(url_event)
            evento_soup = BeautifulSoup(evento_page.content)
            tabla_eventos_soups.append([evento_soup, url_event])
    
    # Se genera la tabla con los datos de cada evento
    tabla_eventos = []
    for evento in tabla_eventos_soups:
        evento_data = evento[0].find("div", {"class": "summary entry-summary"})
        url_event = evento[1]
        title = evento_data.find_all('h1', {"itemprop": "name"})[0].span.string
        fechas = getDates(evento_data)
        description = evento_data.p.string
        
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

        # Se añade una fila con los datos del evento para cada día
        # que este acontece.
        for i in range(len(fechas)):
            tabla_eventos.append([title, fechas[i], location, description, category,
                                 url_event])

    # Se convierte la tabla a un dataframe de Pandas
    data = pd.DataFrame(tabla_eventos, columns=["title", "date", "location", "description", "category", "url"])
    return(data)

def getEvents(initial_date, end_date, mode="laguna"):
    # Toma las fechas de inicio y fin del periodo sobre el que queremos
    # consultar eventos. Ambas han de ser objetos de tipo datetime.
    # Devuelve un dataframe de Pandas con los datos de los eventos.
    # No incluye la metereología.
    
    lagenda_soup = getPageSoup(initial_date, end_date, mode="laguna")
    data = scrapEvents(lagenda_soup)
    return(data)
