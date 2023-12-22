from __future__ import annotations

import logging
import pathlib
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
from datakart import Jusogokr, Kakao, Naver
from tqdm import tqdm

WORK_DIR = pathlib.Path(__file__).parent
OUTPUT_DIR = WORK_DIR / "output"
IN_EXCEL = WORK_DIR / "banks.xlsx"
STEP_1 = OUTPUT_DIR / "step_1.xlsx"

NAVER_KEY = "4LmEBVOylhQ9Da_Rhryr"
NAVER_SEC = "WwF0cMKQKS"
JUSO_KEY = "devU01TX0FVVEgyMDIzMTIxNDAwMzkyNjExNDM1NDg="
KAKAO_KEY = "2f15ef773b35f21f74877b7ed5122a76"

logger = logging.getLogger(__name__)


def init_output_folder():
    if not OUTPUT_DIR.is_dir():
        print(f"'{OUTPUT_DIR}' 폴더를 생성합니다.")
        OUTPUT_DIR.mkdir()


def load_excel() -> pd.DataFrame:
    df_raw = pd.read_excel(IN_EXCEL, sheet_name="반기보('23.6월말)", skiprows=3, header=None)
    df_body = df_raw.iloc[2:].reset_index(drop=True)
    df_body.columns = ["은행명", "점포명", "점포구분", "시도", "시군구", "읍면동", "도로명", "전화번호"]
    # df_header = df_raw.iloc[0:2].ffill(axis="rows").ffill(axis="columns")
    # ser_header = df_header.apply(lambda x: ".".join(x) if len(x.unique()) > 1 else x[0], axis="rows")
    # df_body.columns = ser_header
    return df_body.fillna("").map(lambda x: str(x).strip())


def query_kakao(keyword: str) -> str:
    resp = Kakao(KAKAO_KEY).local_keyword(keyword.strip())
    return resp[0].get("road_address_name", "") if resp else ""


def query_naver(keyword: str) -> str:
    resp = Naver(NAVER_KEY, NAVER_SEC).local(keyword.strip())
    return resp[0].get("roadAddress", "") if resp else ""


def query_juso(keyword: str) -> dict:
    resp = Jusogokr(JUSO_KEY).addr(keyword.strip())
    if not resp:
        return {}

    elem = resp[0]
    sido = elem.get("siNm", "")
    sgg = elem.get("sggNm", "")
    road = elem.get("rn", "")
    buld_main = elem.get("buldMnnm", "")
    buld_sub = elem.get("buldSlno", "")
    buld = buld_main if buld_sub == "0" else f"{buld_main}-{buld_sub}"
    return dict(sido=sido, sgg=sgg, road=road, buld=buld)


def verify_road_address(idx, addr: str, br_name: str) -> dict:
    if not addr.strip() or not br_name.strip():
        return dict(idx=idx)

    verified = query_juso(addr)
    if not verified:
        logger.warning(f"{idx=}, {br_name=}, {addr=}, not found at jusogokr, try kakao")
        if addr_kakao := query_kakao(br_name):
            verified = query_juso(addr_kakao)

    if not verified:
        logger.warning(f"{idx=}, {br_name=}, {addr=}, not found at kakao, try naver")
        if addr_naver := query_naver(br_name):
            verified = query_juso(addr_naver)

    if not verified:
        logger.error(f"{idx=}, {br_name=}, {addr=}, not found at naver, skip this row")

    return dict(idx=idx, **verified)


def main():
    df_raw = load_excel()
    df_query = df_raw.query("점포구분=='지점' and 은행명=='산업은행'").sort_values(["은행명", "점포명"]).reset_index(drop=True)
    # df_query = df_raw.query("점포구분=='지점'").sort_values(["은행명", "점포명"]).reset_index(drop=True)
    df_filter = df_query.filter(["은행명", "점포명", "점포구분", "시도", "시군구", "도로명"])
    df_filter.head()

    df_filter["도로명"] = df_filter["도로명"].replace(r"\(.+\)", "", regex=True)  # cleansing
    df_filter.to_excel(STEP_1, index=False)

    result = []
    with tqdm(total=df_filter.shape[0]) as pbar:
        # for idx, ser in df_filter.iterrows():
        #     br_name = f'{ser["은행명"]} {ser["점포명"]}'
        #     addr = f'{ser["시도"]} {ser["시군구"]} {ser["도로명"]}'
        #     verified = verify_road_address(idx=idx, addr=addr, br_name=br_name)
        #     result.append(verified)
        #     pbar.update()

        with ThreadPoolExecutor() as executor:
            future_many = []
            for idx, ser in df_filter.iterrows():
                br_name = f'{ser["은행명"]} {ser["점포명"]}'
                addr = f'{ser["시도"]} {ser["시군구"]} {ser["도로명"]}'
                future = executor.submit(verify_road_address, idx=idx, addr=addr, br_name=br_name)
                future_many.append(future)

            for future in as_completed(future_many):
                result.append(future.result())
                pbar.update()

    df_verified = pd.DataFrame.from_dict(result).set_index("idx", drop=True)
    df_result = pd.merge(df_filter, df_verified, left_index=True, right_index=True, how="inner")
    df_result.head()

    same_sido = df_result["시도"] == df_result["sido"]
    same_sgg = df_result["시군구"] == df_result["sgg"]
    same_roadnm = df_result["도로명"] == df_result["road"] + " " + df_result["buld"]
    same_addr = same_sido & same_sgg & same_roadnm

    df_result["is_same"] = False
    df_result.loc[same_addr, "is_same"] = True
    df_result.to_excel(STEP_1, index=False)


if __name__ == "__main__":
    init_output_folder()
    logging.basicConfig(level=logging.INFO, filename=OUTPUT_DIR / "err.log")
    main()
