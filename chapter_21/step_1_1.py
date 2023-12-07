#######################################
# 1. 필요모듈
#######################################
import pandas as pd
from datakart import Datagokr

import step_0

#######################################
# 2. 환경설정
#######################################
API_KEY = "rrRMoK6NHEsLQc4Y2omMvJBTGnaLe8pZzRqAjoGH+mfOerOQtJudgapObiTi2gl07RWrZjO0ie5yryFlMxGV9A=="
STEP_1_1 = step_0.OUTPUT_DIR / "step_1_1.xlsx"


#######################################
# 3. 기본함수
#######################################
pass


#######################################
# 4. 메인함수
#######################################
def main():
    api = Datagokr(API_KEY)
    raw = api.lawd_code(region="서울특별시")
    df_raw = pd.DataFrame(raw, dtype="str")
    df_raw.sort_values("region_cd").reset_index(drop=True).to_excel(STEP_1_1, index=False)


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
