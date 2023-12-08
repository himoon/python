#######################################
# 1. 필요모듈
#######################################
from pathlib import Path

import geopandas as gpd
import matplotlib.font_manager as fm
import pandas as pd
from matplotlib import rc

import step_0
import step_1_3
import step_2_1

#######################################
# 2. 환경설정
#######################################
STEP_2_2 = step_0.OUTPUT_DIR / "step_2_2.geojson"


#######################################
# 3. 기본함수
#######################################
def set_font():
    FONT_PATH = Path(__file__).parent.parent / "font/Pretendard-Bold.ttf"
    font_name = fm.FontProperties(fname=FONT_PATH).get_name()
    rc("font", family=font_name)


#######################################
# 4. 메인함수
#######################################
def main():
    set_font()

    gdf_raw: gpd.GeoDataFrame = gpd.read_file(step_1_3.STEP_1_3)
    gdf_raw = gdf_raw.astype({"x": "float", "y": "float"})
    gdf_filtered = gdf_raw.set_crs("EPSG:5174", allow_override=True).filter(["adm_nm", "x", "y", "geometry"])

    df_price = pd.read_excel(step_2_1.STEP_2_1, sheet_name="result")
    df_price["시군구"] = df_price["지역명"].str.rsplit(n=1, expand=True).iloc[:, -1]
    df_price.columns = ["adm_nm", "adm_cd", "avg_price", "sgg_nm"]

    gdf_merged: gpd.GeoDataFrame = pd.merge(gdf_filtered, df_price, on="adm_nm", how="inner")
    gdf_merged = gdf_merged.filter(["adm_nm", "adm_cd", "sgg_nm", "avg_price", "x", "y", "geometry"])

    ax = gdf_merged.plot(column="avg_price", legend=True, cmap="OrRd", figsize=(9, 6))
    # gdf_merged.apply(lambda x: ax.annotate(text=x["시군구"], xy=x.geometry.representative_point().coords[0], ha="center"), axis=1)
    gdf_merged.apply(lambda x: ax.annotate(text=x["sgg_nm"], xy=(x["x"], x["y"]), ha="center"), axis=1)
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
