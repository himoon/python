#######################################
# 1. 필요모듈
#######################################
import geopandas as gpd

import step_0
import step_2_3

#######################################
# 2. 환경설정
STEP_2_4 = step_0.OUTPUT_DIR / "step_2_4_{}.png"
#######################################


#######################################
# 3. 기본함수
#######################################
pass


#######################################
# 4. 메인함수
#######################################
def main():
    gdf_raw: gpd.GeoDataFrame = gpd.read_file(step_2_3.STEP_2_3)
    ax = gdf_raw.plot(column="avg_price", cmap="OrRd", edgecolor="k", legend=True)
    ax.set_axis_off()
    ax.get_figure().savefig(STEP_2_4.as_posix().format(1))

    ax = gdf_raw.plot(column="avg_price", cmap="OrRd", edgecolor="k", legend=True, scheme="quantiles", k=5)
    ax.set_axis_off()
    ax.get_figure().savefig(STEP_2_4.as_posix().format(2))

    ax = gdf_raw.plot(column="avg_price", cmap="OrRd", edgecolor="k", legend=True, scheme="quantiles", k=10)
    ax.set_axis_off()
    ax.get_figure().savefig(STEP_2_4.as_posix().format(3))


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
