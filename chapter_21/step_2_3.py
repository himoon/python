#######################################
# 1. 필요모듈
#######################################
import geopandas as gpd
import pandas as pd

import step_0
import step_1_3
import step_2_1

#######################################
# 2. 환경설정
STEP_2_3 = step_0.OUTPUT_DIR / "step_2_3.geojson"
#######################################


#######################################
# 3. 기본함수
#######################################
pass


#######################################
# 4. 메인함수
#######################################
def main():
    gdf_raw: gpd.GeoDataFrame = gpd.read_file(step_2_1.STEP_2_1)
    print(gdf_raw.head(2))

    df_price = pd.read_excel(step_1_3.STEP_1_3, sheet_name="result")
    df_price.columns = ["adm_nm", "avg_price"]
    print(df_price.head(2))

    gdf_merged: gpd.GeoDataFrame = pd.merge(gdf_raw, df_price, on="adm_nm", how="inner")
    gdf_merged = gdf_merged.filter(["adm_nm", "avg_price", "geometry"])
    print(gdf_merged.head(2))

    with open(STEP_2_3, "w") as fp:
        fp.write(gdf_merged.to_json(drop_id=True))


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
