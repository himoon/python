from datetime import datetime
from pprint import pprint

import requests
from dateutil.relativedelta import relativedelta

API_KEY = "sample"  # 여러분의 API 인증키로 바꿔주세요.
API_URL = "http://ecos.bok.or.kr/api/"


def get_date_start_end(intv="D", rows=100):
    if intv == "D":
        dt_end = datetime.now() - relativedelta(days=1)
        dt_start = dt_end - relativedelta(days=rows - 1)
        return dt_start.strftime("%Y%m%d"), dt_end.strftime("%Y%m%d")
    elif intv == "M":
        dt_end = datetime.now() - relativedelta(months=1)
        dt_start = dt_end - relativedelta(months=rows - 1)
        return dt_start.strftime("%Y%m"), dt_end.strftime("%Y%m")


intv = "M"
rows = 2
start, end = get_date_start_end(intv=intv, rows=rows)

code0 = "722Y001"
code1 = "0101000"
service = f"StatisticSearch/{API_KEY}/json/kr/"
params = f"1/{rows}/{code0}/{intv}/{start}/{end}/{code1}"
req_url = API_URL + service + params
print(req_url)

resp = requests.get(req_url)
parsed = resp.json()
pprint(parsed)

code0 = "721Y001"  # 월별 국고채(3년) 데이터의 통계표코드
code1 = "5020000"  # 월별 국고채(3년) 데이터의 통계항목코드
service = f"StatisticSearch/{API_KEY}/json/kr/"
params = f"1/{rows}/{code0}/{intv}/{start}/{end}/{code1}"
req_url = API_URL + service + params
print(req_url)

resp = requests.get(req_url)
parsed_2 = resp.json()
pprint(parsed_2)
