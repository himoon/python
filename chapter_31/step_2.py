from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
from datakart import Sgis
from tqdm import tqdm

import step_0
import step_1

STEP_2 = step_0.OUTPUT_DIR / "step_2.xlsx"


logger = logging.getLogger(__name__)


def load_excel() -> pd.DataFrame:
    df_raw = pd.read_excel(step_1.STEP_1)
    return df_raw.filter(["은행명", "점포명", "점포구분", "sido", "sgg", "road", "buld"])


def query_x_y(idx, br_name: str, addr: str) -> dict:
    try:
        resp = Sgis(step_0.SGIS_API_KEY, step_0.SGIS_API_SEC).geocode_wgs84(addr)
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
    step_0.init_output_folder()
    logging.basicConfig(level=logging.INFO, filename=step_0.OUTPUT_DIR / "err.log")
    main()
