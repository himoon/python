#######################################
# 1. 필요모듈
#######################################
import json

from sgis import Sgis

import step_0

#######################################
# 2. 환경설정
#######################################
API_KEY = "c45c510fe7854d5aae90"
API_SEC = "fde5af5e4362466b91fe"
STEP_1_3 = step_0.OUTPUT_FOLDER / "step_1_3.geojson"


#######################################
# 3. 기본함수
#######################################
pass


#######################################
# 4. 메인함수
#######################################
def main():
    api = Sgis(API_KEY, API_SEC)
    resp = api.hadm_area(year="2023", adm_cd="11", low_search="2")
    with open(STEP_1_3, "w") as fp:
        json.dump(resp, fp, ensure_ascii=False)


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
