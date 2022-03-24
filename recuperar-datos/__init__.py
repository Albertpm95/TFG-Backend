from __future__ import print_function
from http.client import HTTPResponse
from urllib.error import HTTPError

import json
import requests

from flask import Flask
from flask_cors import CORS, cross_origin


from constants import DSHBRD_UID_1, DSHBRD_UID_2, URL_GRAFANA, API_KEY_GRAFANA, LOGIN_USR, LOGIN_PSW

import azure.functions as func

app = Flask(__name__)
CORS(app, resources={
     r"/*": {"origins": "*"}})

headers = {
    'Authorization': 'Bearer ' + API_KEY_GRAFANA,
    'login': LOGIN_USR,
    'email': LOGIN_PSW

}
auth = (LOGIN_USR, LOGIN_PSW)

url_1 = URL_GRAFANA + 'api/dashboards/uid/' + DSHBRD_UID_1
url_2 = URL_GRAFANA + 'api/dashboards/uid/' + DSHBRD_UID_1
url_3 = URL_GRAFANA + 'api/dashboards/home'


@app.after_request
@app.route("/recuperar-datos")
def main(req: func.HttpRequest) -> func.HttpResponse:

    try:
        respuesta_1 = requests.get(
            url_1, auth=auth
        )
        respuesta_2 = requests.get(
            url_2, auth=auth
        )
        respuesta_3 = requests.get(
            url_3, auth=auth
        )

        try:
            respuestaJSON_1 = respuesta_1.json()
            respuestaJSON_2 = respuesta_2.json()
            respuestaJSON_3 = respuesta_3.json()
            print(respuestaJSON_1)
            print(respuestaJSON_2)
            print(respuestaJSON_3)

        except:
            print('No se puede mostrar json')

    except:
        print('La llamada a la URL no ha funcionado.')

    return func.HttpResponse(
        json.dumps(respuestaJSON_1)
    )
