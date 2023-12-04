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

import json
from pprint import pprint

import pandas as pd

parsed = json.loads(response.content)
pprint(parsed)

raw = parsed.get("StanReginCd", [])[-1].get("row", [])
df_raw = pd.DataFrame(raw, dtype="str")
print(df_raw.head(3))

# 행정안전부_행정표준코드_법정동코드 https://www.data.go.kr/data/15077871/openapi.do
