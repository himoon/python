from __future__ import annotations

import logging
import pathlib
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import step_1
from datakart import Jusogokr, Kakao, Naver, Sgis
from tqdm import tqdm

WORK_DIR = pathlib.Path(__file__).parent
OUTPUT_DIR = WORK_DIR / "output"
IN_EXCEL = WORK_DIR / "banks.xlsx"
STEP_2 = OUTPUT_DIR / "step_2.xlsx"

NAVER_KEY = "4LmEBVOylhQ9Da_Rhryr"
NAVER_SEC = "WwF0cMKQKS"
JUSO_KEY = "devU01TX0FVVEgyMDIzMTIxNDAwMzkyNjExNDM1NDg="
KAKAO_KEY = "2f15ef773b35f21f74877b7ed5122a76"
SGIS_API_KEY = "c45c510fe7854d5aae90"
SGIS_API_SEC = "fde5af5e4362466b91fe"


logger = logging.getLogger(__name__)


def load_excel() -> pd.DataFrame:
    df_raw = pd.read_excel(step_1.STEP_1)
    return df_raw.filter(["은행명", "점포명", "점포구분", "sido", "sgg", "road", "buld"])


def query_x_y(idx, br_name: str, addr: str) -> dict:
    try:
        resp = Sgis(SGIS_API_KEY, SGIS_API_SEC).geocode_wgs84(addr)
        if resp:
            return dict(idx=idx, br_name=br_name, **resp[0])
        return dict(idx=idx, br_name=br_name)
    except Exception as e:
        logger.error(f"{addr=}, {e}")
        return dict(idx=idx, br_name=br_name)


def main():
    df_raw = load_excel()
    df_raw.head()

    result = []
    with tqdm(total=df_raw.shape[0]) as pbar:
        with ThreadPoolExecutor() as executor:
            future_many = []
            for idx, ser in df_raw.iterrows():
                br_name = f'{ser["은행명"]} {ser["점포명"]}{ser["점포구분"]}'
                addr = f'{ser["sido"]} {ser["sgg"]} {ser["road"]} {ser["buld"]}'
                future = executor.submit(query_x_y, idx=idx, br_name=br_name, addr=addr)
                future_many.append(future)

            for future in as_completed(future_many):
                result.append(future.result())
                pbar.update()

    df_x_y = pd.DataFrame.from_dict(result).set_index("idx", drop=True)
    df_x_y = df_x_y.filter(["br_name", "road_nm", "x", "y"])

    df_result = pd.merge(df_raw, df_x_y, left_index=True, right_index=True, how="inner")
    df_result.head()
    df_result.to_excel(STEP_2, index=False)


if __name__ == "__main__":
    step_1.init_output_folder()
    logging.basicConfig(level=logging.INFO, filename=OUTPUT_DIR / "err.log")
    main()
