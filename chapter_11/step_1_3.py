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

        for key in xlsx.sheet_names:
            df_raw = xlsx.parse(key, index_col="TIME")
            df_raw = df_raw.tail(ROWS)

            df_raw["DATA_MAX"] = df_raw["DATA_VALUE"].max()
            df_raw["DATA_MIN"] = df_raw["DATA_VALUE"].min()

            y_value = df_raw["DATA_VALUE"]
            y_max = df_raw["DATA_MAX"] * 1.02
            y_min = df_raw["DATA_MIN"] * 0.98
            x_index = df_raw.index

            change = y_value.iloc[-1] - y_value.iloc[0]
            color = "red" if change > 0 else "blue" if change < 0 else "black"
            params = dict(x=x_index, color=color, alpha=0.10)

            axes = y_value.plot(figsize=(9, 3), color=color, linewidth=5)
            if change > 0:
                axes.fill_between(y1=y_value, y2=y_min, **params)
            elif change < 0:
                axes.fill_between(y1=y_value, y2=y_max, **params)
            else:
                axes.fill_between(y1=y_min, y2=y_max, **params)

            axes.set_xlim(x_index.min(), x_index.max())
            axes.set_ylim(y_min.iloc[0], y_max.iloc[0])
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
