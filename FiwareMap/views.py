from django.http import request, HttpRequest, JsonResponse
from django.shortcuts import render
import requests
import json

# Datos para acceder a la plataforma FIWARE
servicio = 'smart_campus_uma'
subservicio = '/fraterni_lab'
user = 'usr_fraterni_lab'
password = 'TVBjMdCd'

# Url plataforma FIWARE
urlPlataforma = 'https://150.214.58.178'

# url para pedir token
puertoToken = ':6001'
pathToken = '/v3/auth/tokens'

# url para pedir todas las entidades
puertoEntidades = ':2026'
pathEntidades = '/v2/entities'
opcionesEntidades = '?limit=1000&options=count'


def obtenerToken():
    data = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": servicio
                        },
                        "name": user,
                        "password": password
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "name": servicio
                    },
                    "name": subservicio
                }
            }
        }
    }
    urlToken = urlPlataforma + puertoToken + pathToken
    r = requests.post(urlToken, data=JsonResponse(data), headers={'Content-Type': 'application/json'}, verify=False)

    return r.headers.get('X-Subject-Token')


def pedirEntidades(token):
    urlEntidades = urlPlataforma + puertoEntidades + pathEntidades + opcionesEntidades
    headersEntidades = {'Fiware-Service': 'smart_campus_uma', 'Fiware-ServicePath': '/fraterni_lab',
                        'X-Auth-Token': token
                        }
    # verify = False para saltarse el tema de los certificados

    return requests.get(urlEntidades, headers=headersEntidades, verify=False)


def mostrarMapa(request):
    # 1 - pedimos el token
    token = obtenerToken()
    # print('token = ' + token)

    # 2 - Pedimos las entidades que vamos a mostrar en el mapa
    entidades = pedirEntidades(token)
    # print('respuesta: ' + entidades.text)

    return JsonResponse(entidades.json(), safe=False)
