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
    df_raw = pd.DataFrame(parsed["기준금리"], dtype="str")
    df_raw.info()
    print("=" * 40)
    print(df_raw.describe(include="all"))
    print("=" * 40)
    print(df_raw.head(3))


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
