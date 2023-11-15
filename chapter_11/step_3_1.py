##############################################################################
# 1. 필요모듈
##############################################################################
from datetime import datetime

import pandas as pd
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

import step_0
import step_1_2

##############################################################################
# 2. 환경설정
##############################################################################
STEP_3_1 = step_0.OUTPUT_FOLDER / "step_3_1.docx"
GRAPH_WIDTH, GRAPH_HEIGHT = Mm(30), Mm(8)


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


def apply_font_style(style, size=None, bold=False, font_name=None, rgb=None):
    this_font = style.font
    if size:
        this_font.size = size
    if bold:
        this_font.bold = True
    if font_name:
        this_font.name = font_name
        style._element.rPr.rFonts.set(qn("w:eastAsia"), font_name)
    if rgb:
        this_font.color.rgb = RGBColor(*rgb)
    return style


def init_style(document):
    style_normal = document.styles["Normal"]
    apply_font_style(style_normal, size=Pt(10), font_name="나눔고딕")

    p_format = style_normal.paragraph_format
    p_format.space_before = 0
    p_format.space_after = 0
    p_format.line_spacing_rule = WD_LINE_SPACING.SINGLE


def get_index_values(df_raw):
    s_value = df_raw["DATA_VALUE"]
    s_diff = s_value.diff()
    s_pct_change = s_value.pct_change()

    value = s_value.iloc[-1]
    diff = s_diff.iloc[-1]
    diff_rate = s_pct_change.iloc[-1]
    rgb = (
        (0xE5, 0x00, 0x00) if diff > 0 else (0x03, 0x43, 0xDF) if diff < 0 else None
    )  # https://xkcd.com/color/rgb/
    dt = s_value.index[-1].to_pydatetime()

    return value, diff, diff_rate, rgb, dt


def get_arrow(diff):
    return "▲" if diff > 0 else "▼" if diff < 0 else ""


def add_break_line(document, pt):
    document.add_paragraph().add_run(" ").font.size = Pt(pt)


