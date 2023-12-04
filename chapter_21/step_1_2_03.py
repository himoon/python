import pandas as pd
from datakart import Datagokr

API_KEY = "rrRMoK6NHEsLQc4Y2omMvJBTGnaLe8pZzRqAjoGH+mfOerOQtJudgapObiTi2gl07RWrZjO0ie5yryFlMxGV9A=="

api = Datagokr(API_KEY)
raw = api.apt_trans(lawd_code="11110", deal_ym="201512")
df_raw = pd.DataFrame(raw)
print(df_raw.head(3))

# 국토교통부_아파트매매 실거래자료 https://www.data.go.kr/data/15058747/openapi.do
