import requests

url = "http://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList"
params = {
    "serviceKey": "rrRMoK6NHEsLQc4Y2omMvJBTGnaLe8pZzRqAjoGH+mfOerOQtJudgapObiTi2gl07RWrZjO0ie5yryFlMxGV9A==",
    "pageNo": "1",
    "numOfRows": "3",
    "type": "json",
    "locatadd_nm": "서울특별시",
}

response = requests.get(url, params=params)
print(response.content)

# 행정안전부_행정표준코드_법정동코드 https://www.data.go.kr/data/15077871/openapi.do
