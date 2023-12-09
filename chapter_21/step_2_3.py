#######################################
# 1. 필요모듈
#######################################
import geopandas as gpd
import mapclassify as mc
import matplotlib as mpl
import pydeck as pdk
import streamlit as st

import step_0
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
    st.markdown("# 서울지역 단위면적당 아파트 매매 가격")

    gdf_raw = gpd.read_file(step_2_2.STEP_2_2)

    k = 10
    c10 = mc.MaximumBreaks(gdf_raw["avg_price"], k=k)
    gdf_raw["mc"] = c10.yb
    # gdf_raw.assign(cl=c10.yb).plot(column="cl", categorical=True, k=10, cmap="OrRd", linewidth=0.1, edgecolor="white", legend=True)

    cmap = mpl.colormaps["OrRd"]
    norm = mpl.colors.Normalize(vmin=c10.yb.min(), vmax=c10.yb.max())
    smap = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
    rgba = smap.to_rgba(gdf_raw["mc"], bytes=True).astype(int)
    gdf_raw["color"] = rgba.tolist()

    center = gdf_raw.geometry.unary_union.centroid
    view_state = pdk.ViewState(longitude=center.x, latitude=center.y, zoom=9.5, bearing=0, pitch=30)

    geojson_layer = pdk.Layer(
        "GeoJsonLayer",
        gdf_raw,
        opacity=0.8,
        stroked=False,
        filled=True,
        wireframe=False,
        extruded=True,
        get_elevation="avg_price",
        get_fill_color="color",
        get_line_color=[255, 255, 255],
        get_line_width=100,
        pickable=True,
        auto_highlight=True,
    )

    deck = pdk.Deck(
        layers=[geojson_layer],
        initial_view_state=view_state,
        map_style="road",
        tooltip={"text": "{adm_nm}", "style": {"color": "white"}},
    )
    st.pydeck_chart(deck)


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
