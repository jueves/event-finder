# Práctica 1: Web scraping

## Contexto

Usualmente, cuando vamos a algún tipo de evento cultural, en los días previos al mismo verificamos las condiciones meteorológicas previstas en diferentes webs o en app disponibles en nuestro smartphone. Esta información nos permite resolver preguntas del tipo: ¿qué medio de transporte uso? ¿qué tipo de ropa he de llevar?

Además, para los que vivimos en regiones con climas muy cambiantes como en las Islas Canarias, esta información se vuelve más necesaria. Es por ello, que consideramos de gran utilidad tener toda esta información en el mismo lugar.

Las dos webs usadas permiten construir este data set, centrándonos en los eventos que se anuncian en la web [La Agenda](https://lagenda.org) y en las previsiones meteorológicas aportadas por la [AEMET](https://opendata.aemet.es/centrodedescargas/inicio).
También se han obtenido datos a [Google Maps](https://cloud.google.com/maps-platform/) y del proyecto [DS Códigos Postales INE](https://github.com/inigoflores/ds-codigos-postales-ine-es/) para relacionar los lugares de La Agenda con los datos de AEMET.


## Título para el data set

Datos de eventos y condiciones meteorológicas esperadas

## Descripción del data set

Para dar respuesta a esta necesidad, el data set está compuesto de las variables principales referentes al evento: fecha, descripción, hora, municipio donde se celebra,... y datos referentes a las condiciones meteorológicas esperadas: temperatura, estado del cielo y probabilidad de lluvia.

## Representación gráfica

## Contenido

Para cada evento, el cual se corresponde con un registro en el conjunto de datos, se recogen las siguientes variables:

* **title**: título del evento. Str.
* **date**: día en el que se celebra el evento, en el formato dd/mm/aaa.  
* **location**: lugar donde se celebra el evento. Str.
* **catrgory**: categoría en la que se engloba el evento. Str.  
* **url**: url en la que se publica el evento. Str.  
* **estadoCielo**: recoge el estado del cielo el día del evento. Predicción 00-24. Vacío en caso de estar despejado o no tener predicción disponible. Str.
* **probPrecipitacion**: recoge la probabilidad de que produzcan precipitaciones. Predicción 00-24. Int.
* **sensTermMax**: recoge la sensación térmica máxima el día del evento. Int.
* **sensTermMin**: recoge la sensación térmica mínima el día del evento. Int.
* **temperaturaMax**: recoge la temperatura máxima el día del evento. Int.
* **temperaturaMin**: recoge la temperatura mínima el día del evento. Int.

Los datos del evento (**title, date, location, catrgory, url**) se obtienen con los paquetes *BeautifulSoup* y *Request*.
Los datos de predicción meteorológica (**estadoCielo, probPrecipitacion, sensTermMax, sensTermMin, temperaturaMax, temperaturaMin**) se obtienen a través de la API de la **AEMET**, ayudados de los paquetes *http.client* y *ssl*.

Además de los paquetes anteriores, se utilizan otras librerías como *Pandas* o *Datetime*

En cuanto al periodo de tiempo,

## Agredecimientos

La información ha sido recopilada de diferentes fuentes:

### [La Agenda](https://lagenda.org)
 y a través de la API de la [AEMET](https://opendata.aemet.es/dist/index.html?#!/predicciones-especificas/Predicci%C3%B3n_por_municipios_diaria_Tiempo_actual). Para los datos de los eventos, se ha hecho uso del lenguaje de programación Python y de técnicas de *Web Scraping* para extraer la información alojada en las páginas HTML. Para los datos de la AEMET, se ha hecho uso de la API de la AEMET, donde se indican todos los pasos a seguir para hacer un buen uso de ella.
Los datos han sido recolectados desde la web [La Agenda](https://lagenda.org) y a través de la API de la [AEMET](https://opendata.aemet.es/dist/index.html?#!/predicciones-especificas/Predicci%C3%B3n_por_municipios_diaria_Tiempo_actual). Para los datos de los eventos, se ha hecho uso del lenguaje de programación Python y de técnicas de *Web Scraping* para extraer la información alojada en las páginas HTML. Para los datos de la AEMET, se ha hecho uso de la API de la AEMET, donde se indican todos los pasos a seguir para hacer un buen uso de ella.

Se desconoce si han habido iniciativas similares a esta, pero si son numerosos los estudios en los que se relaciona una variable endógena con variables exógenas, como las condiciones meteorológicas.

## Inspiración

Como comentado en el contexto, la intención es poder cubrir la necesidad que tienen los espectadores de los eventos publicados en la web [La Agenda](https://lagenda.org) de conocer con anticipación las condiciones meteorológicas esperadas en la fecha de dicho evento.

Sin embargo, esta no es la única utilidad que se le podría dar a este proyecto. Tanto los cuerpos de seguridad como los medios de transporte público podrían estar interesados en esta información. Por ejemplo, si se trata de un evento de exterior y se esperan condiciones de tormenta, esto incrementa la probabilidad de que se produzcan inundaciones, con lo que tendrán que prestar más atención a este evento, debido a la concentración de público.

Otra aplicabilidad de este data set sería poder hacer un estudio de la relación que existe entre la venta de entradas para un evento y las condiciones meteorológicas previstas. Este análisis permitiría estimar a los organizadores del evento la afluencia de público y, en consecuencia, dimensionar los servicios acordes con el público esperado.


## Licencia

## Código y Dataset

Tanto el código como el data set se pueden encontrar en el repositorio de Github siguiente:

## Contribuciones

Investigación previa: Luis Cobiella y Jonay Velázquez

Redacción de las respuestas: Luis Cobiella y Jonay Velázquez

Desarrollo código: Luis Cobiella y Jonay Velázquez
