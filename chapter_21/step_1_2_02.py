import requests

url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade"
params = {
    "serviceKey": "rrRMoK6NHEsLQc4Y2omMvJBTGnaLe8pZzRqAjoGH+mfOerOQtJudgapObiTi2gl07RWrZjO0ie5yryFlMxGV9A==",
    "LAWD_CD": "11110",
    "DEAL_YMD": "201512",
}

response = requests.get(url, params=params)

import pandas as pd
import xmltodict

parsed = xmltodict.parse(response.content)
df_raw = pd.DataFrame(parsed["response"]["body"]["items"]["item"])
print(df_raw.head(3))

# 국토교통부_아파트매매 실거래자료 https://www.data.go.kr/data/15058747/openapi.do
