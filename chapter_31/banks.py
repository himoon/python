import pathlib

import pandas as pd

WORK_DIR = pathlib.Path(__file__).parent
INPUT = WORK_DIR / "banks.xlsx"
OUTPUT = WORK_DIR / "banks.json"

df_raw = pd.read_excel(INPUT, dtype="str", sheet_name="반기보('23.6월말)")
df_raw.head(5)

df_raw = pd.read_excel(INPUT, dtype="str", sheet_name="반기보('23.6월말)", skiprows=3, header=None)
df_raw.head(5)

df_header = df_raw.iloc[0:2].ffill(axis="rows").ffill(axis="columns")
df_header = df_header.apply(lambda x: ".".join([x for x in x if x]) if len(x.unique()) > 1 else x[0], axis="rows")


df_raw.iloc[2:]

df_raw.columns = df_header


df_raw = pd.read_excel(INPUT, dtype="str", sheet_name="반기보('23.6월말)", skiprows=3)
df_raw.head(5)


df_raw = pd.read_excel(INPUT, dtype="str", sheet_name="반기보('23.6월말)", skiprows=3, header=[0, 1])
df_raw.head(5)

df_raw.iloc[:, 0].unique()
