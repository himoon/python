#######################################
# 1. 필요모듈
#######################################
from pathlib import Path

#######################################
# 2. 환경설정
#######################################
WORK_DIR = Path(__file__).parent
OUTPUT_DIR = WORK_DIR / "output"


#######################################
# 3. 기본함수
#######################################
def init_output_folder():
    if not OUTPUT_DIR.is_dir():
        print(f"'{OUTPUT_DIR}' 폴더를 생성합니다.")
        OUTPUT_DIR.mkdir()


def clear_output_folder():
    if OUTPUT_DIR.is_dir():
        for path in OUTPUT_DIR.iterdir():
            if path.is_file():
                try:
                    path.unlink()
                except Exception as e:
                    print(e)


#######################################
# 4. 메인함수
#######################################
pass

#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    init_output_folder()
