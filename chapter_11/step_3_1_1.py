#######################################
# 1. 필요모듈
#######################################
from datetime import datetime

import pandas as pd
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

import step_0
import step_1_2

#######################################
# 2. 환경설정
#######################################
STEP_3_1 = step_0.OUTPUT_FOLDER / "step_3_1.docx"
PAGE_WIDTH, PAGE_HEIGHT, PAGE_MARGIN = Mm(210), Mm(297), Mm(12.7)
GRAPH_WIDTH, GRAPH_HEIGHT = Mm(30), Mm(8)


#######################################
# 3. 기본함수
#######################################
pass


#######################################
# 4. 메인함수
#######################################
def main():
    document = Document()

    for section in document.sections:
        section.page_width = PAGE_WIDTH
        section.page_height = PAGE_HEIGHT
        section.top_margin = PAGE_MARGIN
        section.left_margin = PAGE_MARGIN
        section.right_margin = PAGE_MARGIN
        section.bottom_margin = PAGE_MARGIN

    document.add_heading("정기예금 금리 현황표", level=0)
    document.save(STEP_3_1)


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
