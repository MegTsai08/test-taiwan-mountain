from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 註冊微軟正黑體（支援繁體中文）
pdfmetrics.registerFont(TTFont("JhengHei", "C:/Windows/Fonts/msjh.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("JhengHei-Bold", "C:/Windows/Fonts/msjhbd.ttc", subfontIndex=0))

# 定義樣式
title_style = ParagraphStyle(
    "Title", fontName="JhengHei-Bold", fontSize=22,
    textColor=colors.HexColor("#2d6a2d"), spaceAfter=4, alignment=1
)
subtitle_style = ParagraphStyle(
    "Subtitle", fontName="JhengHei", fontSize=12,
    textColor=colors.grey, spaceAfter=16, alignment=1
)
heading_style = ParagraphStyle(
    "Heading", fontName="JhengHei-Bold", fontSize=14,
    textColor=colors.HexColor("#2d6a2d"), spaceBefore=16, spaceAfter=6,
    borderPad=4
)
body_style = ParagraphStyle(
    "Body", fontName="JhengHei", fontSize=11,
    leading=20, spaceAfter=6
)
step_style = ParagraphStyle(
    "Step", fontName="JhengHei-Bold", fontSize=12,
    textColor=colors.HexColor("#1a4a1a"), spaceBefore=12, spaceAfter=4
)
code_style = ParagraphStyle(
    "Code", fontName="Courier", fontSize=10,
    leading=16, spaceAfter=4, leftIndent=10
)
# 表格內文字樣式
cell_style = ParagraphStyle(
    "Cell", fontName="JhengHei", fontSize=10, leading=16
)
cell_bold_style = ParagraphStyle(
    "CellBold", fontName="JhengHei-Bold", fontSize=10,
    textColor=colors.white, leading=16, alignment=1
)
cell_center_style = ParagraphStyle(
    "CellCenter", fontName="JhengHei", fontSize=10,
    leading=16, alignment=1
)

def P(text, style=None):
    """快速建立 Paragraph，表格內文字換行用"""
    if style is None:
        style = cell_style
    return Paragraph(text, style)

def code_block(text):
    """灰底程式碼區塊"""
    data = [[Paragraph(text, code_style)]]
    t = Table(data, colWidths=[16*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f0f0f0")),
        ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ("PADDING", (0,0), (-1,-1), 8),
    ]))
    return t

# 建立 PDF
doc = SimpleDocTemplate(
    "C:/Meg_course/test/project/開發筆記.pdf",
    pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2.5*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm
)

story = []

# ── 標題 ──
story.append(Paragraph("台灣百岳查詢網頁", title_style))
story.append(Paragraph("開發流程筆記  |  2026/06/29", subtitle_style))
story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2d6a2d")))
story.append(Spacer(1, 12))

# ── 一、環境確認 ──
story.append(Paragraph("一、開發環境", heading_style))
story.append(Paragraph("開始之前先確認電腦裡有沒有裝好這些工具：", body_style))

env_data = [
    [P("工具", cell_bold_style), P("版本", cell_bold_style), P("用途", cell_bold_style)],
    [P("Python"), P("3.13.13"), P("程式語言")],
    [P("uv"), P("0.11.9"), P("套件管理工具（比 pip 更快）")],
    [P("Flask"), P("3.1.3"), P("Python 網頁框架")],
]
env_table = Table(env_data, colWidths=[3.5*cm, 4*cm, 8.5*cm])
env_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2d6a2d")),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f5fff5")]),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
    ("PADDING", (0,0), (-1,-1), 8),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
]))
story.append(env_table)
story.append(Spacer(1, 6))
story.append(Paragraph("確認指令（在 PowerShell 輸入）：", body_style))
story.append(code_block("python --version<br/>pip --version<br/>uv --version"))
story.append(Spacer(1, 4))

# ── 二、建立專案 ──
story.append(Paragraph("二、建立專案", heading_style))

story.append(Paragraph("步驟 1｜建立專案資料夾", step_style))
story.append(Paragraph("選擇一個位置放專案，這裡放在：", body_style))
story.append(code_block("C:\\Meg_course\\test\\project"))

story.append(Paragraph("步驟 2｜初始化專案", step_style))
story.append(code_block("cd C:\\Meg_course\\test\\project<br/>uv init"))
story.append(Paragraph(
    "這會自動產生 pyproject.toml 設定檔，並指定使用 Python 3.13。", body_style))

story.append(Paragraph("步驟 3｜安裝 Flask", step_style))
story.append(code_block("uv add flask"))
story.append(Paragraph(
    "uv 會自動建立虛擬環境（.venv 資料夾），並把 Flask 及相關套件裝進去。", body_style))

# ── 三、建立程式檔案 ──
story.append(Paragraph("三、建立程式檔案", heading_style))
story.append(Paragraph("專案最終的檔案結構如下：", body_style))
story.append(code_block(
    "project/<br/>"
    "├── app.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Flask 主程式<br/>"
    "├── mountains.json &nbsp;# 百岳資料（30筆）<br/>"
    "├── pyproject.toml &nbsp;# 專案設定（uv自動產生）<br/>"
    "└── templates/<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;├── index.html &nbsp;# 首頁（清單＋搜尋）<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;└── detail.html # 詳細頁面"
))

