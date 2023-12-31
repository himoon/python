#######################################
# 1. 필요모듈
#######################################
import pandas as pd

import step_0
import step_2_1

#######################################
# 2. 환경설정
#######################################
STEP_2_2 = step_0.OUTPUT_FOLDER / "step_2_2.xlsx"


#######################################
# 3. 기본함수
#######################################
pass


#######################################
# 4. 메인함수
#######################################
def main():
    df_deposit = pd.read_excel(step_2_1.STEP_2_1)
    df_deposit.columns = [col.strip().replace("\n", "") for col in df_deposit.columns]

    for col in ["세전이자율", "세후이자율", "세후이자", "최고우대금리"]:
        df_deposit[col] = df_deposit[col].str.replace("%", "e-2")
        df_deposit[col] = df_deposit[col].str.replace(",", "")
        df_deposit[col] = df_deposit[col].astype(float)

    with pd.ExcelWriter(STEP_2_2) as writer:
        df_deposit.to_excel(writer, sheet_name="deposit", index=False)


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
