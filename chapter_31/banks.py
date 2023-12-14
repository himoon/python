from __future__ import annotations

import logging
import pathlib
import re
import time
from pprint import pprint

import pandas as pd
import requests
from datakart import Jusogokr, Kakao, Naver
from tqdm import tqdm

logger = logging.getLogger(__name__)


class Sgis:
    """통계지리정보서비스 SGIS"""

    def __init__(
        self,
        api_key: str,
        api_sec: str,
    ) -> None:
        self.api_key: str = api_key
        self.api_sec: str = api_sec

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
        # https://sgis.kostat.go.kr/developer/html/newOpenApi/api/dataApi/basics.html#auth
        url = "https://sgisapi.kostat.go.kr/OpenAPI3/auth/authentication.json"
        params = dict(consumer_key=self.api_key, consumer_secret=self.api_sec)
        resp = requests.get(url, params=params)
        parsed = resp.json()
        self.raise_for_err_cd(parsed)

        result = parsed.get("result", {})
        self._timeout = result.get("accessTimeout", 0)
        self._token = result.get("accessToken", "")
        return result

    def geocode(
        self,
        address: str,
        page: int = 0,
        limit: int = 5,
    ) -> dict:
        # https://sgis.kostat.go.kr/developer/html/newOpenApi/api/dataApi/addressBoundary.html#geocode
        url = "https://sgisapi.kostat.go.kr/OpenAPI3/addr/geocodewgs84.json"
        params = dict(
            accessToken=self.access_token,
            address=f"{address}",
            pagenum=f"{page}",
            resultcount=f"{limit}",
        )
        resp = requests.get(url, params=params)
        parsed = resp.json()
        self.raise_for_err_cd(parsed)

        result = parsed.get("result", {})
        total = result.get("totalcount")

        return parsed


WORK_DIR = pathlib.Path(__file__).parent
INPUT = WORK_DIR / "banks.xlsx"
OUTPUT = WORK_DIR / "banks_output.xlsx"

NAVER_KEY = "4LmEBVOylhQ9Da_Rhryr"
NAVER_SEC = "WwF0cMKQKS"
JUSO_KEY = "devU01TX0FVVEgyMDIzMTIxNDAwMzkyNjExNDM1NDg="
KAKAO_KEY = "2f15ef773b35f21f74877b7ed5122a76"

df_raw = pd.read_excel(INPUT, sheet_name="반기보('23.6월말)", skiprows=3, header=None)
df_raw.head(5)

df_header = df_raw.iloc[0:2].ffill(axis="rows").ffill(axis="columns")
ser_header = df_header.apply(lambda x: ".".join(x) if len(x.unique()) > 1 else x[0], axis="rows")
ser_header

df_reset = df_raw.iloc[2:].reset_index(drop=True)
# df_sliced.columns = ser_header
df_reset.columns = ["은행명", "점포명", "점포구분", "시도", "시군구", "읍면동", "도로명", "전화번호"]
df_reset.fillna("", inplace=True)
df_reset.head()

df_queried = df_reset.query("점포구분=='지점' and 은행명=='산업은행'").sort_values(["은행명", "점포명"]).reset_index(drop=True)
df_filtered = df_queried.filter(["은행명", "점포명", "점포구분", "시도", "시군구", "도로명"])
df_filtered.head()

df_validated = df_filtered.copy()
df_validated = df_validated.fillna("").applymap(lambda x: str(x).strip())
df_validated["도로명"] = df_validated["도로명"].replace(r"\(.+\)", "", regex=True)
# df_validated.apply(lambda x: print(x.unique()), axis=0)
df_validated.to_excel(OUTPUT)

df_validated["은행명"].sort_values()
df_validated["점포명"].sort_values()
df_validated["점포구분"].sort_values()
df_validated["시도"].sort_values()
df_validated["시군구"].sort_values()
df_validated["도로명"].sort_values()

juso = Jusogokr(JUSO_KEY)
naver = Naver(NAVER_KEY, NAVER_SEC)
kakao = Kakao(KAKAO_KEY)


for idx, ser in tqdm(df_validated.iterrows(), total=df_validated.shape[0]):
    # ser = df_validated.loc[884]
    addr = f'{ser["시도"]} {ser["시군구"]} {ser["도로명"]}'
    if not addr.strip():
        df_validated.loc[idx, "siNm"] = ""
        df_validated.loc[idx, "sggNm"] = ""
        df_validated.loc[idx, "roadNm"] = ""
        continue

    rows = juso.addr(addr)
    if not rows:
        logger.error(f"{addr} not found, try kakao")
        br_name = f'{ser["은행명"]} {ser["점포명"]} {ser["점포구분"]}'
        kakao_resp = kakao.local_keyword(br_name)
        if kakao_resp:
            kakao_row = kakao_resp[0]
            addr = kakao_row["road_address_name"]
            rows = juso.addr(addr)

    if not rows:
        logger.error(f"{addr} not found, try naver")
        naver_resp = naver.local(br_name)
        if naver_resp:
            naver_row = naver_resp[0]
            addr = naver_row["roadAddress"]
            rows = juso.addr(addr)

    if not rows:
        logger.error(f"{addr} not found")
        df_validated.loc[idx, "siNm"] = ""
        df_validated.loc[idx, "sggNm"] = ""
        df_validated.loc[idx, "roadNm"] = ""
        continue

    row = rows[0]
    df_validated.loc[idx, "siNm"] = row.get("siNm", "")
    df_validated.loc[idx, "sggNm"] = row.get("sggNm", "")

    road_nm = row.get("rn", "")
    buld_main = row.get("buldMnnm", "")
    buld_sub = row.get("buldSlno", "")
    buld_nm = buld_main if buld_sub == "0" else f"{buld_main}-{buld_sub}"
    df_validated.loc[idx, "roadNm"] = f"{road_nm} {buld_nm}"


same_sido = df_validated["시도"] == df_validated["siNm"]
same_sgg = df_validated["시군구"] == df_validated["sggNm"]
same_roadnm = df_validated["도로명"] == df_validated["roadNm"]
same_addr = same_sido & same_sgg & same_roadnm

df_validated["original"] = False
df_validated.loc[same_addr, "original"] = True

df_validated.to_excel(OUTPUT, index=False)

# "서울특별시 강남구 언주로 706 우정빌딩 not found", 1695
