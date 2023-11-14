##############################################################################
# 1. 필요모듈
##############################################################################
import json
import pandas as pd

from docx import Document
from docx.shared import Inches, Cm, Pt, Mm
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_LINE_SPACING
from docx.enum.style import WD_STYLE
from docx.oxml.ns import qn, nsdecls


import matplotlib.pyplot as plt
import numpy as np
import time


##############################################################################
# 2. 환경설정
##############################################################################
STEP_1_2 = "output/step_1_2.xlsx"
STEP_1_3 = "output/{}"
STEP_3_1 = "output/step_3_1.docx"
TEMPLATE = "template.docx"


##############################################################################
# 3. 기본함수
##############################################################################
def set_margin(document, margin=12.7):
    for section in document.sections:
        section.top_margin = Mm(margin)
        section.bottom_margin = Mm(margin)
        section.left_margin = Mm(margin)
        section.right_margin = Mm(margin)
        section.page_width = Mm(210)
        section.page_height = Mm(297)


def init_style(document):
    style = document.styles["Normal"]
    style.font.name = "나눔고딕"
    style.font.size = Pt(10)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "나눔고딕")  # 한글 폰트를 따로 설정해 준다

    paragraph_format = style.paragraph_format
    paragraph_format.space_before = Pt(0)
    paragraph_format.space_after = Pt(0)
    paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    # style = styles.add_style("normal_py", WD_STYLE_TYPE.PARAGRAPH)
    # style.base_style = styles["Normal"]


def get_value_changes(df_raw):
    s_value = df_raw["DATA_VALUE"]
    s_diff = s_value.diff()
    s_pct_change = s_value.pct_change()

    value = s_value.iloc[-1]
    diff = s_diff.iloc[-1]
    diff_rate = s_pct_change.iloc[-1]
    date_string = s_value.index[-1].strftime("'%y.%m.%d.")
    return value, diff, diff_rate, date_string


