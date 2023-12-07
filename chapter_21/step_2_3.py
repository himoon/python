#######################################
# 1. 필요모듈
#######################################
from pathlib import Path

import geopandas as gpd
import matplotlib.font_manager as fm
import pandas as pd
import pydeck as pdk
from matplotlib import rc

import step_0
import step_1_3
import step_2_1
import step_2_2

#######################################
# 2. 환경설정
#######################################
STEP_2_3 = step_0.OUTPUT_DIR / "step_2_3.html"


#######################################
# 3. 기본함수
#######################################
pass


#######################################
# 4. 메인함수
#######################################
def main():
    df_json = pd.read_json(step_1_3.STEP_1_3)

    gdf_raw: gpd.GeoDataFrame = gpd.read_file(step_1_3.STEP_1_3)
    gdf_raw = gdf_raw.astype({"x": "float", "y": "float"})
    gdf_fixed = gdf_raw.set_crs("EPSG:5174", allow_override=True)
    gdf_fixed
    gdf_fixed.geometry.get_coordinates()

    df = pd.DataFrame()
    df["coordinates"] = df_json["features"].apply(lambda row: row["geometry"]["coordinates"])

    view_state = pdk.ViewState(
        latitude=37.55,
        longitude=127,
        zoom=11,
        maxZoom=16,
        pitch=45,
        bearing=0,
    )

    polygon_layer = pdk.Layer(
        "PolygonLayer",
        df,
        id="geojson",
        opacity=0.8,
        stroked=False,
        get_polygon="coordinates",
        filled=True,
        extruded=True,
        wireframe=True,
        get_elevation="elevation",
        get_fill_color="[255, 255, 30]",
        get_line_color=[255, 255, 255],
        auto_highlight=True,
        pickable=True,
    )

    r = pdk.Deck(
        layers=[polygon_layer],
        initial_view_state=view_state,
        map_style=pdk.map_styles.LIGHT,
    )
    r.to_html()


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