##############################################################################
# 4. 메인함수
##############################################################################
def main():
    document = Document()
    set_margin(document)
    init_style(document)

    ##########################################################################
    ##########################################################################
    p_title = document.add_heading("정기예금 금리 현황표", level=0)
    apply_font_style(p_title.runs[-1], Pt(20), True, "나눔고딕")

    now_format = datetime.now().isoformat(sep=" ", timespec="minutes")
    p_title.add_run(f" ({now_format})")
    apply_font_style(p_title.runs[-1], Pt(14), True, "나눔고딕")

    add_break_line(document, 6)

    p_head_1 = document.add_paragraph()
    apply_font_style(p_head_1.add_run("1. 주요 경제지표"), Pt(14), True)

    add_break_line(document, 10)
    document.save(STEP_3_1)

    ##########################################################################
    ##########################################################################
    with pd.ExcelFile(step_1_2.STEP_1_2) as xlsx:
        xlsx.sheet_names
        df_base: pd.DataFrame = pd.read_excel(xlsx, sheet_name="base", index_col="TIME")
        df_tb: pd.DataFrame = pd.read_excel(xlsx, sheet_name="tb", index_col="TIME")
        df_cb: pd.DataFrame = pd.read_excel(xlsx, sheet_name="cb", index_col="TIME")
        df_kospi: pd.DataFrame = pd.read_excel(
            xlsx, sheet_name="kospi", index_col="TIME"
        )
        df_ex: pd.DataFrame = pd.read_excel(xlsx, sheet_name="ex", index_col="TIME")

    ##########################################################################
    ##########################################################################
    table = document.add_table(rows=1, cols=5)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.allow_autofit = False

    CELL_WIDTH = Mm(35.5)
    row_1_1 = table.rows[0]
    for td in row_1_1.cells:
        td.width = CELL_WIDTH

    cell_a, cell_b, cell_c, cell_d, cell_e = row_1_1.cells

    ##########################################################################
    # 기준금리
    ##########################################################################
    value, diff, diff_rate, rgb, dt = get_index_values(df_base)
    change = f"{get_arrow(diff)}{diff:,.2f}  {diff_rate:+,.2%}"

    p1 = cell_a.paragraphs[0]
    p2, p3, p4, p5 = [cell_a.add_paragraph() for _ in range(4)]
    apply_font_style(p1.add_run("기준금리"), Pt(12), True)
    apply_font_style(p2.add_run(f"{value:,.2f}"), Pt(14), True)
    apply_font_style(p3.add_run(change), Pt(10), True, rgb=rgb)
    apply_font_style(
        p5.add_run(dt.strftime("%Y-%m-%d")), Pt(8), True, rgb=(0x92, 0x95, 0x91)
    )
    p4.add_run().add_picture(
        (step_0.OUTPUT_FOLDER / "step_1_3_base_mo.png").as_posix(),
        width=GRAPH_WIDTH,
        height=GRAPH_HEIGHT,
    )
    p4.paragraph_format.space_after = Mm(1)
    p4.paragraph_format.space_before = Mm(1)
    document.save(STEP_3_1)

    ##########################################################################
    # 국고채
    ##########################################################################
    value, diff, diff_rate, rgb, dt = get_index_values(df_tb)
    change = f"{get_arrow(diff)}{diff:,.3f}  {diff_rate:+,.2%}"

    p1 = cell_b.paragraphs[0]
    p2, p3, p4, p5 = [cell_b.add_paragraph() for _ in range(4)]

    apply_font_style(p1.add_run("국고채"), Pt(12), True)
    apply_font_style(p1.add_run("(3Y)"), Pt(8), True)
    apply_font_style(p2.add_run(f"{value:,.3f}"), Pt(14), True)
    apply_font_style(p3.add_run(change), Pt(10), True, rgb=rgb)
    apply_font_style(
        p5.add_run(dt.strftime("%Y-%m-%d")), Pt(8), True, rgb=(0x92, 0x95, 0x91)
    )
    p4.add_run().add_picture(
        (step_0.OUTPUT_FOLDER / "step_1_3_tb.png").as_posix(),
        width=GRAPH_WIDTH,
        height=GRAPH_HEIGHT,
    )
    p4.paragraph_format.space_after = Mm(1)
    p4.paragraph_format.space_before = Mm(1)
    document.save(STEP_3_1)

    ##########################################################################
    # 회사채
    ##########################################################################
    value, diff, diff_rate, rgb, dt = get_index_values(df_cb)
    change = f"{get_arrow(diff)}{diff:,.3f}  {diff_rate:+,.2%}"

    p1 = cell_c.paragraphs[0]
    p2, p3, p4, p5 = [cell_c.add_paragraph() for _ in range(4)]

    apply_font_style(p1.add_run("회사채"), Pt(12), True)
    apply_font_style(p1.add_run("(3Y,AA-)"), Pt(8), True)
    apply_font_style(p2.add_run(f"{value:,.3f}"), Pt(14), True)
    apply_font_style(p3.add_run(change), Pt(10), True, rgb=rgb)
    apply_font_style(
        p5.add_run(dt.strftime("%Y-%m-%d")), Pt(8), True, rgb=(0x92, 0x95, 0x91)
    )
    p4.add_run().add_picture(
        (step_0.OUTPUT_FOLDER / "step_1_3_cb.png").as_posix(),
        width=GRAPH_WIDTH,
        height=GRAPH_HEIGHT,
    )
    p4.paragraph_format.space_after = Mm(1)
    p4.paragraph_format.space_before = Mm(1)
    document.save(STEP_3_1)

    ##########################################################################
    # KOSPI
    ##########################################################################
    value, diff, diff_rate, rgb, dt = get_index_values(df_kospi)
    change = f"{get_arrow(diff)}{diff:,.2f}  {diff_rate:+,.2%}"

    p1 = cell_d.paragraphs[0]
    p2, p3, p4, p5 = [cell_d.add_paragraph() for _ in range(4)]

    apply_font_style(p1.add_run("KOSPI"), Pt(12), True)
    apply_font_style(p2.add_run(f"{value:,.2f}"), Pt(14), True)
    apply_font_style(p3.add_run(change), Pt(10), True, rgb=rgb)
    apply_font_style(
        p5.add_run(dt.strftime("%Y-%m-%d")), Pt(8), True, rgb=(0x92, 0x95, 0x91)
    )
    p4.add_run().add_picture(
        (step_0.OUTPUT_FOLDER / "step_1_3_kospi.png").as_posix(),
        width=GRAPH_WIDTH,
        height=GRAPH_HEIGHT,
    )
    p4.paragraph_format.space_after = Mm(1)
    p4.paragraph_format.space_before = Mm(1)
    document.save(STEP_3_1)

    ##########################################################################
    # 원달러
    ##########################################################################
    value, diff, diff_rate, rgb, dt = get_index_values(df_ex)
    change = f"{get_arrow(diff)}{diff:,.2f}  {diff_rate:+,.2%}"

    p1 = cell_e.paragraphs[0]
    p2, p3, p4, p5 = [cell_e.add_paragraph() for _ in range(4)]

    apply_font_style(p1.add_run("원/달러환율"), Pt(12), True)
    apply_font_style(p2.add_run(f"{value:,.2f}"), Pt(14), True)
    apply_font_style(p3.add_run(change), Pt(10), True, rgb=rgb)
    apply_font_style(
        p5.add_run(dt.strftime("%Y-%m-%d")), Pt(8), True, rgb=(0x92, 0x95, 0x91)
    )
    p4.add_run().add_picture(
        (step_0.OUTPUT_FOLDER / "step_1_3_ex.png").as_posix(),
        width=GRAPH_WIDTH,
        height=GRAPH_HEIGHT,
    )
    p4.paragraph_format.space_after = Mm(1)
    p4.paragraph_format.space_before = Mm(1)
    document.save(STEP_3_1)


##############################################################################
# 5. 실행
##############################################################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
