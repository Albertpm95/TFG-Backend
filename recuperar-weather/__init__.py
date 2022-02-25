from __future__ import print_function
from http.client import HTTPResponse

from flask import Flask
from flask_cors import CORS, cross_origin

import azure.functions as func

from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps


owm = OWM('9416facf5188cc40fe5ba4f71e2f4f06')
mgr = owm.weather_manager()

api_key = '9416facf5188cc40fe5ba4f71e2f4f06'

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.after_request
@app.route("/recuperar-weather")
def main(req: func.HttpRequest) -> func.HttpResponse:
    observation = mgr.weather_at_place('Paterna,ES')
    w = observation.weather
    w.detailed_status         # 'clouds'
    w.wind()                  # {'speed': 4.6, 'deg': 330}
    w.humidity                # 87

    # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
    w.temperature('celsius')
    w.rain                    # {}
    w.heat_index              # None
    w.clouds                  # 75
    print(w.temperature)

    return 'ok'
