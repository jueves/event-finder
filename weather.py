import datetime
from darksky.api import DarkSky
from darksky.types import languages, units, weather


# Usamos la API de Dark Sky que nos permite ver la predicción del tiempo en el día en curso hasta un horizonte de 7 días, 
# tomando como parámetro de entrada las coordenadas del lugar y la fecha del evento. Los datos se actualizan continuamente.

#Por seguridad, mantenemos la clave para poder usar la API en un fichero externo

class Weather:
    darksky_key = ""
    # Se crea un archivo de previsiones para cada localización y día.
    # Con esto reducimos las llamadas a la API.
    # Se incluye una entrada para los casos en que no sea posible 
    # devolver una predicción.
    weather_dic = {'non_available': {'estadoCielo': 999,
                                     'probPrecipitacion': 999,
                                     'sensTermMax': 999,
                                     'sensTermMin': 999,
                                     'temperaturaMax': 999,
                                     'temperaturaMin': 999,}}
   
    def __init__(self, darksky_key):
        self.darksky_key = darksky_key
        # Se crea un objeto darksky con la clave de la API.
        self.darksky = DarkSky(darksky_key)
        
    def getDictionary(self):
        return(self.weather_dic)
        
    def getWeather(self, location, date):
        # Recibe una lista con las coordenadas de un lugar y un objeto datetime.datetime
        # con el día sobre el que se quiere la predicción.
        # Devuelve un diccionario con la previsisión para dicho día.
        
        # Trabajaremos sólo con días, convertimos el datetime.datime a datetime.date
        date = date.date()
        
        # Fijamos la predicción por defecto
        prediction = self.weather_dic['non_available']
        
        
        # Comprobamos si existe predicción para el municipio
        # Dado que las predicciones sólo se almacenan durante la ejecución del
        # programa, estas se actualizarán en cada ejecución del mismo.
        archived_prediction = False
        
        # Calcula si la fecha está en el rango que podemos obtener.
        exists_prediction = date < datetime.date.today() + datetime.timedelta(days=7)
        
        # Cuando hay un error en la localización esta adopta el valor 0
        if location==[0]:
            exists_prediction = False
        
        location_key = str(location)
        
        if exists_prediction and location_key in self.weather_dic.keys():
            if date in self.weather_dic[location_key].keys():
                archived_prediction = True
                prediction = self.weather_dic[location_key][date]
        
        if exists_prediction and not archived_prediction:
            # Obtenemos los datos de Dark Sky para toda la semana en location
            forecast = self.darksky.get_forecast(
                    location[0], location[1],
                    extend=False, # default `False`
                    lang=languages.ENGLISH, # default `ENGLISH`
                    units=units.AUTO, # default `auto`
                    exclude=[weather.MINUTELY, weather.ALERTS] # default `[]`
                    )
            
            # Extraemos los datos de interés y los almacenamos en forma de
            # diccionario.
            location_prediction = {}
            for day in forecast.daily.data:
                day_prediction = {'estadoCielo': day.cloud_cover,
                                  'probPrecipitacion': day.precip_probability,
                                  'sensTermMax': day.apparent_temperature_max,
                                  'sensTermMin': day.apparent_temperature_min,
                                  'temperaturaMax': day.temperature_max,
                                  'temperaturaMin': day.temperature_min,}
                
                location_prediction[day.time.date()] = day_prediction
            
            # Actualizamos el diccionario principal
            self.weather_dic.update({location_key: location_prediction})
            
            # Nos asguramos de que disponemos de los dato y los devolvemos.
            if date in location_prediction.keys():
                prediction = location_prediction[date]
    
        return(prediction)
