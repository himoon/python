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


my_request = [
    ["기준금리", "M", "722Y001", "0101000", 1],
    ["국고채", "D", "817Y002", "010200000", 1],
]
for args in my_request:
    name, intv, code0, code1, rows = args
    start, end = get_date_start_end(intv=intv, rows=rows)
    service = f"StatisticSearch/{API_KEY}/json/kr/"
    params = f"1/{rows}/{code0}/{intv}/{start}/{end}/{code1}"
    req_url = API_URL + service + params
    print(req_url)

    resp = requests.get(req_url)
    parsed = resp.json()
    pprint(parsed)
