#######################################
# 1. 필요모듈
#######################################
import requests

import step_0

#######################################
# 2. 환경설정
#######################################
STEP_2_1 = step_0.OUTPUT_FOLDER / "step_2_1.xls"


#######################################
# 3. 기본함수
#######################################
pass


#######################################
# 4. 메인함수
#######################################
def main():
    req_url = "https://finlife.fss.or.kr/finlife/cmmn/file/clipFileDown.do?crfName=deposit_List&crfParams=PAGETYPE:AJAX|MENUNO:700002|PAGEINDEX:1|PAGESIZE:10|PAGEUNIT:10|TOTAL:0|SAVETRM:12|AREATYPE:01%2C02%2C03%2C04%2C05%2C06%2C07%2C08%2C09%2C10%2C11%2C12%2C13%2C14%2C15%2C16%2C17|TOPFINGRPNO:020000|AREACDNM:%EC%A0%84%EC%B2%B4|TOPFINGRPNONM:%EC%A0%84%EC%B2%B4|JOINDENY:1|JOINDENYNM:%EC%A0%9C%ED%95%9C%EC%97%86%EC%9D%8C|INTRRATETYPE:S|INTRRATETYPENM:%EC%A0%84%EC%B2%B4|JOINWAY:1%2C2%2C3%2C4%2C5%2C9|JOINWAYNM:%EC%A0%84%EC%B2%B4|SPCLCNDCD:|SPCLCNDNM:%EC%A0%84%EC%B2%B4|INPUTMONEY:10000000|SEARCHKEYWORD:|SEARCHCONDITION:|INTRRATETYPE:S|LISTORDER:INTRRATEDESC|LOGADD:|MENUID:2000100|SEARCHFOCUS:1|BLTN_ID:BB000000000000000135&crfDownloadType=EXCEL&itemType=deposit"
    resp = requests.get(req_url)
    if resp.status_code == 200:
        with open(STEP_2_1, "wb") as fp:
            fp.write(resp.content)
    else:
        raise ValueError(f"invalid status_code, got {resp.status_code!r}")


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
