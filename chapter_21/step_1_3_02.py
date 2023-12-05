from pprint import pprint

from datakart import Sgis

API_KEY = "c45c510fe7854d5aae90"
API_SEC = "fde5af5e4362466b91fe"
api = Sgis(API_KEY, API_SEC)
geojson = api.hadm_area(year="2023", adm_cd="11", low_search="1")
pprint(geojson)

# SGIS https://sgis.kostat.go.kr/developer/html/newOpenApi/api/dataApi/basics.html#auth
