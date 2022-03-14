from __future__ import print_function
from http.client import HTTPResponse
from urllib.error import HTTPError

import json
import requests

from flask import Flask
from flask_cors import CORS, cross_origin


from constants import DSHBRD_1, DSHBRD_2, URL_GRAFANA, API_KEY_GRAFANA, LOGIN_USR, LOGIN_PSW

import azure.functions as func

app = Flask(__name__)
CORS(app, resources={
     r"/*": {"origins": "*"}})

headers = {
    'Authorization': 'Bearer ' + API_KEY_GRAFANA,
}
auth = (LOGIN_USR, LOGIN_PSW)

url_1 = URL_GRAFANA + 'api/dashboards/uid/' + DSHBRD_1
url_2 = URL_GRAFANA + 'api/dashboards/uid/' + DSHBRD_2


@app.after_request
@app.route("/recuperar-datos")
def main(req: func.HttpRequest) -> func.HttpResponse:

    try:
        respuesta = requests.get(
            url_1, auth=auth
        )

        try:
            respuestaJSON = respuesta.json()
            print(respuestaJSON)

            with open('respuestaJSON.txt', 'w') as rJson:
                rJson.write(respuestaJSON)

        except:
            print('No se puede mostrar json')

        try:
            request = respuesta.request
            with open('request.txt', 'w') as a:
                a.write(request)
        except:
            print('No se puede mostrar request')

        try:
            headers = respuesta.headers
            with open('headers.txt', 'w') as b:
                b.write(headers)
        except:
            print('No se puede mostrar headers')

        try:
            content = respuesta.content
            with open('content.txt', 'w') as c:
                c.write(content)
        except:
            print('No se puede mostrar content')
    except:
        print('La llamada a la URL no ha funcionado.')

    return 'ok'
