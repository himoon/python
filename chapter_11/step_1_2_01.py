#######################################
# 1. 필요모듈
#######################################
import json
from pprint import pprint

import pandas as pd

import step_0
import step_1_1

#######################################
# 2. 환경설정
#######################################
STEP_1_2 = step_0.OUTPUT_FOLDER / "step_1_2.xlsx"


#######################################
# 3. 기본함수
#######################################
pass


#######################################
# 4. 메인함수
#######################################
def main():
    with open(step_1_1.STEP_1_1, "r") as fp:
        parsed = json.load(fp)

    keys = parsed.keys()
    print(keys)
    for key in keys:
        rows = parsed.get(key, {})
        print(f"{key} 데이터 수: {len(rows)}")
        print(f"{key} 컬럼명: {rows[0].keys()}")
        pprint(rows[0])
        print("=" * 40)


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
