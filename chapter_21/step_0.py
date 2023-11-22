#######################################
# 1. 필요모듈
#######################################
from pathlib import Path

#######################################
# 2. 환경설정
#######################################
API_KEY_DATA_GO = "rrRMoK6NHEsLQc4Y2omMvJBTGnaLe8pZzRqAjoGH+mfOerOQtJudgapObiTi2gl07RWrZjO0ie5yryFlMxGV9A=="
WORKING_FOLDER = Path(__file__).parent
OUTPUT_FOLDER = WORKING_FOLDER / "output"


#######################################
# 3. 기본함수
#######################################
def init_output_folder():
    if not OUTPUT_FOLDER.is_dir():
        print(f"'{OUTPUT_FOLDER}' 폴더를 생성합니다.")
        OUTPUT_FOLDER.mkdir()


def clear_output_folder():
    if OUTPUT_FOLDER.is_dir():
        for path in OUTPUT_FOLDER.iterdir():
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
