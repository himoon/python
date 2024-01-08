from __future__ import annotations

import json
import logging
import pathlib
from concurrent.futures import ThreadPoolExecutor, as_completed

import geopandas as gpd
import mapclassify as mc
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import streamlit as st
from datakart import Jusogokr, Kakao, Naver, Sgis
from tqdm import tqdm

import step_0
import step_1
import step_2

logger = logging.getLogger(__name__)


def query_sgis() -> gpd.GeoDataFrame:
    sgis = Sgis(step_0.SGIS_API_KEY, step_0.SGIS_API_SEC)
    features = sgis.hadm_area()
    gdf_raw = gpd.GeoDataFrame.from_features(features, crs="EPSG:5179")
    return gdf_raw.to_crs("EPSG:4326").filter(["adm_cd", "adm_nm", "geometry"])


def get_br_list():
    df_raw = pd.read_excel(step_2.STEP_2)
    df_raw.head()
    return df_raw.filter(["br_name", "x", "y"])


def get_img_uri():
    import base64

    fullpath = step_0.WORK_DIR / "img_symbol_chbi.png"
    with open(step_0.WORK_DIR / fullpath, "rb") as fp:
        res = base64.b64encode(fp.read()).decode("utf-8")
        ext = fullpath.suffix
        uri = f"data:image/{ext[1:]};base64,{res}"
    return uri


def main():
    gdf_raw = query_sgis()
    gdf_raw.head()

    df_br_list = get_br_list()
    df_br_list.head()

    ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/c/c4/Projet_bi%C3%A8re_logo_v2.png"
    ICON_URL = "https://www.kdb.co.kr/wcmscontents/hmp/ch/bi/bi/rc/img_symbol_chbi.png"
    icon_data = {
        # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
        # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
        "url": ICON_URL,
        "width": 262,
        "height": 232,
    }

    center = gdf_raw.geometry.unary_union.centroid
    view_state = pdk.ViewState(longitude=center.x, latitude=center.y, zoom=5.5, bearing=0, pitch=30)

    icon_data = {
        # "url": "https://cdn-icons-png.flaticon.com/512/3917/3917527.png?ga=GA1.1.1040331474.1703310165&",
        # "url": "https://img.icons8.com/plasticine/100/000000/marker.png",
        # "url": (step_0.WORK_DIR / "img_symbol_chbi.png").as_posix(),
        # "url": "https://www.kdb.co.kr/wcmscontents/hmp/ch/bi/bi/rc/img_symbol_chbi.png",
        "url": get_img_uri(),
        "width": 128,
        "height": 128,
    }

    df_br_list["icon_data"] = None
    for i in df_br_list.index:
        df_br_list["icon_data"][i] = icon_data
    df_br_list.head()

    icon_layer = pdk.Layer(
        type="IconLayer",
        data=df_br_list,
        get_icon="icon_data",
        get_size=4,
        size_scale=15,
        get_position=["x", "y"],
        pickable=True,
    )
    deck = pdk.Deck(
        # layers=[column_layer, geojson_layer],
        layers=[icon_layer],
        initial_view_state=view_state,
        map_style="road",
    )
    deck.to_html()

    # column_layer = pdk.Layer(
    #     "ColumnLayer",
    #     data=df_br_list,
    #     get_position=["x", "y"],
    #     get_elevation="1000",
    #     elevation_scale=100,
    #     radius=1000,
    #     get_fill_color=[0, 255, 255],
    #     pickable=True,
    #     auto_highlight=True,
    # )
    # geojson_layer = pdk.Layer(
    #     "GeoJsonLayer",
    #     gdf_raw,
    #     opacity=0.8,
    #     stroked=False,
    #     filled=True,
    #     wireframe=False,
    #     # extruded=True,
    #     # get_elevation="avg_price",
    #     get_fill_color=[0, 0, 255, 100],
    #     get_line_color=[255, 255, 255],
    #     get_line_width=100,
    #     pickable=True,
    #     # auto_highlight=True,
    # )


if __name__ == "__main__":
    step_0.init_output_folder()
    logging.basicConfig(level=logging.INFO, filename=step_0.OUTPUT_DIR / "err.log")
    main()
