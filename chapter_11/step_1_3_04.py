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
ROWS = 100


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
        df_raw["DATA_MAX"] = df_raw["DATA_VALUE"].max()
        df_raw["DATA_MIN"] = df_raw["DATA_VALUE"].min()

        y_value = df_raw["DATA_VALUE"]
        y_max = df_raw["DATA_MAX"]
        y_min = df_raw["DATA_MIN"]
        x_index = df_raw.index

        axes = y_value.plot(figsize=(9, 3))
        axes.fill_between(x=x_index, y1=y_value, y2=y_max, color="blue", alpha=0.25)
        axes.fill_between(x=x_index, y1=y_value, y2=y_min, color="red", alpha=0.75)

        axes.set_xlim(x_index.min(), x_index.max())
        axes.set_ylim(y_value.min(), y_value.max())
        axes.set_axis_off()

        fig = axes.get_figure()
        fig.set_tight_layout(True)
        fig.savefig(STEP_1_3.as_posix().format(key))
        plt.show()


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
