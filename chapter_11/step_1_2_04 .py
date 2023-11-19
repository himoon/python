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
def get_filtered(raw_data, format="%Y%m%d"):
    df_raw = pd.DataFrame(raw_data, dtype="str")
    df_raw["DATA_VALUE"] = df_raw["DATA_VALUE"].astype("float")
    df_raw["TIME"] = pd.to_datetime(df_raw["TIME"], format=format)
    df_raw.index = df_raw["TIME"]
    return df_raw.filter(["ITEM_NAME1", "UNIT_NAME", "DATA_VALUE"])


#######################################
# 4. 메인함수
#######################################
def main():
    with open(step_1_1.STEP_1_1, "r") as fp:
        parsed = json.load(fp)

    raw_data = parsed["기준금리"]
    df_filtered = get_filtered(raw_data, format="%Y%m%d")
    print(df_filtered.head(2))
    print()
    df_filtered.info()

    with pd.ExcelWriter(STEP_1_2) as writer:
        df_filtered.to_excel(writer, sheet_name="기준금리", index=True)


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
