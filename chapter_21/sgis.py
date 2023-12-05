from __future__ import annotations

import logging
import time
from enum import Enum

import requests

logger = logging.getLogger(__name__)


class Boundary(str, Enum):
    HADM_AREA = f"/boundary/hadmarea.geojson"
    STATS_AREA = f"/boundary/statsarea.geojson"
    USER_AREA = f"/boundary/userarea.geojson"

    def __str__(self) -> str:
        return self.value


class Sgis:
    """통계지리정보서비스 SGIS"""

    def __init__(
        self,
        api_key: str = "c45c510fe7854d5aae90",
        api_sec: str = "fde5af5e4362466b91fe",
        api_url: str = "https://sgisapi.kostat.go.kr/OpenAPI3",
    ) -> None:
        self.api_key: str = api_key
        self.api_sec: str = api_sec
        self.api_url: str = api_url

    @staticmethod
    def raise_for_err_cd(parsed: dict) -> None:
        err_cd = parsed.get("errCd", 0)
        if err_cd:
            raise ValueError(f"[{err_cd}] {parsed.get('errMsg', 0)}")

    @property
    def access_token(self) -> str:
        if not hasattr(self, "_token") or int(self._timeout) / 1000 - 10 < time.time():
            self.auth()
        return self._token

    def auth(self) -> dict:
        params = f"consumer_key={self.api_key}&consumer_secret={self.api_sec}"
        resp = requests.get(f"{self.api_url}/auth/authentication.json?{params}")
        parsed = resp.json()
        self.raise_for_err_cd(parsed)

        result = parsed.get("result", {})
        self._timeout = result.get("accessTimeout", 0)
        self._token = result.get("accessToken", "")
        return result

    def hadm_area(self, year: str = "2023", adm_cd: str = None, low_search: str = "0") -> dict:
        # https://sgis.kostat.go.kr/developer/html/newOpenApi/api/dataApi/address3.html#hadmarea
        # UTM-K (EPSG 5179)
        params = dict(accessToken=self.access_token, year=year, adm_cd=adm_cd, low_search=low_search)
        resp = requests.get(f"{self.api_url}{Boundary.HADM_AREA}", params=params)
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
