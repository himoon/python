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

    p_title = document.add_paragraph("", style="Title")
    print(f"* add_run 실행 전 p_title.runs : {p_title.runs}")

    run_title = p_title.add_run("정기예금 금리 현황표")
    run_title.font.bold = True
    run_title.font.size = Pt(20)
    run_title.font.color.rgb = RGBColor(0x03, 0x43, 0xDF)
    run_title.font.name = "나눔고딕"
    run_title._element.rPr.rFonts.set(qn("w:eastAsia"), "나눔고딕")

    now_format = datetime.now().isoformat(sep=" ", timespec="minutes")
    run_datetime = p_title.add_run(f" ({now_format})")
    run_datetime.font.bold = True
    run_datetime.font.size = Pt(14)
    run_datetime.font.color.rgb = RGBColor.from_string("0343df")
    run_datetime.font.name = "나눔고딕"
    run_datetime._element.rPr.rFonts.set(qn("w:eastAsia"), "나눔고딕")

    style_normal = document.styles["Normal"]
    style_normal.font.size = Pt(10)
    style_normal.font.name = "나눔고딕"
    style_normal._element.rPr.rFonts.set(qn("w:eastAsia"), "나눔고딕")
    p_format = style_normal.paragraph_format
    p_format.space_before = 0
    p_format.space_after = 0
    p_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

    p_blank = document.add_paragraph()
    p_blank.add_run(" ").font.size = Pt(6)

    p_1 = document.add_paragraph("")
    run_1 = p_1.add_run("1. 주요 경제지표")
    run_1.font.bold = True
    run_1.font.size = Pt(14)

    p_blank = document.add_paragraph()
    p_blank.add_run(" ").font.size = Pt(10)

    document.save(STEP_3_1)


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
