##############################################################################
# 1. 필요모듈
##############################################################################
import json
import pandas as pd


##############################################################################
# 2. 환경설정
##############################################################################
STEP_1_1 = "output/step_1_1.json"
STEP_2_1 = "output/step_1_2.xlsx"


##############################################################################
# 3. 기본함수
##############################################################################
def get_filtered(raw, format):
    df_raw = pd.DataFrame(raw, dtype=str)
    df_raw["DATA_VALUE"] = df_raw["DATA_VALUE"].astype("float")
    df_raw.index = pd.to_datetime(df_raw["TIME"], format=format)
    return df_raw.filter(["ITEM_NAME1", "UNIT_NAME", "DATA_VALUE"])


##############################################################################
# 4. 메인함수
##############################################################################
def main():
    with open(STEP_1_1, "r") as fp:
        jsoned = json.load(fp)

    base_mo = jsoned.get("기준금리M", [])
    df_base_mo = get_filtered(base_mo, "%Y%m")
    df_base = get_filtered(jsoned.get("기준금리", []), "%Y%m%d")
    df_tb = get_filtered(jsoned.get("국고채", []), "%Y%m%d")
    df_cb = get_filtered(jsoned.get("회사채", []), "%Y%m%d")
    df_kospi = get_filtered(jsoned.get("KOSPI", []), "%Y%m%d")
    df_ex = get_filtered(jsoned.get("원달러환율", []), "%Y%m%d")

    with pd.ExcelWriter(STEP_2_1) as writer:
        df_base_mo.to_excel(writer, sheet_name="base_mo", index=True)
        df_base.to_excel(writer, sheet_name="base", index=True)
        df_tb.to_excel(writer, sheet_name="tb", index=True)
        df_cb.to_excel(writer, sheet_name="cb", index=True)
        df_kospi.to_excel(writer, sheet_name="kospi", index=True)
        df_ex.to_excel(writer, sheet_name="ex", index=True)


##############################################################################
# 5. 실행
##############################################################################
if __name__ == "__main__":
    main()
