from __future__ import print_function
from http.client import HTTPResponse
from urllib.error import HTTPError

from constants import API_KEY_WEATHER, LAT, LONG

import json
import math
import requests

from flask import Flask
from flask_cors import CORS, cross_origin

import azure.functions as func

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.after_request
@app.route("/recuperar-weather")
def main(req: func.HttpRequest) -> func.HttpResponse:

    arr = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
           'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', ]

    url = 'https://api.openweathermap.org/data/2.5/onecall?lat={0}&lon={1}&exclude=hourly,minutely&appid={2}&lang=es&&units=metric'.format(
        LAT, LONG, API_KEY_WEATHER)

    try:
        respuesta = requests.get(url)

        forecast = respuesta.json()

        respuesta = {
            'ciudad': 'Paterna',
            'icono': forecast['current']['weather']['icon'],
            'hoy':
                {
                    'temperatura': {
                        'temperatura_Actual': forecast['current']['temp'],
                        'sensacion_termica': forecast['current']['feels_like']
                    },
                    'presion_atm': forecast['current']['pressure'],
                    'humedad': forecast['current']['humidity'],
                    'viento': {
                        'velocidad': math.ceil(forecast['current']['wind_speed']),
                        # Transformamos grados 0..360 en una direccion cardinal.
                        'direccion_viento': arr[(forecast['current']['wind_deg']) % 16],
                    },
                    'nubes': forecast['current']['clouds'],
            },
            'prevision_tres_dias':
                {
                    'dia_uno': forecast['daily'][0]['weather'][0]['icon'],
                    'dia_dos': forecast['daily'][1]['weather'][0]['icon'],
                    'dia_tres': forecast['daily'][2]['weather'][0]['icon'],
            }
        }

        return func.HttpResponse(
            json.dumps(respuesta)
        )
    except:
        return func.HttpResponse(
            json.dumps('Error en la llamada a la API de OpenWeather')
        )
