# -*- coding: utf-8 -*-
"""
Pruebas de webscrapping
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Captura la página entera
lagenda_page = requests.get("https://lagenda.org/programacion/planfinde")

# Ver el código de estado de la captura
lagenda_page.status_code

# Pasar el contenido de la pag por BeautifulSoup
soup = BeautifulSoup(lagenda_page.content)

# Muestra todo el contenido capturado
soup.prettify

# Muestra todos los enlaces de soup
soup.find_all('a')

# Muestra la primera etiqueta que contenga "title"
soup.find("title")

# Crea un objeto con todas las etiquetas que contengan "title"
titulos = soup.find_all("title")

# Encuentra todos los títulos h4
soup.find_all('h4')

# Las etiquetas h4 con class="title" contienen los títulos de los eventos
eventos = soup.find_all("h4", {"class": "title"})

# Ejemplo de etiqueta h4 capturada
eventos[3]

# Seleccionamos sólo el enlace
eventos[3].a

# Seleccionamos solo el nombre del enlace
eventos[3].a.string

# Imprimir títulos de eventos
counter = 1
for evento in eventos:
    print(counter)
    print(evento.a.string)
    counter = counter + 1

# Se ve que en el caso de lagenda.org existe un <div> que incluye a todo el
# evento y es un nivel superior a las etiquetas h4 que hemos detectado.

# Para imprimir todo el nivel superior usamos el sufijo .parent
eventos[3].parent

# Tabla con nombres y títulos de eventos
tabla_eventos = []
for evento in eventos:
    name = evento.a.string
    full_event = evento.parent    # Categoría que contiene todo el evento.
    categ = full_event.find("div", {"class": "post-category"}).a.string
    tabla_eventos.append([name, categ])

# Convertir la tabla a un dataframe de Pandas
data = pd.DataFrame(tabla_eventos, columns=["Nombre", "Categoría"])

print(data.head())
