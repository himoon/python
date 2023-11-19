#######################################
# 1. 필요모듈
#######################################
import json
import time
from datetime import datetime

import requests
from dateutil.relativedelta import relativedelta

#######################################
# 2. 환경설정
#######################################
API_KEY = "9NPPLWUVZGMSFQP0CL23"  # 여러분의 API 인증키로 바꿔주세요.
API_URL = "http://ecos.bok.or.kr/api/"


#######################################
# 3. 기본함수
#######################################
def get_date_start_end(intv="D", rows=100):
    if intv == "D":
        dt_end = datetime.now() - relativedelta(days=1)
        dt_start = dt_end - relativedelta(days=rows - 1)
        return dt_start.strftime("%Y%m%d"), dt_end.strftime("%Y%m%d")
    elif intv == "M":
        dt_end = datetime.now() - relativedelta(months=1)
        dt_start = dt_end - relativedelta(months=rows - 1)
        return dt_start.strftime("%Y%m"), dt_end.strftime("%Y%m")


#######################################
# 4. 메인함수
#######################################
def main():
    my_request = [
        ["기준금리M", "M", "722Y001", "0101000", 100],
        ["기준금리", "D", "722Y001", "0101000", 100],
        ["국고채", "D", "817Y002", "010200000", 100],
        ["회사채", "D", "817Y002", "010300000", 100],
        ["코스피지수", "D", "802Y001", "0001000", 100],
        ["원/달러환율", "D", "731Y001", "0000001", 100],
    ]
    dumped = {}
    for args in my_request:
        name, intv, code0, code1, rows = args
        start, end = get_date_start_end(intv=intv, rows=rows)
        service = f"StatisticSearch/{API_KEY}/json/kr/"
        params = f"1/{rows}/{code0}/{intv}/{start}/{end}/{code1}"
        req_url = API_URL + service + params
        print(f"{name} 입력값 : {params}")

        resp = requests.get(req_url)
        parsed = resp.json()
        dumped[name] = parsed.get("StatisticSearch", {}).get("row", [])
        time.sleep(0.5)

    with open("step_1_1.json", "w") as fp:
        json.dump(dumped, fp, ensure_ascii=False)


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    main()
