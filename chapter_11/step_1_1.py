#######################################
# 1. 필요모듈
#######################################
import json
from datetime import datetime
from time import sleep

import requests
from dateutil.relativedelta import relativedelta
from tqdm import tqdm

import step_0

#######################################
# 2. 환경설정
#######################################
API_KEY = "9NPPLWUVZGMSFQP0CL23"
API_URL = "http://ecos.bok.or.kr/api/"
STEP_1_1 = step_0.OUTPUT_FOLDER / "step_1_1.json"


#######################################
# 3. 기본함수
#######################################
def get_date_start_end(intv="D", rows=100):
    dt_base = datetime.now() - relativedelta(days=1)
    if intv == "D":
        dt_start = dt_base - relativedelta(days=rows)
        return dt_start.strftime("%Y%m%d"), dt_base.strftime("%Y%m%d")
    elif intv == "M":
        dt_start = dt_base - relativedelta(months=rows)
        return dt_start.strftime("%Y%m"), dt_base.strftime("%Y%m")
    elif intv == "A":
        dt_start = dt_base - relativedelta(years=rows)
        return dt_start.strftime("%Y"), dt_base.strftime("%Y")
    raise ValueError(f"invalid interval, got {intv!r}")


def get_query_string(args):
    _, code0, code1, intv, rows = args
    date_start, date_end = get_date_start_end(intv=intv, rows=rows)
    params = {
        "서비스명": "StatisticSearch",  # API서비스명
        "인증키": API_KEY,  # 오픈API 인증키
        "요청유형": "json",  # 결과값의 파일 형식
        "언어구분": "kr",  # 결과값의 언어 - kr(국문), en(영문)
        "요청시작건수": "1",  # 전체 결과값 중 시작 번호
        "요청종료건수": f"{rows}",  # 전체 결과값 중 끝 번호
        "통계표코드": code0,  # 통계표코드
        "주기": intv,  # 주기(년:A, 반년:S, 분기:Q, 월:M, 반월:SM, 일: D)
        "검색시작일자": date_start,  # 검색시작일자(202401, 20240101 등)
        "검색종료일자": date_end,  # 검색종료일자(202412, 20241231 등)
        "통계항목코드1": code1,  # 통계항목코드1(옵션)
        "통계항목코드2": "?",  # 통계항목코드2(옵션)
        "통계항목코드3": "?",  # 통계항목코드3(옵션)
        "통계항목코드4": "?",  # 통계항목코드4(옵션)
    }
    return "/".join(params.values())


#######################################
# 4. 메인함수
#######################################
def main():
    my_request = [
        ("기준금리M", "722Y001", "0101000", "M", 100),
        ("기준금리", "722Y001", "0101000", "D", 100),
        ("국고채", "817Y002", "010200000", "D", 100),
        ("회사채", "817Y002", "010300000", "D", 100),
        ("코스피지수", "802Y001", "0001000", "D", 100),
        ("원/달러환율", "731Y001", "0000001", "D", 100),
    ]

    dumped = {}
    for args in tqdm(my_request):
        resp = requests.get(f"{API_URL}{get_query_string(args)}")
        status_code = resp.status_code
        if status_code == 200:
            jsoned = resp.json()
            result = jsoned.get("StatisticSearch", {}).get("row", [])
            dumped[args[0]] = result
        else:
            raise ValueError(f"invalid status_code, got {status_code!r}")
        sleep(1)

    with open(STEP_1_1, "w") as fp:
        json.dump(dumped, fp, ensure_ascii=False)


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
