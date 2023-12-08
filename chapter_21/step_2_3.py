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
    def multipolygon_to_coordinates(x):
        if hasattr(x, "geoms"):
            lon, lat = x.geoms[0].exterior.xy
            return [[x, y] for x, y in zip(lon, lat)]
        else:
            lon, lat = x.exterior.xy
            return [[x, y] for x, y in zip(lon, lat)]

    df_json = gpd.read_file(step_0.OUTPUT_DIR / "older_seoul.geojson")
    df_json = gpd.read_file(step_2_2.STEP_2_2)
    df_json["coordinates"] = df_json["geometry"].apply(multipolygon_to_coordinates)
    df_json.explore()
    # del df_json["geometry"]
    # df_json["정규화인구"] = df_json["인구"] / df_json["인구"].max()

    # Make layer
    layer = pdk.Layer(
        "PolygonLayer",  # 사용할 Layer 타입
        df_json,  # 시각화에 쓰일 데이터프레임
        get_polygon="coordinates",  # geometry 정보를 담고있는 컬럼 이름
        # get_fill_color="[0, 255*정규화인구, 0]",  # 각 데이터 별 rgb 또는 rgba 값 (0~255)
        get_fill_color="[0, 255, 0]",  # 각 데이터 별 rgb 또는 rgba 값 (0~255)
        pickable=True,  # 지도와 interactive 한 동작 on
        auto_highlight=True,  # 마우스 오버(hover) 시 박스 출력
    )

    # Set the viewport location
    center = [126.986, 37.565]
    view_state = pdk.ViewState(longitude=center[0], latitude=center[1], zoom=10)

    # Render
    r = pdk.Deck(layers=[layer], initial_view_state=view_state)
    r.to_html()

    layer = pdk.Layer(
        "PolygonLayer",  # 사용할 Layer 타입
        df_json,  # 시각화에 쓰일 데이터프레임
        get_polygon="coords",  # geometry 정보를 담고있는 컬럼 이름
        get_fill_color="[0, 255, 0]",  # 각 데이터 별 rgb 또는 rgba 값 (0~255)
        pickable=True,  # 지도와 interactive 한 동작 on
        auto_highlight=True,  # 마우스 오버(hover) 시 박스 출력
    )

    # Set the viewport location
    center = [126.986, 37.565]
    view_state = pdk.ViewState(longitude=center[0], latitude=center[1], zoom=10)

    # Render
    r = pdk.Deck(layers=[layer], initial_view_state=view_state)
    r.to_html()


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
