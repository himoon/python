from __future__ import annotations

import logging
import os
import time
from enum import Enum

import geodatasets
import geopandas as gpd

# 필요한 패키지와 라이브러리를 가져옴
import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from matplotlib import font_manager, rc
from pyproj import Transformer
from working.enums import Boundary

# data = np.random.randint(-100, 100, 50).cumsum()

# plt.plot(range(50), data, "r")
# mpl.rcParams["axes.unicode_minus"] = False
# plt.title("시간별 가격 추이")
# plt.ylabel("주식 가격")
# plt.xlabel("시간(분)")

# print("버전: ", mpl.__version__)
# print("설치 위치: ", mpl.__file__)
# print("설정 위치: ", mpl.get_configdir())
# print("캐시 위치: ", mpl.get_cachedir())

# print("설정파일 위치: ", mpl.matplotlib_fname())

# font_list = fm.findSystemFonts(fontpaths=None, fontext="ttf")
# font_list

# # ttf 폰트 전체갯수
# print(len(font_list))


path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
fontprop = fm.FontProperties(fname=path, size=18)
# plt.ylabel("세로축", fontproperties=fontprop)
# plt.title("가로축", fontproperties=fontprop)
# plt.show()


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


# 법정동코드
# 행정표준코드관리시스템
# https://www.code.go.kr/stdcode/regCodeL.do


# pd.read_csv("법정동코드 전체자료.txt", encoding="cp949", delimiter="\t")


# 지도 경계
# http://www.gisdeveloper.co.kr/?p=2332#comment-40449

logger = logging.getLogger(__name__)


API_URL = "https://sgisapi.kostat.go.kr/OpenAPI3"


class Sgis:
    """통계지리정보서비스 SGIS"""

    def __init__(
        self,
        api_key: str = "c45c510fe7854d5aae90",
        api_sercret: str = "fde5af5e4362466b91fe",
        api_url: str = "https://sgisapi.kostat.go.kr/OpenAPI3",
    ) -> None:
        self.api_key: str = api_key
        self.api_sercret: str = api_sercret
        self.api_url: str = api_url

    @property
    def access_token(self) -> str:
        if not hasattr(self, "_token") or int(self._timeout) / 1000 - 10 < time.time():
            self.auth()
        return self._token

    @staticmethod
    def raise_for_err_cd(parsed: dict) -> None:
        err_cd = parsed.get("errCd", 0)
        if err_cd:
            raise ValueError(f"[{err_cd}] {parsed.get('errMsg', 0)}")

    def auth(self) -> dict:
        params = f"consumer_key={self.api_key}&consumer_secret={self.api_sercret}"
        resp = requests.get(f"{self.api_url}/auth/authentication.json?{params}")
        parsed = resp.json()
        self.raise_for_err_cd(parsed)

        result = parsed.get("result", {})
        self._timeout = result.get("accessTimeout", 0)
        self._token = result.get("accessToken", "")
        return result

    # https://sgis.kostat.go.kr/developer/html/newOpenApi/api/dataApi/addressBoundary.html#hadmarea
    # UTM-K (EPSG 5179)
    def hadm_area(self, year: str = "2023", adm_cd: str = None, low_search: str = "0") -> dict:
        params = dict(accessToken=self.access_token, year=year, adm_cd=adm_cd, low_search=low_search)
        resp = requests.get(f"{API_URL}{Boundary.HADM_AREA}", params=params)
        parsed = resp.json()
        self.raise_for_err_cd(parsed)
        return parsed

    def addr_stage(self, cd: str = None, pg_yn: str = "0") -> list:
        # https://sgis.kostat.go.kr/developer/html/newOpenApi/api/dataApi/addressBoundary.html#stage
        # https://sgisapi.kostat.go.kr/OpenAPI3/addr/stage.json
        params = dict(accessToken=self.access_token, cd=cd, pg_yn=pg_yn)
        resp = requests.get(f"https://sgisapi.kostat.go.kr/OpenAPI3/addr/stage.json", params=params)
        parsed = resp.json()
        self.raise_for_err_cd(parsed)
        return parsed.get("result", [])

    @classmethod
    def _test():
        self = Sgis()
        raw_1 = self.hadm_area("2023", low_search="0")
        df_raw_1 = gpd.GeoDataFrame.from_features(raw_1)
        df_raw_1.plot()

        self = Sgis()
        raw_2 = self.hadm_area("2023", adm_cd="11", low_search="1")
        df_raw_2 = gpd.GeoDataFrame.from_features(raw_2)
        axws = df_raw_2.plot()
        axws.set_axis_off()

        df_seoul = df_raw_1[df_raw_1["adm_cd"] == "11"]
        df_seoul.plot()

        df_seoul = df_seoul.set_crs(epsg=5171, allow_override=True)
        df_seoul.filter(["geometry"])
        df_seoul.crs

        ######################################################################
        ######################################################################
        df_raw: gpd.GeoDataFrame = gpd.read_file(SHP)
        df_raw.geometry
        df_raw.crs
        df_raw.plot()

        grouped = df_raw.groupby("NAME")
        for name, df_name in grouped:
            ax = df_name.plot()
            ax.set_title(name, fontproperties=fontprop)

        df_raw_1 = df_raw.to_crs("epsg:5181")
        df_line9 = df_raw_1[df_raw_1.NAME == "지하철9호선"]
        df_line9.plot()

        df_raw_2 = df_raw.to_crs("epsg:2097")
        df_raw_2.crs
        df_line9 = df_raw_2[df_raw_2.NAME == "지하철9호선"]
        df_line9.plot()

        df_raw_3 = df_raw.to_crs("epsg:2097")
        df_raw_3.crs
        df_line9 = df_raw_3.loc[df_raw_3.NAME.str.contains("지하철")]
        df_line9.plot()

        df_raw.plot()
        df_raw.NAME.unique()
        df_raw.set_geometry("geometry", crs="epsg:5174", inplace=True)
        df_raw.set_geometry("geometry", crs="epsg:5171", inplace=True)
        df_raw.plot()
        df_raw.crs
        df_line9 = df_raw[df_raw.NAME == "지하철9호선"]
        df_line9.filter(["geometry"])
        df_line9.crs

        pd.concat([df_seoul.filter(["geometry"]), df_line9.filter(["geometry"])])

        ######################################################################
        ######################################################################
        usa = gpd.read_file(geodatasets.get_path("geoda.natregimes"))

        usa.crs
        ax = usa.plot()
        ax.set_title("WGS84 (lat/lon)")
        usa.geometry[0]

        usa = usa.to_crs("ESRI:102003")
        ax = usa.plot()
        ax.set_title("NAD 1983 Albers contiguous USA")
        usa.geometry
