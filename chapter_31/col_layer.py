"""
ColumnLayer
===========

Real estate values for select properties in Taipei. Data is from 2012-2013.
The height of a column indicates increasing price per unit area, and the color indicates distance from a subway stop.

The real estate valuation data set from UC Irvine's Machine Learning repository, viewable here:

https://archive.ics.uci.edu/ml/datasets/Real+estate+valuation+data+set
"""

import pandas as pd
import pydeck as pdk

import step_2

df_raw = pd.read_excel(step_2.STEP_2)
df_raw = df_raw.filter(["br_name", "x", "y"])
df_raw.head()


DATA_URL = "https://raw.githubusercontent.com/ajduberstein/geo_datasets/master/housing.csv"
df = pd.read_csv(DATA_URL)
df.head()
view_state = pdk.ViewState(longitude=127, latitude=37, zoom=5.5, bearing=0, pitch=30)

view = pdk.data_utils.compute_view(df[["lng", "lat"]])
view.pitch = 75
view.bearing = 0

column_layer = pdk.Layer(
    "ColumnLayer",
    data=df_raw,
    # get_position=["lng", "lat"],
    get_position=["x", "y"],
    get_elevation="100",
    elevation_scale=100,
    radius=50,
    # get_fill_color=["mrt_distance * 10", "mrt_distance", "mrt_distance * 10", 140],
    get_fill_color=[0, 0, 255],
    pickable=True,
    auto_highlight=True,
)

tooltip = {
    "html": "<b>{mrt_distance}</b> meters away from an MRT station, costs <b>{price_per_unit_area}</b> NTD/sqm",
    "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
}

r = pdk.Deck(
    column_layer,
    initial_view_state=view,
    tooltip=tooltip,
    # map_provider="mapbox",
    # map_style=pdk.map_styles.SATELLITE,
)

r.to_html()
