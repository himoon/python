from enum import Enum
from pprint import pprint

import geopandas as gpd
import pandas as pd
import requests


class SERVICE(str, Enum):
    WFS = "WFS"
    WMS = "WMS"


class REQUEST(str, Enum):
    CAPABILITIES = "GetCapabilities"
    FEATURE = "GetFeature"
    MAP = "GetMap"


API_KEY = "5180848F-6F1E-3CDF-BA39-0464077ED534"

params = dict(
    key=f"{API_KEY}",
    request=f"{REQUEST.FEATURE}",  # 요청 서비스 오퍼레이션 : GetFeature, GetCapabilities
    typename=f"lt_c_adsido_info,lt_c_adsigg_info",  # 하나 또는 쉼표(,)로 분리된 지도레이어 목록, 최대 4개 : 레이어 목록 참고
    service=f"{SERVICE.WFS}",  # 요청 서비스명 : WFS(기본값)
    version=f"1.1.0",  # 요청 서비스 버전 : 1.1.0(기본값)
    # bbox=f"13987670,3912271,14359383,4642932",
    # propertyname=f"mnum,sido_cd,sigungu_cd,dyear,dnum,ucode,bon_bun,bu_bun,uname,sido_name,sigg_name,ag_geom",
    # maxfeatures="40",
    # srsname="EPSG:900913",
    output="application/json",
    # exceptions="text/xml",
)


# url = f"https://api.vworld.kr/req/wfs?SERVICE=WFS&REQUEST=GetFeature&TYPENAME=lt_c_uq111&BBOX=13987670,3912271,14359383,4642932&PROPERTYNAME=mnum,sido_cd,sigungu_cd,dyear,dnum,ucode,bon_bun,bu_bun,uname,sido_name,sigg_name,ag_geom&VERSION=1.1.0&MAXFEATURES=40&SRSNAME=EPSG:900913&OUTPUT=application/json&EXCEPTIONS=text/xml&KEY={API_KEY}"
url = f"https://api.vworld.kr/req/wfs"
resp = requests.get(url, params=params)
resp
gdf_raw = gpd.read_file(resp.text)
gdf_raw
gdf_raw.plot()
