#######################################
# 1. 필요모듈
#######################################
import json

import geopandas as gpd
import pandas as pd

import step_0
import step_1_2
import step_1_3
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
    gdf_raw: gpd.GeoDataFrame = gpd.read_file(step_1_3.STEP_1_3)
    gdf_fixed = gdf_raw.set_crs("EPSG:5174", allow_override=True)
    gdf_fixed.plot()

    df_value = pd.read_excel(step_2_1.STEP_2_1, sheet_name="result")

    gdf_merged = pd.merge(gdf_fixed, df_value, left_on="adm_nm", right_on="지역명", how="inner")
    ax = gdf_merged.plot(column="면적당금액", legend=True, cmap="OrRd", figsize=(9, 6))
    gdf_merged.plot(ax=ax, color="none", edgecolor="black", lw=1)
    ax.set_axis_off()


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
