from pprint import pprint

import requests

url = "http://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList"
params = {
    "serviceKey": "rrRMoK6NHEsLQc4Y2omMvJBTGnaLe8pZzRqAjoGH+mfOerOQtJudgapObiTi2gl07RWrZjO0ie5yryFlMxGV9A==",
    "pageNo": "1",
    "numOfRows": "5000",
    "type": "json",
    # "locatadd_nm": "서울특별시",
}

response = requests.get(url, params=params)
response.json()


# https://www.data.go.kr/data/15077871/openapi.do
