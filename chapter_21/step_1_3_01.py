from pprint import pprint

import requests


def auth():
    url = "https://sgisapi.kostat.go.kr/OpenAPI3/auth/authentication.json"
    params = {
        "consumer_key": "c45c510fe7854d5aae90",
        "consumer_secret": "fde5af5e4362466b91fe",
    }

    resp = requests.get(url, params=params)
    return resp.json().get("result")


def get_hadm_area(token):
    url = "https://sgisapi.kostat.go.kr/OpenAPI3/boundary/hadmarea.geojson"
    params = {
        "accessToken": token,
        "year": "2023",
        "adm_cd": "11",
        "low_search": "1",
    }

    resp = requests.get(url, params=params)
    return resp.json()


access = auth()
geojson = get_hadm_area(access.get("accessToken", ""))
pprint(geojson)


# SGIS https://sgis.kostat.go.kr/developer/html/newOpenApi/api/dataApi/basics.html#auth
