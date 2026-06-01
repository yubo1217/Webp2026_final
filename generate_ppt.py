from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

BLUE       = RGBColor(0x1A, 0x73, 0xE8)
DARK_BLUE  = RGBColor(0x0D, 0x47, 0xA1)
LIGHT_BLUE = RGBColor(0xE8, 0xF0, 0xFE)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
DARK       = RGBColor(0x20, 0x20, 0x20)
GRAY       = RGBColor(0x5F, 0x63, 0x68)
LIGHT_GRAY = RGBColor(0xF8, 0xF9, 0xFA)
GREEN      = RGBColor(0x34, 0xA8, 0x53)
RED        = RGBColor(0xEA, 0x43, 0x35)
ORANGE     = RGBColor(0xFB, 0xBC, 0x04)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

# ── 工具函式 ─────────────────────────────────────────────

def rect(slide, x, y, w, h, fill=None, line=None, lw=Pt(0)):
    s = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    s.line.width = lw
    if fill:
        s.fill.solid(); s.fill.fore_color.rgb = fill
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = line
    else:
        s.line.fill.background()
    return s

def txt(slide, text, x, y, w, h, size=16, bold=False, color=DARK,
        align=PP_ALIGN.LEFT, italic=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold
    r.font.italic = italic; r.font.color.rgb = color
    return tb

def header(slide, title, subtitle=None):
    rect(slide, 0, 0, 13.33, 1.15, fill=BLUE)
    rect(slide, 0, 1.15, 13.33, 0.05, fill=DARK_BLUE)
    txt(slide, title, 0.5, 0.12, 11, 0.7, size=28, bold=True, color=WHITE)
    if subtitle:
        txt(slide, subtitle, 0.5, 0.72, 10, 0.35,
            size=14, color=RGBColor(0xBB, 0xDE, 0xFB))

def bullets(slide, items, x, y, w, size=18, color=DARK, gap=0.65):
    for i, item in enumerate(items):
        txt(slide, f"•  {item}", x, y + i * gap, w, gap - 0.05,
            size=size, color=color)

def big_card(slide, title, body, x, y, w, h, bg=LIGHT_BLUE, title_color=DARK_BLUE):
    rect(slide, x, y, w, h, fill=bg,
         line=RGBColor(0xC5, 0xD8, 0xFB), lw=Pt(1))
    txt(slide, title, x+0.2, y+0.15, w-0.35, 0.4,
        size=15, bold=True, color=title_color)
    txt(slide, body,  x+0.2, y+0.62, w-0.35, h-0.75,
        size=13, color=DARK)

def flow_box(slide, label, x, y, w=2.2, h=1.3, bg=BLUE):
    rect(slide, x, y, w, h, fill=bg)
    txt(slide, label, x+0.1, y+0.25, w-0.2, h-0.3,
        size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

def arrow(slide, x, y):
    txt(slide, "→", x, y, 0.4, 0.5,
        size=22, bold=True, color=BLUE, align=PP_ALIGN.CENTER)

# ════════════════════════════════════════════════
# Slide 1 — 封面
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 13.33, 7.5, fill=BLUE)
rect(s, 9.5, -1.0, 5.5, 5.5, fill=DARK_BLUE)
rect(s, -1.5, 5.0, 5.0, 5.0, fill=DARK_BLUE)

txt(s, "☁", 1.2, 1.2, 2.0, 1.6, size=64, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, "React Cloud Drive", 1.2, 2.85, 11, 1.1,
    size=46, bold=True, color=WHITE)
txt(s, "全端雲端硬碟系統", 1.2, 3.95, 10, 0.65,
    size=24, color=RGBColor(0xBB, 0xDE, 0xFB))
rect(s, 1.2, 4.72, 2.5, 0.05, fill=WHITE)
txt(s, "React  ·  Django  ·  DRF  ·  SQLite3  ·  MUI",
    1.2, 4.88, 11, 0.42, size=15, color=RGBColor(0x9E, 0xC8, 0xFF))

# ════════════════════════════════════════════════
# Slide 2 — 專案概述
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
header(s, "專案概述")
rect(s, 0, 1.2, 13.33, 6.3, fill=WHITE)

txt(s, "個人化雲端硬碟，支援巢狀資料夾管理與完整使用者認證",
    0.5, 1.45, 12.3, 0.55, size=17, color=GRAY)

features = [
    ("👤", "使用者認證",  "註冊、登入、登出"),
    ("📁", "資料夾管理",  "建立、巢狀、刪除"),
    ("⬆",  "檔案上傳",   "多檔同時，同名覆蓋"),
    ("⬇",  "下載 / 刪除","直連下載，同步清除"),
    ("🔒", "資料隔離",   "每人只能存取自己的資料"),
    ("🌐", "前後端分離", "React + Django REST API"),
]
for i, (icon, title, desc) in enumerate(features):
    col, row = i % 3, i // 3
    cx = 0.5 + col * 4.2
    cy = 2.2 + row * 2.35
    rect(s, cx, cy, 3.95, 2.15, fill=LIGHT_BLUE,
         line=RGBColor(0xC5, 0xD8, 0xFB), lw=Pt(1))
    txt(s, icon,  cx+0.2, cy+0.3,  0.7, 0.75, size=30)
    txt(s, title, cx+1.0, cy+0.28, 2.7, 0.45,
        size=16, bold=True, color=DARK_BLUE)
    txt(s, desc,  cx+1.0, cy+0.82, 2.7, 0.5, size=13, color=GRAY)

# ════════════════════════════════════════════════
# Slide 4 — 系統架構
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
header(s, "系統架構")
rect(s, 0, 1.2, 13.33, 6.3, fill=LIGHT_GRAY)

layers = [
    (BLUE,      "前端層",   "React 19  ·  MUI v9  ·  React Router  ·  fetch API"),
    (DARK_BLUE, "後端層",   "Django 6  ·  Django REST Framework  ·  Token Auth  ·  CORS"),
    (GREEN,     "資料層",   "SQLite3  ·  本地檔案系統 (media/)"),
]
for i, (color, title, sub) in enumerate(layers):
    cy = 1.55 + i * 1.7
    rect(s, 1.0, cy, 9.5, 1.45, fill=color)
    txt(s, title, 1.25, cy+0.2, 2.5, 0.55,
        size=20, bold=True, color=WHITE)
    txt(s, sub, 3.85, cy+0.28, 6.4, 0.55, size=14, color=WHITE)
    if i < 2:
        txt(s, "▼", 5.5, cy+1.45, 0.6, 0.28,
            size=15, bold=True, color=color, align=PP_ALIGN.CENTER)

rect(s, 10.8, 1.55, 2.2, 5.05, fill=WHITE,
     line=RGBColor(0xDA, 0xDC, 0xE0), lw=Pt(1))
txt(s, "通訊", 10.95, 1.65, 1.8, 0.38,
    size=14, bold=True, color=BLUE, align=PP_ALIGN.CENTER)
for i, c in enumerate(["HTTP REST", "Token 認證", "CORS", "FormData"]):
    txt(s, c, 10.9, 2.15+i*0.75, 1.95, 0.6,
        size=13, color=DARK, align=PP_ALIGN.CENTER)

# ════════════════════════════════════════════════
# Slide 5 — 後端技術
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
header(s, "後端技術")
rect(s, 0, 1.2, 13.33, 6.3, fill=WHITE)

pkgs = [
    ("Django 6",              "核心框架、ORM、路由、Admin"),
    ("Django REST Framework", "ViewSet、Serializer、REST API"),
    ("rest_framework.authtoken", "DRF 內建 Token 認證"),
    ("django-cors-headers",   "允許前端跨域呼叫 API"),
    ("SQLite3",               "Django 內建，零設定資料庫"),
]
for i, (pkg, desc) in enumerate(pkgs):
    col, row = i % 2, i // 2
    cx = 0.5 + col * 6.3
    cy = 1.5 + row * 1.72
    if i == 4:
        cx = 3.4; cy = 1.5 + 2 * 1.72
    rect(s, cx, cy, 6.0, 1.52, fill=LIGHT_BLUE,
         line=RGBColor(0xC5, 0xD8, 0xFB), lw=Pt(1))
    txt(s, pkg,  cx+0.22, cy+0.15, 5.6, 0.48,
        size=17, bold=True, color=DARK_BLUE)
    txt(s, desc, cx+0.22, cy+0.75, 5.6, 0.55, size=14, color=GRAY)

# ════════════════════════════════════════════════
# Slide 6 — 資料模型
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
header(s, "資料模型")
rect(s, 0, 1.2, 13.33, 6.3, fill=LIGHT_GRAY)

# Folder 表
rect(s, 0.5, 1.45, 3.8, 3.8, fill=WHITE, line=BLUE, lw=Pt(2))
rect(s, 0.5, 1.45, 3.8, 0.5, fill=BLUE)
txt(s, "Folder", 0.65, 1.5, 3.5, 0.38, size=17, bold=True, color=WHITE)
for i, (f, t) in enumerate([
    ("id",          "BigInt  PK"),
    ("name",        "CharField"),
    ("parent",      "FK → self  (nullable)"),
    ("user",        "FK → User"),
    ("created_at",  "DateTime"),
]):
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    rect(s, 0.5, 1.95+i*0.45, 3.8, 0.44, fill=bg)
    txt(s, f, 0.65, 1.99+i*0.45, 1.5, 0.36, size=13, color=DARK)
    txt(s, t, 2.2,  1.99+i*0.45, 1.9, 0.36, size=12, color=GRAY)

# File 表
rect(s, 5.0, 1.45, 3.8, 4.65, fill=WHITE, line=GREEN, lw=Pt(2))
rect(s, 5.0, 1.45, 3.8, 0.5, fill=GREEN)
txt(s, "File", 5.15, 1.5, 3.5, 0.38, size=17, bold=True, color=WHITE)
for i, (f, t) in enumerate([
    ("id",          "BigInt  PK"),
    ("name",        "CharField"),
    ("file",        "FileField"),
    ("size",        "BigInt"),
    ("mime_type",   "CharField"),
    ("folder",      "FK → Folder (nullable)"),
    ("user",        "FK → User"),
    ("created_at",  "DateTime"),
]):
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    rect(s, 5.0, 1.95+i*0.42, 3.8, 0.41, fill=bg)
    txt(s, f, 5.15, 1.98+i*0.42, 1.5, 0.34, size=12, color=DARK)
    txt(s, t, 6.65, 1.98+i*0.42, 1.9, 0.34, size=11, color=GRAY)

# 關聯說明
rect(s, 9.2, 1.45, 3.8, 3.8, fill=WHITE,
     line=RGBColor(0xDA, 0xDC, 0xE0), lw=Pt(1))
txt(s, "關聯關係", 9.35, 1.55, 3.4, 0.38,
    size=16, bold=True, color=DARK_BLUE)
rels = [
    "User ──→ Folder  (1:N)",
    "User ──→ File    (1:N)",
    "Folder → Folder  (自參考)",
    "Folder → File    (1:N)",
]
for i, r in enumerate(rels):
    txt(s, r, 9.35, 2.1+i*0.7, 3.5, 0.58,
        size=14, bold=True, color=DARK_BLUE if i < 2 else BLUE)

# 儲存路徑
rect(s, 0.5, 6.22, 12.5, 0.72, fill=LIGHT_BLUE,
     line=RGBColor(0xC5, 0xD8, 0xFB), lw=Pt(1))
txt(s, "檔案路徑：  media / files / {user_id} / {folder_id} / {filename}",
    0.7, 6.35, 12.0, 0.45, size=15, bold=True, color=DARK_BLUE)

# ════════════════════════════════════════════════
# Slide 7a — API 端點（認證）
# ════════════════════════════════════════════════
def _api_table(slide, rows, col_x, col_w, row_h=0.72, start_y=1.75):
    mc = {"GET": GREEN, "POST": BLUE, "DELETE": RED}
    pc = {"公開": ORANGE, "認證": BLUE}
    for i, (method, ep, perm, desc) in enumerate(rows):
        bg = WHITE if i % 2 == 0 else LIGHT_GRAY
        cy = start_y + i * row_h
        rect(slide, 0.3, cy, 12.9, row_h - 0.04, fill=bg)
        rect(slide, 0.36, cy + row_h*0.18, 1.4, row_h*0.58, fill=mc.get(method, GRAY))
        txt(slide, method, 0.36, cy + row_h*0.2, 1.4, row_h*0.5,
            size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        txt(slide, ep,   1.94, cy + row_h*0.2,  3.8, row_h*0.55, size=14, color=DARK)
        rect(slide, 5.91, cy + row_h*0.2, 2.35, row_h*0.5, fill=pc.get(perm, GRAY))
        txt(slide, perm, 5.91, cy + row_h*0.22, 2.35, row_h*0.45,
            size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        txt(slide, desc, 8.46, cy + row_h*0.2,  4.65, row_h*0.55, size=14, color=DARK)

col_x = [0.3, 1.88, 5.85, 8.4]
col_w = [1.53, 3.92, 2.5,  4.8]
heads = ["Method", "Endpoint", "權限", "說明"]

s = prs.slides.add_slide(BLANK)
header(s, "API 端點  —  認證")
rect(s, 0, 1.2, 13.33, 6.3, fill=WHITE)
txt(s, "使用者認證相關端點（無需登入即可呼叫的為「公開」）",
    0.5, 1.35, 12.3, 0.38, size=14, color=GRAY)
for x, w, h in zip(col_x, col_w, heads):
    rect(s, x, 1.8, w, 0.5, fill=BLUE)
    txt(s, h, x+0.08, 1.84, w-0.12, 0.38,
        size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
_api_table(s, [
    ("POST", "/api/auth/register/", "公開", "建立新帳號"),
    ("POST", "/api/auth/login/",    "公開", "登入，回傳 Token"),
    ("POST", "/api/auth/logout/",   "認證", "刪除 Token，登出"),
    ("GET",  "/api/auth/me/",       "認證", "取得目前登入使用者資訊"),
], col_x, col_w, row_h=0.82, start_y=2.38)

# ════════════════════════════════════════════════
# Slide 7b — API 端點（資料夾 & 檔案）
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
header(s, "API 端點  —  資料夾 & 檔案")
rect(s, 0, 1.2, 13.33, 6.3, fill=WHITE)
txt(s, "所有資料夾 / 檔案 API 均須附上 Authorization: Token <token>",
    0.5, 1.35, 12.3, 0.38, size=14, color=GRAY)
for x, w, h in zip(col_x, col_w, heads):
    rect(s, x, 1.8, w, 0.5, fill=BLUE)
    txt(s, h, x+0.08, 1.84, w-0.12, 0.38,
        size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
_api_table(s, [
    ("GET",    "/api/folders/",             "認證", "列出目前使用者的所有資料夾"),
    ("POST",   "/api/folders/",             "認證", "建立資料夾（可指定 parent）"),
    ("DELETE", "/api/folders/{id}/",        "認證", "刪除資料夾及其內容"),
    ("GET",    "/api/files/",               "認證", "列出目前使用者的所有檔案"),
    ("POST",   "/api/files/",               "認證", "上傳檔案（FormData，含 folder_id）"),
    ("GET",    "/api/files/{id}/download/", "認證", "下載檔案（回傳附件 FileResponse）"),
    ("DELETE", "/api/files/{id}/",          "認證", "刪除檔案並移除磁碟上的實體檔"),
], col_x, col_w, row_h=0.63, start_y=2.38)

# ════════════════════════════════════════════════
# Slide 8 — Token 認證
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
header(s, "Token 認證")
rect(s, 0, 1.2, 13.33, 6.3, fill=LIGHT_GRAY)

txt(s, "登入流程", 0.5, 1.38, 4, 0.42,
    size=16, bold=True, color=DARK_BLUE)
steps = [
    "帳號 +\n密碼",
    "POST\n/auth/login/",
    "驗證身份\nauthenticate()",
    "回傳\nToken",
    "存入\nlocalStorage",
]
for i, label in enumerate(steps):
    flow_box(s, label, 0.5 + i*2.42, 1.88, w=2.2, h=1.4,
             bg=BLUE if i != 0 else DARK_BLUE)
    if i < 4:
        arrow(s, 2.72 + i*2.42, 2.38)

txt(s, "之後每次請求", 0.5, 3.58, 5, 0.42,
    size=16, bold=True, color=DARK_BLUE)
req_steps = [
    "發送\nAPI 請求",
    "自動帶入\nAuthorization:\nToken xxx",
    "後端驗證\nToken",
    "回傳\n資料",
]
for i, label in enumerate(req_steps):
    flow_box(s, label, 0.5 + i*2.95, 4.08, w=2.7, h=1.45, bg=DARK_BLUE)
    if i < 3:
        arrow(s, 3.22 + i*2.95, 4.6)

rect(s, 0.5, 5.82, 12.4, 0.55, fill=WHITE,
     line=RGBColor(0xDA, 0xDC, 0xE0), lw=Pt(1))
txt(s, "登出：後端刪除 DB 中的 Token 記錄，前端清除 localStorage",
    0.7, 5.9, 12.0, 0.38, size=14, color=DARK)

# ════════════════════════════════════════════════
# Slide 9 — 前端技術
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
header(s, "前端技術")
rect(s, 0, 1.2, 13.33, 6.3, fill=WHITE)

techs = [
    ("React 19",         "UI 框架，元件化開發"),
    ("MUI v9",           "Material Design 元件庫"),
    ("React Router v7",  "頁面路由，PrivateRoute 保護"),
    ("fetch API",        "瀏覽器內建，無需安裝套件"),
    ("Context API",      "全域認證狀態管理"),
    ("Custom Hook",      "useFolder 封裝資料存取邏輯"),
]
for i, (tech, desc) in enumerate(techs):
    col, row = i % 2, i // 2
    cx = 0.5 + col * 6.35
    cy = 1.5 + row * 1.72
    rect(s, cx, cy, 6.1, 1.52, fill=LIGHT_BLUE,
         line=RGBColor(0xC5, 0xD8, 0xFB), lw=Pt(1))
    txt(s, tech, cx+0.22, cy+0.15, 5.7, 0.48,
        size=17, bold=True, color=DARK_BLUE)
    txt(s, desc, cx+0.22, cy+0.75, 5.7, 0.55, size=14, color=GRAY)

# ════════════════════════════════════════════════
# Slide 10 — API Client
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
header(s, "API Client  ( src/api/client.js )")
rect(s, 0, 1.2, 13.33, 6.3, fill=WHITE)

txt(s, "封裝 fetch API，提供三個方法供全專案使用",
    0.5, 1.45, 12.3, 0.48, size=17, color=GRAY)

methods = [
    ("client.get(path)",         "取得資料，自動帶入 Token"),
    ("client.post(path, body)",  "新增資料或登入，支援 JSON 與 FormData"),
    ("client.delete(path)",      "刪除資源"),
]
for i, (m, d) in enumerate(methods):
    cy = 2.15 + i * 1.55
    rect(s, 0.5, cy, 12.3, 1.35, fill=LIGHT_GRAY,
         line=RGBColor(0xDA, 0xDC, 0xE0), lw=Pt(1))
    rect(s, 0.5, cy, 0.12, 1.35, fill=BLUE)
    txt(s, m, 0.78, cy+0.15, 7.0, 0.48,
        size=18, bold=True, color=DARK_BLUE)
    txt(s, d, 0.78, cy+0.72, 11.8, 0.48, size=14, color=GRAY)

rect(s, 0.5, 6.8, 12.3, 0.45, fill=LIGHT_BLUE,
     line=RGBColor(0xC5, 0xD8, 0xFB), lw=Pt(1))
txt(s, "每次請求自動從 localStorage 取出 token 並帶入 Authorization header",
    0.7, 6.88, 12.0, 0.3, size=13, bold=True, color=DARK_BLUE)

# ════════════════════════════════════════════════
# Slide 11 — 狀態管理
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
header(s, "狀態管理")
rect(s, 0, 1.2, 13.33, 6.3, fill=LIGHT_GRAY)

# AuthContext
rect(s, 0.4, 1.4, 5.9, 5.3, fill=WHITE,
     line=RGBColor(0xDA, 0xDC, 0xE0), lw=Pt(1))
rect(s, 0.4, 1.4, 5.9, 0.52, fill=BLUE)
txt(s, "AuthContext", 0.58, 1.46, 5.5, 0.38,
    size=17, bold=True, color=WHITE)
txt(s, "全域認證狀態，透過 useAuth() 取得",
    0.58, 2.05, 5.5, 0.38, size=13, color=GRAY)
for i, (name, desc) in enumerate([
    ("currentUser",  "登入中的使用者（null = 未登入）"),
    ("login()",      "取得 Token，存入 localStorage"),
    ("register()",   "註冊後自動呼叫 login()"),
    ("logout()",     "刪除 Token，導向登入頁"),
]):
    cy = 2.58 + i * 0.98
    rect(s, 0.55, cy, 5.6, 0.82, fill=LIGHT_BLUE,
         line=RGBColor(0xC5, 0xD8, 0xFB), lw=Pt(1))
    txt(s, name, 0.72, cy+0.08, 1.9, 0.32,
        size=14, bold=True, color=DARK_BLUE)
    txt(s, desc, 0.72, cy+0.46, 5.2, 0.28, size=12, color=GRAY)

# useFolder
rect(s, 6.75, 1.4, 6.15, 5.3, fill=WHITE,
     line=RGBColor(0xDA, 0xDC, 0xE0), lw=Pt(1))
rect(s, 6.75, 1.4, 6.15, 0.52, fill=GREEN)
txt(s, "useFolder(folderId)", 6.93, 1.46, 5.8, 0.38,
    size=17, bold=True, color=WHITE)
txt(s, "管理資料夾內容，封裝 API 呼叫",
    6.93, 2.05, 5.8, 0.38, size=13, color=GRAY)
for i, (name, desc) in enumerate([
    ("folder",       "目前資料夾"),
    ("childFolders", "子資料夾陣列"),
    ("childFiles",   "子檔案陣列"),
    ("loading",      "載入狀態"),
    ("refresh()",    "操作後手動刷新"),
]):
    cy = 2.58 + i * 0.82
    rect(s, 6.9, cy, 5.85, 0.68, fill=LIGHT_BLUE,
         line=RGBColor(0xC5, 0xD8, 0xFB), lw=Pt(1))
    txt(s, name, 7.06, cy+0.07, 2.1, 0.3,
        size=14, bold=True, color=GREEN)
    txt(s, desc, 7.06, cy+0.38, 5.5, 0.24, size=12, color=GRAY)

# ════════════════════════════════════════════════
# Slide 12 — 檔案上傳
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
header(s, "檔案上傳")
rect(s, 0, 1.2, 13.33, 6.3, fill=WHITE)

steps = [
    ("1", "選取檔案",  "input[type=file]\n支援多選"),
    ("2", "打包資料",  "FormData\n含 folder_id"),
    ("3", "POST 上傳", "client.post\n('/api/files/')"),
    ("4", "後端儲存",  "寫入 media/\n更新資料庫"),
    ("5", "刷新列表",  "refresh()\n顯示新檔案"),
]
for i, (num, title, sub) in enumerate(steps):
    cx = 0.4 + i * 2.45
    rect(s, cx, 1.55, 2.25, 3.2, fill=LIGHT_BLUE,
         line=RGBColor(0xC5, 0xD8, 0xFB), lw=Pt(1))
    rect(s, cx, 1.55, 2.25, 0.52, fill=BLUE)
    txt(s, num,   cx+0.08, 1.58, 2.1, 0.38,
        size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, title, cx+0.12, 2.22, 2.0, 0.5,
        size=16, bold=True, color=DARK_BLUE, align=PP_ALIGN.CENTER)
    txt(s, sub,   cx+0.12, 2.88, 2.0, 0.75,
        size=13, color=GRAY, align=PP_ALIGN.CENTER)
    if i < 4:
        arrow(s, cx+2.27, 2.88)

rect(s, 0.4, 5.1, 12.5, 1.55, fill=LIGHT_GRAY,
     line=RGBColor(0xDA, 0xDC, 0xE0), lw=Pt(1))
txt(s, "同名覆蓋邏輯", 0.62, 5.18, 5, 0.4,
    size=15, bold=True, color=DARK_BLUE)
txt(s, "查詢相同 name + user + folder  →  若存在則刪除舊檔並更新  →  若不存在則新增",
    0.62, 5.65, 12.1, 0.82, size=14, color=DARK)

# ════════════════════════════════════════════════
# Slide 13 — 資料夾與麵包屑
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
header(s, "資料夾管理與麵包屑")
rect(s, 0, 1.2, 13.33, 6.3, fill=LIGHT_GRAY)

# 左：資料夾
rect(s, 0.4, 1.42, 5.9, 5.18, fill=WHITE,
     line=RGBColor(0xDA, 0xDC, 0xE0), lw=Pt(1))
rect(s, 0.4, 1.42, 5.9, 0.5, fill=BLUE)
txt(s, "資料夾管理", 0.58, 1.48, 5.5, 0.36,
    size=16, bold=True, color=WHITE)
bullets(s, [
    "POST /api/folders/  { name, parent }",
    "parent = null → 根目錄",
    "parent = id → 子資料夾",
    "DELETE /api/folders/{id}/",
], 0.58, 2.1, 5.5, size=14, gap=0.72)

txt(s, "階層示例", 0.58, 5.0, 2.5, 0.36,
    size=13, bold=True, color=DARK_BLUE)
for i, line in enumerate([
    "My Drive  (parent=null)",
    "  └─ 工作  (parent=根.id)",
    "       └─ 2025  (parent=工作.id)",
]):
    txt(s, line, 0.58, 5.42+i*0.35, 5.5, 0.32, size=12, color=GRAY)

# 右：麵包屑
rect(s, 6.6, 1.42, 6.35, 5.18, fill=WHITE,
     line=RGBColor(0xDA, 0xDC, 0xE0), lw=Pt(1))
rect(s, 6.6, 1.42, 6.35, 0.5, fill=GREEN)
txt(s, "麵包屑導航  Breadcrumb.js", 6.78, 1.48, 6.0, 0.36,
    size=16, bold=True, color=WHITE)
bc_items = [
    ("My Drive",    "首頁，不可點擊"),
    ("中間資料夾",  "可點擊，導向 /folder/{id}"),
    ("當前資料夾",  "純文字，表示目前位置"),
]
for i, (key, val) in enumerate(bc_items):
    cy = 2.12 + i * 1.25
    rect(s, 6.75, cy, 6.05, 1.05, fill=LIGHT_BLUE,
         line=RGBColor(0xC5, 0xD8, 0xFB), lw=Pt(1))
    txt(s, key, 6.92, cy+0.1, 2.2, 0.38,
        size=15, bold=True, color=DARK_BLUE)
    txt(s, val, 6.92, cy+0.58, 5.7, 0.34, size=13, color=GRAY)

txt(s, "示例：  My Drive  /  工作  /  2025",
    6.75, 5.78, 6.05, 0.42,
    size=14, bold=True, color=DARK_BLUE)

# ════════════════════════════════════════════════
# Slide 14 — UI 元件
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
header(s, "UI 元件設計  ( Material-UI )")
rect(s, 0, 1.2, 13.33, 6.3, fill=WHITE)

# 色票
txt(s, "主題色彩", 0.5, 1.35, 3, 0.38,
    size=15, bold=True, color=DARK)
palette = [
    (BLUE,       "#1A73E8"),
    (DARK_BLUE,  "#0D47A1"),
    (GREEN,      "#34A853"),
    (RED,        "#EA4335"),
    (ORANGE,     "#FBBC04"),
]
for i, (color, hex_val) in enumerate(palette):
    cx = 0.5 + i * 2.38
    rect(s, cx, 1.8, 2.15, 0.62, fill=color,
         line=RGBColor(0xDA, 0xDC, 0xE0), lw=Pt(1))
    txt(s, hex_val, cx+0.08, 1.85, 2.0, 0.3,
        size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

comps = [
    ("Navbar",        "AppBar + Avatar",     "固定頂部，顯示使用者，含登出"),
    ("FolderItem",    "Card + ActionArea",   "點擊進資料夾，右鍵選單刪除"),
    ("FileItem",      "Card + Download",     "依 mime_type 顯示不同圖示"),
    ("UploadButton",  "Button + Loading",    "上傳中顯示轉圈，完成後提示"),
    ("Login/Register","Paper + TextField",   "單欄置中，表單驗證"),
    ("Breadcrumb",    "MUI Breadcrumbs",     "可點擊路徑導航"),
]
for i, (comp, tech, desc) in enumerate(comps):
    col, row = i % 3, i // 3
    cx = 0.5 + col * 4.24
    cy = 2.72 + row * 1.85
    rect(s, cx, cy, 4.0, 1.68, fill=LIGHT_GRAY,
         line=RGBColor(0xDA, 0xDC, 0xE0), lw=Pt(1))
    txt(s, comp, cx+0.18, cy+0.12, 3.6, 0.4,
        size=16, bold=True, color=BLUE)
    txt(s, tech, cx+0.18, cy+0.58, 3.6, 0.32,
        size=12, italic=True, color=DARK_BLUE)
    txt(s, desc, cx+0.18, cy+0.98, 3.6, 0.55, size=12, color=GRAY)

# ════════════════════════════════════════════════
# Slide 15a — 前端目錄結構
# ════════════════════════════════════════════════
CODE = RGBColor(0xAB, 0xB2, 0xBF)

s = prs.slides.add_slide(BLANK)
header(s, "前端目錄結構  ( react_cloud_drive/src/ )")
rect(s, 0, 1.2, 13.33, 6.3, fill=RGBColor(0x1E, 0x22, 0x27))
for i, line in enumerate([
    "api/",
    "  client.js            ←  fetch 封裝，自動帶入 Token Header",
    "contexts/",
    "  AuthContext.js       ←  全域認證狀態（currentUser、login、logout）",
    "hooks/",
    "  useFolder.js         ←  資料夾 / 檔案讀取與刷新",
    "pages/",
    "  DrivePage.js         ←  主頁面，組合所有元件",
    "components/",
    "  Auth/    Login.js    Register.js",
    "  Drive/   FolderItem.js  FileItem.js  UploadButton.js",
    "           Breadcrumb.js  NewFolderDialog.js",
    "  Layout/  Navbar.js",
]):
    txt(s, line, 0.7, 1.55+i*0.46, 12.0, 0.42, size=13, color=CODE)

# ════════════════════════════════════════════════
# Slide 15b — 後端目錄結構
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
header(s, "後端目錄結構  ( django_backend/ )")
rect(s, 0, 1.2, 13.33, 6.3, fill=RGBColor(0x1E, 0x22, 0x27))
for i, line in enumerate([
    "core/",
    "  settings.py          ←  INSTALLED_APPS、Token Auth、CORS、媒體路徑",
    "  urls.py              ←  主路由，include drive.urls",
    "drive/",
    "  models.py            ←  Folder（自參考）、File（含 FileField）",
    "  serializers.py       ←  FolderSerializer、FileSerializer",
    "  views.py             ←  ViewSet + register / login / logout views",
    "  urls.py              ←  /api/ 前綴路由表",
    "media/files/           ←  使用者上傳的實體檔案",
    "db.sqlite3             ←  SQLite 資料庫（零設定）",
    "requirements.txt       ←  Django、DRF、django-cors-headers",
]):
    txt(s, line, 0.7, 1.55+i*0.46, 12.0, 0.42, size=13, color=CODE)

# ════════════════════════════════════════════════
# Slide 16 — 總結
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 13.33, 7.5, fill=BLUE)
rect(s, 9.5, -1.0, 5.5, 5.5, fill=DARK_BLUE)
rect(s, -1.5, 5.0, 5.0, 5.0, fill=DARK_BLUE)

txt(s, "總結", 0.6, 0.4, 12, 0.85,
    size=40, bold=True, color=WHITE)
rect(s, 0.6, 1.25, 3.0, 0.06, fill=WHITE)

items = [
    ("✅", "前後端分離",   "React + Django REST Framework"),
    ("✅", "Token 認證",   "DRF 內建，登入取 Token，自動帶入每次請求"),
    ("✅", "巢狀資料夾",   "自參考外鍵，麵包屑導航"),
    ("✅", "完整檔案管理", "上傳、下載、刪除，同名自動覆蓋"),
    ("✅", "資料安全隔離", "每位使用者只能存取自己的資料"),
    ("✅", "Material UI",  "Google Drive 風格介面"),
]
for i, (icon, title, desc) in enumerate(items):
    cy = 1.52 + i * 0.87
    txt(s, f"{icon}  {title}", 0.6, cy, 4.5, 0.5,
        size=18, bold=True, color=WHITE)
    txt(s, desc, 5.2, cy+0.06, 7.8, 0.38,
        size=15, color=RGBColor(0xBB, 0xDE, 0xFB))

rect(s, 0.6, 7.05, 12.1, 0.05, fill=RGBColor(0xBB, 0xDE, 0xFB))
txt(s, "React Cloud Drive  ·  2025",
    0.6, 7.14, 12.1, 0.28,
    size=13, color=RGBColor(0x9E, 0xC8, 0xFF), align=PP_ALIGN.CENTER)

# ════════════════════════════════════════════════
out = "/home/yubo/Webp2026_final/cloud_drive_presentation.pptx"
prs.save(out)
print(f"✅  已生成：{out}  ({len(prs.slides)} 張投影片)")
