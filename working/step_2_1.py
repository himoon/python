# 국토교통부_아파트매매 실거래자료
# https://www.data.go.kr/data/15058747/openapi.do


import requests

import step_0

url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade"
params = {
    "serviceKey": step_0.API_KEY_DATA_GO,
    "LAWD_CD": "11110",
    "DEAL_YMD": "201512",
}

response = requests.get(url, params=params)
print(response.content)
