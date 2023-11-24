#######################################
# 1. 필요모듈
#######################################
from docx2pdf import convert

import step_0
import step_3_3

#######################################
# 2. 환경설정
#######################################
STEP_3_4 = step_0.OUTPUT_FOLDER / "step_3_4.pdf"


#######################################
# 3. 기본함수
#######################################
pass


#######################################
# 4. 메인함수
#######################################
def main():
    convert(step_3_3.STEP_3_3, STEP_3_4)


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
