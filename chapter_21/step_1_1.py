# 국토교통부_아파트매매 실거래 상세 자료
# https://www.data.go.kr/data/15057511/openapi.do

import requests

url = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev"
params = {
    "serviceKey": "rrRMoK6NHEsLQc4Y2omMvJBTGnaLe8pZzRqAjoGH%2BmfOerOQtJudgapObiTi2gl07RWrZjO0ie5yryFlMxGV9A%3D%3D",
    "pageNo": "1",
    "numOfRows": "10",
    "LAWD_CD": "11110",
    "DEAL_YMD": "201512",
}

response = requests.get(url, params=params)
print(response.content)
