from __future__ import annotations

import logging

import geopandas as gpd
import pydeck as pdk
import streamlit as st
from datakart import Sgis

import step_0

logger = logging.getLogger(__name__)


def query_sgis() -> gpd.GeoDataFrame:
    sgis = Sgis(step_0.SGIS_API_KEY, step_0.SGIS_API_SEC)
    features = sgis.hadm_area()
    gdf_raw = gpd.GeoDataFrame.from_features(features, crs="EPSG:5179")
    return gdf_raw.to_crs("EPSG:4326").filter(["adm_cd", "adm_nm", "geometry"])


def main():
    gdf_raw = query_sgis()
    gdf_raw.head()

    center = gdf_raw.geometry.unary_union.centroid
    deck = pdk.Deck(
        # map_style=None,
        # map_provider=None,
        initial_view_state=pdk.ViewState(
            longitude=center.x,
            latitude=center.y,
            zoom=5.5,
            bearing=0,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "GeoJsonLayer",  # https://deck.gl/docs/api-reference/layers/geojson-layer
                gdf_raw,
                opacity=1,  # Default: 1, The opacity of the layer.
                ###################
                # Interaction Properties
                ###################
                pickable=True,  # Default: false, Whether the layer responds to mouse pointer picking events.
                auto_highlight=True,  # Default: false, When true, current object pointed by mouse pointer (when hovered over) is highlighted with highlightColor. Requires pickable to be true.
                ###################
                # Fill Options
                ###################
                filled=True,  # Default: true, Whether to draw filled polygons (solid fill) and points (circles). Note that for each polygon, only the area between the outer polygon and any holes will be filled. This prop is effective only when the polygon is NOT extruded.
                # get_fill_color=[0, 0, 255],  # Default: [0, 0, 0, 255]
                ###################
                # Stroke Options
                ###################
                stroked=True,  # default : True, Whether to draw an outline around polygons and points (circles). Note that for complex polygons, both the outer polygon as well the outlines of any holes will be drawn.
                get_line_color=[
                    255,
                    255,
                    255,
                ],  # Default: [0, 0, 0, 255], The rgba color of a line is in the format of [r, g, b, [a]]. Each channel is a number between 0-255 and a is 255 if not supplied.
                get_line_width=1,  # Default: 1, The width of a line, in units specified by lineWidthUnits (default meters).
                line_width_units=pdk.types.String("pixels"),
                ###################
                # 3D Options
                ###################
                # extruded=False,  # Default: false, Extrude Polygon and MultiPolygon features along the z-axis if set to true. The height of the drawn features is obtained using the getElevation accessor.
                # wireframe=False,  # Default: false, Whether to generate a line wireframe of the hexagon. The outline will have "horizontal" lines closing the top and bottom polygons and a vertical line (a "strut") for each vertex on the polygon.
                # get_elevation="avg_price",  # Default: 1000, The elevation of a polygon feature (when extruded is true).
            )
        ],
    )
    # deck.to_html(open_browser=True, css_background_color="#000")
    st.pydeck_chart(deck)


if __name__ == "__main__":
    step_0.init_output_folder()
    logging.basicConfig(level=logging.INFO, filename=step_0.OUTPUT_DIR / "err.log")
    main()
