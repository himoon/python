##############################################################################
# 1. 필요모듈
##############################################################################
import matplotlib.pyplot as plt
import pandas as pd


##############################################################################
# 2. 환경설정
##############################################################################
STEP_1_2 = "output/step_1_2.xlsx"
STEP_1_3 = "output/{}"
ROWS = 30


##############################################################################
# 3. 기본함수
##############################################################################
def parse_xlsx(sheet_name) -> pd.DataFrame:
    df_raw = pd.read_excel(STEP_1_2, sheet_name=sheet_name)
    df_raw.set_index("TIME", inplace=True)
    return df_raw


def plot_fill_between(df, output):
    ser_value = df["DATA_VALUE"]
    is_rise = ser_value.iloc[0] < ser_value.iloc[-1]

    # https://xkcd.com/color/rgb/
    color = "xkcd:bright red" if is_rise else "xkcd:bright blue"

    fig, ax = plt.subplots(figsize=(9, 3), layout="constrained")
    ylim_min, ylim_max = ser_value.min() * 0.95, ser_value.max() * 1.05
    ax.set_ylim(ylim_min, ylim_max)
    ax.plot(ser_value, linewidth=5, color=color)
    ax.fill_between(
        x=ser_value.index,
        y1=ser_value,
        y2=ylim_min if is_rise else ylim_max,
        color=color,
        alpha=0.1,
    )
    ax.margins(0)
    ax.set_axis_off()
    fig.savefig(STEP_1_3.format(f"grah_{output}.png"))


##############################################################################
# 4. 메인함수
##############################################################################
def main():
    with pd.ExcelFile(STEP_1_2) as xlsx:
        df_base_mo = xlsx.parse("base_mo")
        plot_fill_between(df_base_mo, "base_mo")

        df_tb = xlsx.parse("tb")
        plot_fill_between(df_tb, "tb")

        df_cb = xlsx.parse("cb")
        plot_fill_between(df_cb, "cb")

        df_kospi = xlsx.parse("kospi")
        plot_fill_between(df_kospi, "kospi")

        df_ex = xlsx.parse("ex")
        plot_fill_between(df_ex, "ex")


##############################################################################
# 5. 실행
##############################################################################
if __name__ == "__main__":
    main()
