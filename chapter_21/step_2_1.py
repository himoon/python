#######################################
# 1. 필요모듈
#######################################
import pandas as pd

import step_0
import step_1_2

#######################################
# 2. 환경설정
#######################################
STEP_2_1 = step_0.OUTPUT_FOLDER / "step_2_1.xlsx"


#######################################
# 3. 기본함수
#######################################
pass


#######################################
# 4. 메인함수
#######################################
def main():
    df_raw = pd.read_excel(step_1_2.STEP_1_2, dtype="str")

    df_copied = df_raw.copy()
    df_copied["월"] = df_copied["월"].str.pad(width=2, side="left", fillchar="0")
    df_copied["거래년월"] = df_copied["년"] + df_copied["월"]

    df_copied["거래금액"] = df_copied["거래금액"].str.replace(",", "")
    df_copied = df_copied.astype({"거래금액": "float", "전용면적": "float"})
    df_copied["면적당금액"] = df_copied["거래금액"] / df_copied["전용면적"]

    not_cancelled = df_copied["해제여부"].isna()
    is_brokerage = df_copied["거래유형"] == "중개거래"
    df_sliced = df_copied.loc[not_cancelled & is_brokerage]

    sido_sgg_codes = step_1_2.sido_sgg_codes()
    df_sido_sgg = pd.DataFrame(sido_sgg_codes, columns=["지역코드", "지역명"])

    df_merged = pd.merge(df_sliced, df_sido_sgg, on="지역코드", how="inner")
    df_filtered = df_merged.filter(["지역명", "지역코드", "거래년월", "거래금액", "전용면적", "면적당금액", "아파트"])
    df_sorted = df_filtered.sort_values(["지역명", "거래년월", "면적당금액", "아파트"], ascending=[True, True, False, True])
    df_groupped = df_sorted.groupby(["지역명", "지역코드"])
    df_result = df_groupped["면적당금액"].mean().to_frame().reset_index(drop=False)

    with pd.ExcelWriter(STEP_2_1) as writer:
        df_sido_sgg.to_excel(writer, sheet_name="sido_sgg", index=False)
        df_raw.to_excel(writer, sheet_name="raw", index=False)
        df_sorted.to_excel(writer, sheet_name="sorted", index=False)
        df_result.to_excel(writer, sheet_name="result", index=False)


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
