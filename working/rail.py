from __future__ import annotations

from enum import Enum

import geopandas as gpd
from pyproj import Transformer

SHP = "./N3L_A0171119/N3L_A0171119.shp"


class DIVI(str, Enum):
    """구분 : 철도중심선의 구분을 나타내는 코드 (철도의 구분코드와 동일)"""

    RRD000 = "미분류"
    RRD001 = "고속철도"
    RRD002 = "보통철도"
    RRD003 = "특수철도"
    RRD004 = "지하철(지상)"
    RRD005 = "삭도(케이블카)"
    RRD006 = "모노레일"
    RRD999 = "기타"


class STRU(str, Enum):
    """구조 : 철도중심선의 구조를 나타내는 코드"""

    RRS000 = "미분류"
    RRS001 = "단선"
    RRS002 = "복선"
    RRS003 = "복복선"
    RRS004 = "3복선"
    RRS999 = "기타"


class MNGT(str, Enum):
    """관리기관 : 철도의 관리기관을 나타내는 코드 (철도의 관리기관코드와 동일)"""

    RRM000 = "미분류"
    RRM001 = "국가"
    RRM002 = "지자체"
    RRM003 = "공공기관"
    RRM004 = "개인"
    RRM999 = "기타"


class REST(str, Enum):
    """기타"""


class SCLS(str, Enum):
    """통합코드 : 철도중심선의 통합 표준코드
    - 1/1,000          A0171119 철도중심선
    - 1/5,000 1/25,000 A0171119 철도중심선
    """


class FMTA(str, Enum):
    """제작정보 :
    - 기본도 제작정보를 참조하는 일련번호 (SL_PRODUCT_INFO),
    - 각각의 정기/수시 갱신 영역에 포함되는 지형지물 객체에 일련번호 부여
    """


# 브이월드 -> 공간정보 다운로드 -> 오픈마켓 -> 철도중심선
df_raw: gpd.GeoDataFrame = gpd.read_file(SHP)
df_raw.plot()
df_raw.NAME.unique()
df_raw.set_geometry("geometry", crs="epsg:5174", inplace=True)
df_raw.set_geometry("geometry", crs="epsg:5171", inplace=True)
df_raw.plot()
df_raw.crs
df_raw[df_raw.NAME == "지하철9호선"].plot()

df_raw.head()
df_raw.describe()

df_line9: gpd.GeoDataFrame = df_raw[df_raw.NAME == "지하철9호선"]
df_line9.crs
df_line9.plot()

df_line9_2 = df_line9.set_crs(epsg=5181, allow_override=True)
df_line9_2.crs
