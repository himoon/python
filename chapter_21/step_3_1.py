from __future__ import annotations

import logging
import time
from pprint import pprint
from urllib.parse import urlencode

import requests

# 법정동코드
# 행정표준코드관리시스템
# https://www.code.go.kr/stdcode/regCodeL.do

# import pandas as pd

# pd.read_csv("법정동코드 전체자료.txt", encoding="cp949", delimiter="\t")


# 지도 경계
# http://www.gisdeveloper.co.kr/?p=2332#comment-40449

logger = logging.getLogger(__name__)


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
        return parsed

    def boundary(self, year: str = "2023", adm_cd: str = None, low_search: str = "0"):
        # https://sgisapi.kostat.go.kr/OpenAPI3/boundary/hadmarea.geojson
        year = "2023"
        adm_cd = None
        low_search = "1"
        params = dict(accessToken=self.access_token, year=year, adm_cd=adm_cd, low_search=low_search)
        resp = requests.get(f"https://sgisapi.kostat.go.kr/OpenAPI3/boundary/hadmarea.geojson", params=params)
        print(resp.text)

        parsed = resp.json()
        self.raise_for_err_cd(parsed)
        return parsed

    def addr_stage(self, cd: str = None, pg_yn: str = "1"):
        # https://sgis.kostat.go.kr/developer/html/newOpenApi/api/dataApi/addressBoundary.html#stage
        # https://sgisapi.kostat.go.kr/OpenAPI3/addr/stage.json
        cd = None
        pg_yn = "1"
        params = dict(accessToken=self.access_token, cd=cd, pg_yn=pg_yn)
        resp = requests.get(f"https://sgisapi.kostat.go.kr/OpenAPI3/addr/stage.json", params=params)
        print(resp.text)

        parsed = resp.json()
        self.raise_for_err_cd(parsed)
        return parsed

    @classmethod
    def _test():
        self = Sgis()
