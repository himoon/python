from __future__ import annotations

import logging
import pathlib

import pandas as pd
from datakart import Jusogokr, Kakao, Naver
from tqdm import tqdm

WORK_DIR = pathlib.Path(__file__).parent
OUTPUT_DIR = WORK_DIR / "output"
IN_EXCEL = WORK_DIR / "banks.xlsx"
OUT_EXCEL = OUTPUT_DIR / "banks_output.xlsx"

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


def main():
    df_raw = load_excel()
    # df_query = df_raw.query("점포구분=='지점' and 은행명=='산업은행'").sort_values(["은행명", "점포명"]).reset_index(drop=True)
    df_query = df_raw.query("점포구분=='지점'").sort_values(["은행명", "점포명"]).reset_index(drop=True)
    df_filter = df_query.filter(["은행명", "점포명", "점포구분", "시도", "시군구", "도로명"])
    df_filter.head()

    df_filter["도로명"] = df_filter["도로명"].replace(r"\(.+\)", "", regex=True)  # cleansing
    df_filter.to_excel(OUT_EXCEL)

    # df_validated.apply(lambda x: print(x.unique()), axis=0)
    df_filter["은행명"].sort_values()
    df_filter["점포명"].sort_values()
    df_filter["점포구분"].sort_values()
    df_filter["시도"].sort_values()
    df_filter["시군구"].sort_values()
    df_filter["도로명"].sort_values()

    juso = Jusogokr(JUSO_KEY)
    naver = Naver(NAVER_KEY, NAVER_SEC)
    kakao = Kakao(KAKAO_KEY)
    # kakao.local_keyword("국민은행 양재PB센터")

    for idx, ser in tqdm(df_filter.iterrows(), total=df_filter.shape[0]):
        # ser = df_validated.loc[884]
        br_name = f'{ser["은행명"]} {ser["점포명"]} {ser["점포구분"]}'
        addr = f'{ser["시도"]} {ser["시군구"]} {ser["도로명"]}'
        if not addr.strip():
            df_filter.loc[idx, "siNm"] = ""
            df_filter.loc[idx, "sggNm"] = ""
            df_filter.loc[idx, "roadNm"] = ""
            continue

        rows = juso.addr(addr)
        if not rows:
            logger.warning(f"* {idx=}, {br_name=}, {addr=}, not found, try kakao")
            kakao_resp = kakao.local_keyword(br_name)
            if kakao_resp:
                kakao_row = kakao_resp[0]
                addr = kakao_row.get("road_address_name", "")
                rows = juso.addr(addr)

        if not rows:
            logger.warning(f"* {idx=}, {br_name=}, {addr=}, not found, try naver")
            naver_resp = naver.local(br_name)
            if naver_resp:
                naver_row = naver_resp[0]
                addr = naver_row.get("roadAddress", "")
                rows = juso.addr(addr)

        if not rows:
            logger.error(f"* {idx=}, {br_name=}, {addr=}, not found, skip this row")
            df_filter.loc[idx, "siNm"] = ""
            df_filter.loc[idx, "sggNm"] = ""
            df_filter.loc[idx, "roadNm"] = ""
            continue

        row = rows[0]
        df_filter.loc[idx, "siNm"] = row.get("siNm", "")
        df_filter.loc[idx, "sggNm"] = row.get("sggNm", "")

        road_nm = row.get("rn", "")
        buld_main = row.get("buldMnnm", "")
        buld_sub = row.get("buldSlno", "")
        buld_nm = buld_main if buld_sub == "0" else f"{buld_main}-{buld_sub}"
        df_filter.loc[idx, "roadNm"] = f"{road_nm} {buld_nm}"

    same_sido = df_filter["시도"] == df_filter["siNm"]
    same_sgg = df_filter["시군구"] == df_filter["sggNm"]
    same_roadnm = df_filter["도로명"] == df_filter["roadNm"]
    same_addr = same_sido & same_sgg & same_roadnm

    df_filter["updated"] = True
    df_filter.loc[same_addr, "updated"] = False
    df_filter.to_excel(OUT_EXCEL, index=False)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename=OUTPUT_DIR / "err.log")
    init_output_folder()
    main()
