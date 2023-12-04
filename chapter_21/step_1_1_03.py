import pandas as pd
from datakart import Datagokr

API_KEY = "rrRMoK6NHEsLQc4Y2omMvJBTGnaLe8pZzRqAjoGH+mfOerOQtJudgapObiTi2gl07RWrZjO0ie5yryFlMxGV9A=="

api = Datagokr(API_KEY)
raw = api.lawd_code(region="서울특별시")
df_raw = pd.DataFrame(raw)
print(df_raw.head(3))

# 행정안전부_행정표준코드_법정동코드 https://www.data.go.kr/data/15077871/openapi.do