story.append(Paragraph("步驟 4｜建立 app.py（Flask 主程式）", step_style))
story.append(Paragraph(
    "app.py 是整個網頁的核心，負責：<br/>"
    "・從 mountains.json 讀取百岳資料<br/>"
    "・處理首頁（/）的搜尋功能<br/>"
    "・處理詳細頁面（/mountain/山名）的路由", body_style))

story.append(Paragraph("步驟 5｜建立 templates 資料夾與 index.html", step_style))
story.append(Paragraph(
    "Flask 規定 HTML 檔案必須放在 templates 資料夾裡。<br/>"
    "index.html 是首頁，包含：山岳清單、搜尋框、可點擊的山名連結。", body_style))

story.append(Paragraph("步驟 6｜建立 mountains.json（百岳資料）", step_style))
story.append(Paragraph(
    "把山的資料獨立存成 JSON 檔案，而不是寫死在程式裡。<br/>"
    "好處：資料與程式分開，之後要新增或修改資料只需改 JSON，不用動程式碼。<br/>"
    "目前存放 30 筆百岳資料，每筆包含：山名、海拔、難度、所在縣市、山脈。", body_style))

story.append(Paragraph("步驟 7｜建立 detail.html（詳細頁面）", step_style))
story.append(Paragraph(
    "點擊山名後進入的詳細頁面，顯示該山的完整資訊，並有「返回清單」按鈕。", body_style))

# ── 四、啟動網頁 ──
story.append(Paragraph("四、啟動網頁與測試", heading_style))

story.append(Paragraph("步驟 8｜啟動伺服器", step_style))
story.append(code_block("uv run python app.py"))

story.append(Paragraph("步驟 9｜打開瀏覽器，輸入網址", step_style))
story.append(code_block("http://127.0.0.1:5000"))
story.append(Paragraph("要停止伺服器，在終端機按 Ctrl+C。", body_style))

# ── 五、遇到的 Bug ──
story.append(Paragraph("五、今天遇到的 Bug", heading_style))

bug_data = [
    [P("問題", cell_bold_style), P("原因", cell_bold_style), P("解法", cell_bold_style)],
    [
        P("網頁出現錯誤，沒有顯示 30 筆資料"),
        P("存檔時檔名多了中文逗號，存成 mountains.json，"),
        P("重新建立正確的 mountains.json")
    ],
    [
        P("修正後網頁沒有變化"),
        P("伺服器因找不到檔案而當掉了"),
        P("按 Ctrl+C 重啟伺服器，再執行 uv run python app.py")
    ],
]
bug_table = Table(bug_data, colWidths=[4.5*cm, 6*cm, 5.5*cm])
bug_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#cc3333")),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#fff5f5")]),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
    ("PADDING", (0,0), (-1,-1), 8),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
]))
story.append(bug_table)
story.append(Spacer(1, 8))

# ── 六、完成度 ──
story.append(Paragraph("六、目前完成度：約 55%", heading_style))

done_data = [
    [P("狀態", cell_bold_style), P("功能", cell_bold_style)],
    [P("完成"), P("基本網頁架構（Flask + HTML）")],
    [P("完成"), P("顯示 30 筆百岳清單")],
    [P("完成"), P("搜尋功能（輸入山名過濾）")],
    [P("完成"), P("資料獨立成 JSON 檔案")],
    [P("完成"), P("單一山岳詳細頁面")],
    [P("待完成"), P("排序功能（依高度或難度）")],
    [P("待完成"), P("介面美化")],
    [P("待完成"), P("補齊完整 100 筆百岳資料")],
]
done_table = Table(done_data, colWidths=[3.5*cm, 12.5*cm])
done_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2d6a2d")),
    ("BACKGROUND", (0,1), (0,5), colors.HexColor("#e8f5e8")),
    ("BACKGROUND", (0,6), (0,8), colors.HexColor("#fff0f0")),
    ("ROWBACKGROUNDS", (1,1), (-1,-1), [colors.white, colors.HexColor("#fafafa")]),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
    ("PADDING", (0,0), (-1,-1), 8),
    ("ALIGN", (0,1), (0,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
]))
story.append(done_table)
story.append(Spacer(1, 8))

# ── 七、下次繼續 ──
story.append(Paragraph("七、下次繼續", heading_style))
story.append(Paragraph(
    "1. 美化介面（CSS 樣式調整）<br/>"
    "2. 加入排序功能（依海拔高度或難度排序）<br/>"
    "3. 補齊完整 100 筆百岳資料",
    body_style))

story.append(Spacer(1, 20))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2d6a2d")))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "第一天開發到這裡，從零到有網頁跑起來，非常棒！繼續加油！",
    subtitle_style))

# 產生 PDF
doc.build(story)
print("PDF 產生成功！")
