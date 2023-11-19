#######################################
# 1. 필요모듈
#######################################
import matplotlib.pyplot as plt
import pandas as pd

import step_0
import step_1_2

#######################################
# 2. 환경설정
#######################################
STEP_1_3 = step_0.OUTPUT_FOLDER / "step_1_3_{}.png"
ROWS = 30


#######################################
# 3. 기본함수
#######################################
pass


#######################################
# 4. 메인함수
#######################################
def main():
    with pd.ExcelFile(step_1_2.STEP_1_2) as xlsx:
        print(f"엑셀 시트이름: {xlsx.sheet_names}")

        key = "코스피지수"
        df_raw = xlsx.parse(key, index_col="TIME")
        axes = df_raw["DATA_VALUE"].plot()
        fig = axes.get_figure()
        fig.savefig(STEP_1_3.as_posix().format(key))
        plt.show()


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
