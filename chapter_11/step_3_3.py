##############################################################################
# 1. 필요모듈
##############################################################################
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_LINE_SPACING
from docx.shared import Mm, Pt
from step_3_1 import add_break_line, apply_font_style
from step_3_2 import STEP_3_2

##############################################################################
# 2. 환경설정
##############################################################################
STEP_1_2 = "output/step_1_2.xlsx"
STEP_1_3 = "output/{}"
STEP_3_1 = "output/step_3_1.docx"
STEP_3_2 = "output/step_3_2.docx"
STEP_3_3 = "output/step_3_3.docx"


##############################################################################
# 3. 기본함수
##############################################################################
def init_style(document):
    style_normal = document.styles["List Bullet"]
    apply_font_style(style_normal, size=Pt(8), bold=False, font_name="나눔고딕")

    p_format = style_normal.paragraph_format
    p_format.space_before = 0
    p_format.space_after = 0
    p_format.line_spacing_rule = WD_LINE_SPACING.SINGLE


##############################################################################
# 4. 메인함수
##############################################################################
def main():
    document = Document(STEP_3_2)
    init_style(document)
    add_break_line(document, 10)

    table = document.add_table(rows=1, cols=1)
    table.style = "Light Shading Accent 6"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.allow_autofit = False

    tr = table.rows[0]
    td = tr.cells[0]
    td.width = Mm(174)

    td.paragraphs[-1].add_run("주의사항")
    td.paragraphs[-1].paragraph_format.space_before = Mm(2)
    td.paragraphs[-1].paragraph_format.space_after = Mm(1)

    td.add_paragraph(
        style="List Bullet"
    ).text = "금융회사의 상품별 이자율 등 거래조건이 수시로 변경되어 지연공시될 수 있으므로 거래전 반드시 해당 금융회사에 문의하시기 바랍니다."
    td.paragraphs[-1].runs[-1].font.bold = False

    td.add_paragraph(
        style="List Bullet"
    ).text = "세전 이자율은 우대조건을 반영하지 않은 기본금리입니다. 상세정보의 우대조건에 해당시 보다 높은 이자율이 적용될 수 있습니다."
    td.paragraphs[-1].runs[-1].font.bold = False

    td.add_paragraph(
        style="List Bullet"
    ).text = "세후 이자율은 이자소득 원천징수세 15.4%(소득세 14%, 지방소득세 1.4%)를 차감한 금리입니다."
    td.paragraphs[-1].runs[-1].font.bold = False
    td.paragraphs[-1].paragraph_format.space_after = Mm(2)

    document.save(STEP_3_3)


##############################################################################
# 5. 실행
##############################################################################
if __name__ == "__main__":
    main()
