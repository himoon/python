#######################################
# 1. 필요모듈
#######################################
import geopandas as gpd

import step_0
import step_2_1

#######################################
# 2. 환경설정
#######################################
STEP_2_2 = step_0.OUTPUT_DIR / "step_2_2.png"


#######################################
# 3. 기본함수
#######################################
pass


#######################################
# 4. 메인함수
#######################################
def main():
    gdf_raw: gpd.GeoDataFrame = gpd.read_file(step_2_1.STEP_2_1)
    ax = gdf_raw.plot()
    ax.set_axis_off()
    fig = ax.get_figure()
    fig.savefig(STEP_2_2)


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
