#######################################
# 1. 필요모듈
#######################################
from datetime import datetime

import pandas as pd
from datakart import Datagokr
from dateutil.relativedelta import relativedelta
from tqdm import tqdm

import step_0
import step_1_1

#######################################
# 2. 환경설정
#######################################
API_KEY = "rrRMoK6NHEsLQc4Y2omMvJBTGnaLe8pZzRqAjoGH+mfOerOQtJudgapObiTi2gl07RWrZjO0ie5yryFlMxGV9A=="
STEP_1_2 = step_0.OUTPUT_DIR / "step_1_2.xlsx"


#######################################
# 3. 기본함수
#######################################
def sido_sgg_codes():
    df_region = pd.read_excel(step_1_1.STEP_1_1, dtype="str")
    df_region["sido_sgg"] = df_region["sido_cd"] + df_region["sgg_cd"]

    query = "sgg_cd != '000' and umd_cd == '000' and ri_cd == '00'"
    df_queried = df_region.query(query)
    df_queried.head(3)

    df_filterd = df_queried.filter(["sido_sgg", "locatadd_nm"]).reset_index(drop=True)
    df_filterd.head(3)
    return df_filterd.values.tolist()


def date_range():
    now = datetime.now()
    return sorted([(now - relativedelta(months=idx)).strftime("%Y%m") for idx in range(1, 13)])


#######################################
# 4. 메인함수
#######################################
def main():
    sido_sgg_many = sido_sgg_codes()
    deal_ym_many = date_range()

    api = Datagokr(API_KEY)
    result = []
    for sido_sgg, sido_sgg_nm in tqdm(sido_sgg_many, position=0, leave=False):
        for deal_ym in tqdm(deal_ym_many, position=1, desc=f"[{sido_sgg}][{sido_sgg_nm}]"):
            trans = api.apt_trans(lawd_code=sido_sgg, deal_ym=deal_ym)
            result += trans

    df_result = pd.DataFrame(result)
    df_result.to_excel(STEP_1_2, index=False)


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