##############################################################################
# 4. 메인함수
##############################################################################
def main():
    document = Document()
    set_margin(document)
    init_style(document)

    ##########################################################################
    ##########################################################################
    with pd.ExcelFile(STEP_1_2) as xlsx:
        xlsx.sheet_names
        df_bok: pd.DataFrame = pd.read_excel(xlsx, sheet_name="bok", index_col="TIME")
        df_tb: pd.DataFrame = pd.read_excel(xlsx, sheet_name="tb", index_col="TIME")
        df_cb: pd.DataFrame = pd.read_excel(xlsx, sheet_name="cb", index_col="TIME")
        df_kospi: pd.DataFrame = pd.read_excel(
            xlsx, sheet_name="kospi", index_col="TIME"
        )
        df_ex: pd.DataFrame = pd.read_excel(xlsx, sheet_name="ex", index_col="TIME")

    ##########################################################################
    ##########################################################################
    table = document.add_table(rows=1, cols=5)
    row_1_1 = table.rows[0]
    cell_bok, cell_tb, cell_cb, cell_kospi, cell_ex = row_1_1.cells

    ##########################################################################
    # 기준금리
    ##########################################################################
    value, diff, diff_rate, date_string = get_value_changes(df_bok)
    arrow = "" if not value else "▼" if value < 0 else "▲"
    change = f"{arrow}{diff:,.3f}  {diff_rate:+,.2%}"

    p1 = cell_bok.paragraphs[0]
    p2, p3, p4, p5 = [cell_bok.add_paragraph() for _ in range(4)]

    p1.add_run("기준금리").bold = True
    p1.runs[-1].font.size = Pt(14)

    p2.add_run(f"{value:,.3f}").bold = True
    p2.runs[-1].font.size = Pt(20)

    p3.add_run(change).bold = True  # diff, pct_change
    p3.runs[-1].font.size = Pt(10)

    p4.add_run().add_picture(f"output/grah_bok.png", width=Mm(24), height=Mm(8))

    p5.add_run(date_string).bold = True
    p5.runs[-1].font.size = Pt(8)

    document.save(STEP_3_1)

    ##########################################################################
    # 국고채
    ##########################################################################
    value, diff, diff_rate, date_string = get_value_changes(df_tb)
    arrow = "" if not value else "▼" if value < 0 else "▲"
    change = f"{arrow}{diff:,.3f}  {diff_rate:+,.2%}"

    p1 = cell_tb.paragraphs[0]
    p2, p3, p4, p5 = [cell_tb.add_paragraph() for _ in range(4)]

    p1.add_run("국고채").bold = True
    p1.runs[-1].font.size = Pt(14)
    p1.add_run("(3Y)").bold = True
    p1.runs[-1].font.size = Pt(8)

    p2.add_run(f"{value:,.3f}").bold = True
    p2.runs[-1].font.size = Pt(20)

    p3.add_run(change).bold = True  # diff, pct_change
    p3.runs[-1].font.size = Pt(10)

    p4.add_run().add_picture(f"output/grah_tb.png", width=Mm(24), height=Mm(8))

    p5.add_run(date_string).bold = True
    p5.runs[-1].font.size = Pt(8)

    document.save(STEP_3_1)

    ##########################################################################
    # 회사채
    ##########################################################################
    value, diff, diff_rate, date_string = get_value_changes(df_cb)
    arrow = "" if not value else "▼" if value < 0 else "▲"
    change = f"{arrow}{diff:,.3f}  {diff_rate:+,.2%}"

    p1 = cell_cb.paragraphs[0]
    p2, p3, p4, p5 = [cell_cb.add_paragraph() for _ in range(4)]

    p1.add_run("회사채").bold = True
    p1.runs[-1].font.size = Pt(14)
    p1.add_run("(3Y,AA-)").bold = True
    p1.runs[-1].font.size = Pt(8)

    p2.add_run(f"{value:,.3f}").bold = True
    p2.runs[-1].font.size = Pt(20)

    p3.add_run(change).bold = True  # diff, pct_change
    p3.runs[-1].font.size = Pt(10)

    p4.add_run().add_picture(f"output/grah_cb.png", width=Mm(24), height=Mm(8))

    p5.add_run(date_string).bold = True
    p5.runs[-1].font.size = Pt(8)

    document.save(STEP_3_1)

    ##########################################################################
    # KOSPI
    ##########################################################################
    value, diff, diff_rate, date_string = get_value_changes(df_kospi)
    arrow = "" if not value else "▼" if value < 0 else "▲"
    change = f"{arrow}{diff:,.2f}  {diff_rate:+,.2%}"

    p1 = cell_kospi.paragraphs[0]
    p2, p3, p4, p5 = [cell_kospi.add_paragraph() for _ in range(4)]

    p1.add_run("KOSPI").bold = True
    p1.runs[-1].font.size = Pt(14)

    p2.add_run(f"{value:,.2f}").bold = True
    p2.runs[-1].font.size = Pt(20)

    p3.add_run(change).bold = True  # diff, pct_change
    p3.runs[-1].font.size = Pt(10)

    p4.add_run().add_picture(f"output/grah_kospi.png", width=Mm(24), height=Mm(8))

    p5.add_run(date_string).bold = True
    p5.runs[-1].font.size = Pt(8)

    document.save(STEP_3_1)

    ##########################################################################
    # 원달러
    ##########################################################################
    value, diff, diff_rate, date_string = get_value_changes(df_ex)
    arrow = "" if not value else "▼" if value < 0 else "▲"
    change = f"{arrow}{diff:,.3f}  {diff_rate:+,.2%}"

    p1 = cell_ex.paragraphs[0]
    p2, p3, p4, p5 = [cell_ex.add_paragraph() for _ in range(4)]

    p1.add_run("원/달러환율").bold = True
    p1.runs[-1].font.size = Pt(14)

    p2.add_run(f"{value:,.3f}").bold = True
    p2.runs[-1].font.size = Pt(20)

    p3.add_run(change).bold = True  # diff, pct_change
    p3.runs[-1].font.size = Pt(10)

    p4.add_run().add_picture(f"output/grah_ex.png", width=Mm(24), height=Mm(8))

    p5.add_run(date_string).bold = True
    p5.runs[-1].font.size = Pt(8)

    document.save(STEP_3_1)

    ##########################################################################
    ##########################################################################
    for _ in range(4):
        cell_cb.add_paragraph()

    p1, p2, p3, p4, p5 = cell_cb.paragraphs

    s_value = df_cb["DATA_VALUE"]
    s_diff = s_value.diff()
    s_pct_change = s_value.pct_change()
    value = s_value.iloc[-1]
    arrow = "" if not value else "▼" if value < 0 else "▲"
    change = f"{arrow}{s_diff.iloc[-1]:,.3f}  {s_pct_change.iloc[-1]:+,.2%}"
    date_string = s_value.index[-1].strftime("%m.%d. 종가")

    p1.add_run("회사채(3Y,AA-)").bold = True
    p2.add_run(f"{s_value.iloc[-1]:,.3f}").bold = True
    p3.add_run(change).bold = True  # diff, pct_change
    p4.add_run().add_picture(f"output/grah_cb.png", width=Mm(24), height=Mm(8))
    p5.add_run(date_string).bold = True

    p1.runs[-1].font.size = Pt(14)
    p2.runs[-1].font.size = Pt(20)
    p5.runs[-1].font.size = Pt(8)
    document.save(STEP_3_1)

    # document.add_paragraph("하하하", style="normal_py")
    # document.add_paragraph("하하하", style="No Spacing")
    # document.add_paragraph("하하하", style="Normal")
    # document.add_paragraph("", style="Normal")
    # document.save(STEP_3_1)

    # document.add_heading("정기예금 금리 현황표", 0)

    header = table.rows[0]
    header_cells = table.rows[0].cells
    header_cells[0].text = "지표명"
    header_cells[1].text = "주기"
    header_cells[2].text = "값"
    header_cells[3].text = "단위"
    header_cells[4].text = "직전대비"
    header_cells[5].text = "등락률"
    header_cells[6].text = "그래프"
    document.save(STEP_3_1)

    table = document.add_table(rows=1, cols=7)
    header = table.rows[0]
    header_cells = table.rows[0].cells
    header_cells[0].text = "지표명"
    header_cells[1].text = "주기"
    header_cells[2].text = "값"
    header_cells[3].text = "단위"
    header_cells[4].text = "직전대비"
    header_cells[5].text = "등락률"
    header_cells[6].text = "그래프"
    document.save(STEP_3_1)

    # table.add_row(style="No Spacing")
    # para0 = hdr_cells[0].add_paragraph(style="")
    # dir(para0.paragraph_format)
    # para0.paragraph_format
    # dir(para0)
    # dir(hdr_cells[0])

    s_last = df_kospi.iloc[-1]
    row_cells = table.add_row().cells
    row_cells[0].text = f'{s_last["ITEM_NAME1"]}'
    row_cells[1].text = "월"
    row_cells[2].text = f'{s_last["DATA_VALUE"]}'
    row_cells[3].text = f'{s_last["UNIT_NAME"]}'

    s_value = df_kospi["DATA_VALUE"]
    row_cells[4].text = f"{s_value.diff().iloc[-1]:+,.2f}"
    row_cells[5].text = f"{s_value.pct_change().iloc[-1]:+,.2%}"

    para = row_cells[6].paragraphs[0]
    run = para.add_run()
    pic = "output/grah_kospi.png"
    run.add_picture(pic, width=1400000, height=1400000)

    for qty, id, desc in records:
        row_cells = table.add_row().cells
        row_cells[0].text = str(qty)
        row_cells[1].text = id
        row_cells[2].text = desc

    document.save(STEP_3_1)

    # p = document.add_paragraph("A plain paragraph having some ")
    # p.add_run("bold").bold = True
    # p.add_run(" and some ")
    # p.add_run("italic.").italic = True

    # document.add_heading("Heading, level 1", level=1)
    # document.add_paragraph("Intense quote", style="Intense Quote")

    # document.add_paragraph("first item in unordered list", style="List Bullet")
    # document.add_paragraph("first item in ordered list", style="List Number")

    # document.add_picture("test.png", width=Inches(1.25))

    records = (
        (3, "101", "Spam"),
        (7, "422", "Eggs"),
        (4, "631", "Spam, spam, eggs, and spam"),
    )

    table = document.add_table(rows=1, cols=3)
    header_cells = table.rows[0].cells
    header_cells[0].text = "Qty"
    header_cells[1].text = "Id"
    header_cells[2].text = "Desc"
    for qty, id, desc in records:
        row_cells = table.add_row().cells
        row_cells[0].text = str(qty)
        row_cells[1].text = id
        row_cells[2].text = desc

    # document.add_page_break()
    # document.save("demo.docx")


##############################################################################
# 5. 실행
##############################################################################
if __name__ == "__main__":
    pass
