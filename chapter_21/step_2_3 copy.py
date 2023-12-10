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
    df_price = pd.read_excel(step_1_3.STEP_1_3, sheet_name="result")
    df_price.columns = ["adm_nm", "avg_price"]

    gdf_raw: gpd.GeoDataFrame = gpd.read_file(step_2_1.STEP_2_1)

    gdf_merged: gpd.GeoDataFrame = pd.merge(gdf_raw, df_price, on="adm_nm", how="inner")
    gdf_merged = gdf_merged.filter(["adm_nm", "avg_price", "geometry"])

    ax = gdf_merged.plot(column="avg_price", legend=True, cmap="OrRd", figsize=(9, 6))
    gdf_merged.apply(lambda x: ax.annotate(text=x["sgg_nm"], xy=(x["x"], x["y"]), ha="center"), axis=1)
    # gdf_merged.apply(lambda x: ax.annotate(text=x["시군구"], xy=x.geometry.representative_point().coords[0], ha="center"), axis=1)
    # gdf_merged.apply(lambda x: ax.annotate(text=x["시군구"], xy=x.geometry.centroid.coords[0], ha="center"), axis=1)
    gdf_merged.plot(ax=ax, color="none", edgecolor="black", linewidth=1)
    ax.set_axis_off()
    # https://shotlefttodatascience.com/2018/05/16/adding-labels-to-districts-in-geopandas/

    with open(STEP_2_2, "w") as fp:
        fp.write(gdf_merged.to_json(drop_id=True))


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
