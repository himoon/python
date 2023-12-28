import pathlib

WORK_DIR = pathlib.Path(__file__).parent
OUTPUT_DIR = WORK_DIR / "output"

NAVER_KEY = "4LmEBVOylhQ9Da_Rhryr"
NAVER_SEC = "WwF0cMKQKS"
JUSO_KEY = "devU01TX0FVVEgyMDIzMTIxNDAwMzkyNjExNDM1NDg="
KAKAO_KEY = "2f15ef773b35f21f74877b7ed5122a76"
SGIS_API_KEY = "c45c510fe7854d5aae90"
SGIS_API_SEC = "fde5af5e4362466b91fe"


def init_output_folder():
    if not OUTPUT_DIR.is_dir():
        print(f"'{OUTPUT_DIR}' 폴더를 생성합니다.")
        OUTPUT_DIR.mkdir()
