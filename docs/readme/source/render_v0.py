#!/usr/bin/env python3
"""Render the approved README visual system and technical diagrams.

The product UI always comes from a real screenshot. This script only composes
layout, typography and explanatory graphics around that source material.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[3]
ASSETS = ROOT / "assets"
OUT = ROOT / "docs" / "readme" / "rendered"
MEDIA = ROOT / "docs" / "readme" / "media"

W, H = 1600, 900

WHITE = "#FFFFFF"
INK = "#1D1D1F"
MUTED = "#86868B"
SURFACE = "#F5F5F7"
HAIRLINE = "#D2D2D7"
MINT = "#3DD6A5"
MINT_DARK = "#167C62"
CYAN = "#5DDCF6"

FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_MONO = "/System/Library/Fonts/SFNSMono.ttf"


def font(size: int, *, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_MONO if mono else FONT_BOLD if bold else FONT_REGULAR
    return ImageFont.truetype(path, size=size)


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0], size[1]), radius, fill=255)
    return mask


def paste_rounded(
    canvas: Image.Image,
    image: Image.Image,
    box: tuple[int, int, int, int],
    *,
    radius: int,
    shadow: bool = True,
) -> None:
    x0, y0, x1, y1 = box
    size = (x1 - x0, y1 - y0)
    fitted = image.convert("RGB").resize(size, Image.Resampling.LANCZOS)
    mask = rounded_mask(size, radius)

    if shadow:
        shadow_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        shadow_shape = Image.new("L", size, 0)
        ImageDraw.Draw(shadow_shape).rounded_rectangle(
            (0, 0, size[0] - 1, size[1] - 1), radius, fill=34
        )
        shadow_shape = shadow_shape.filter(ImageFilter.GaussianBlur(22))
        shadow_layer.paste((0, 0, 0, 34), (x0, y0 + 18), shadow_shape)
        canvas.alpha_composite(shadow_layer)

    canvas.paste(fitted, (x0, y0), mask)


def save(image: Image.Image, stem: str, *, png: bool = False) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rgb = image.convert("RGB")
    if png:
        rgb.save(OUT / f"{stem}.png", optimize=True)
    rgb.save(OUT / f"{stem}.webp", "WEBP", quality=92, method=6)


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    *,
    size: int,
    fill: str,
    bold: bool = False,
    mono: bool = False,
    anchor: str | None = None,
) -> None:
    draw.text(xy, text, font=font(size, bold=bold, mono=mono), fill=fill, anchor=anchor)


def arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    *,
    fill: str,
    width: int = 4,
    dashed: bool = False,
) -> None:
    x0, y0 = start
    x1, y1 = end
    if dashed:
        segments = 12
        for i in range(segments):
            if i % 2:
                continue
            a = i / segments
            b = min((i + 1) / segments, 1)
            draw.line(
                (x0 + (x1 - x0) * a, y0 + (y1 - y0) * a,
                 x0 + (x1 - x0) * b, y0 + (y1 - y0) * b),
                fill=fill,
                width=width,
            )
    else:
        draw.line((x0, y0, x1, y1), fill=fill, width=width)

    head = 13
    if abs(x1 - x0) >= abs(y1 - y0):
        direction = 1 if x1 >= x0 else -1
        points = [(x1, y1), (x1 - direction * head, y1 - 8), (x1 - direction * head, y1 + 8)]
    else:
        direction = 1 if y1 >= y0 else -1
        points = [(x1, y1), (x1 - 8, y1 - direction * head), (x1 + 8, y1 - direction * head)]
    draw.polygon(points, fill=fill)


def pill(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    label: str,
    *,
    fill: str,
    text_fill: str,
    outline: str | None = None,
) -> None:
    draw.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=fill, outline=outline, width=2)
    draw_text(
        draw,
        ((box[0] + box[2]) // 2, (box[1] + box[3]) // 2),
        label,
        size=21,
        fill=text_fill,
        bold=True,
        anchor="mm",
    )


def render_hero() -> None:
    canvas = Image.new("RGBA", (W, H), WHITE)
    draw = ImageDraw.Draw(canvas)

    icon = Image.open(ASSETS / "pc-icon.png").convert("RGBA").resize((40, 40), Image.Resampling.LANCZOS)
    canvas.alpha_composite(icon, (94, 68))
    draw_text(draw, (150, 88), "云享传靓仔", size=27, fill=INK, bold=True, anchor="lm")
    draw_text(
        draw,
        (96, 164),
        "本机出片。",
        size=68,
        fill=INK,
        bold=True,
    )
    draw_text(
        draw,
        (96, 252),
        "AI 起稿，参数可编辑。",
        size=48,
        fill=INK,
        bold=True,
    )
    draw_text(
        draw,
        (98, 336),
        "活动摄影精修工作台。",
        size=24,
        fill=MUTED,
    )
    draw_text(
        draw,
        (98, 377),
        "弱网继续工作，参数可回退、可批量同步。",
        size=22,
        fill=MUTED,
    )

    # Editorial text links, not button-shaped marketing chrome.
    draw_text(draw, (98, 438), "下载 Mac / Windows", size=22, fill=MINT_DARK, bold=True)
    draw_text(draw, (338, 438), "查看开源组件  ↗", size=22, fill=INK, bold=True)

    screenshot = Image.open(ASSETS / "shot-color.png")
    paste_rounded(canvas, screenshot, (690, 128, 1535, 656), radius=18, shadow=True)

    # Product truths sit on the same baseline and use typography, not cards.
    draw.line((96, 748, 1504, 748), fill=HAIRLINE, width=2)
    facts = [
        ("01", "LOCAL-FIRST", "本机精修主链路"),
        ("02", "EDITABLE AI", "AI 输出可编辑参数"),
        ("03", "ONE WORKFLOW", "导入、精修、同步、导出"),
    ]
    x_positions = [98, 565, 1032]
    for x, (index, english, chinese) in zip(x_positions, facts):
        draw_text(draw, (x, 786), index, size=18, fill=MINT_DARK, mono=True)
        draw_text(draw, (x + 52, 786), english, size=17, fill=MUTED, mono=True)
        draw_text(draw, (x, 830), chinese, size=27, fill=INK, bold=True)

    save(canvas, "hero-workstation")


def stage(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    number: str,
    title: str,
    subtitle: str,
    *,
    active: bool = False,
) -> None:
    fill = "#E9FBF5" if active else WHITE
    outline = MINT if active else HAIRLINE
    draw.rounded_rectangle(box, radius=18, fill=fill, outline=outline, width=3 if active else 2)
    draw_text(draw, (box[0] + 24, box[1] + 25), number, size=17, fill=MINT_DARK, mono=True)
    draw_text(draw, (box[0] + 24, box[1] + 61), title, size=25, fill=INK, bold=True)
    draw_text(draw, (box[0] + 24, box[1] + 100), subtitle, size=17, fill=MUTED)


def render_local_first() -> None:
    canvas = Image.new("RGBA", (W, H), WHITE)
    draw = ImageDraw.Draw(canvas)

    draw_text(draw, (96, 80), "像素留在本机。", size=64, fill=INK, bold=True)
    draw_text(
        draw,
        (98, 164),
        "网络负责授权与用户主动选择的同步；精修主链路在桌面端完成。",
        size=27,
        fill=MUTED,
    )

    # Main local boundary.
    draw.rounded_rectangle((290, 260, 1308, 702), radius=24, fill=SURFACE)
    draw_text(draw, (330, 308), "LOCAL PROCESSING BOUNDARY", size=18, fill=MINT_DARK, mono=True)
    pill(
        draw,
        (1064, 286, 1266, 334),
        "桌面端本机处理",
        fill="#E9FBF5",
        text_fill=MINT_DARK,
    )

    # Inputs.
    draw_text(draw, (96, 374), "输入", size=20, fill=MUTED, bold=True)
    pill(draw, (70, 410, 230, 466), "本地照片", fill=WHITE, text_fill=INK, outline=HAIRLINE)
    pill(draw, (70, 490, 230, 546), "相册下载", fill=WHITE, text_fill=INK, outline=HAIRLINE)
    arrow(draw, (230, 438), (310, 438), fill=MINT_DARK, width=5)
    arrow(draw, (230, 518), (310, 518), fill=MINT_DARK, width=5)

    # Local processing stages.
    boxes = [
        (330, 382, 536, 520),
        (565, 382, 771, 520),
        (800, 382, 1006, 520),
        (1035, 382, 1241, 520),
    ]
    labels = [
        ("01", "解码与色彩", "JPG / RAW / ICC"),
        ("02", "图像分析", "场景 / 人脸 / 蒙版"),
        ("03", "参数工作栈", "可回退 · 可同步"),
        ("04", "统一渲染", "预览 / 最终导出"),
    ]
    for i, (box, label) in enumerate(zip(boxes, labels)):
        stage(draw, box, *label, active=i == 2)
        if i < len(boxes) - 1:
            arrow(
                draw,
                (box[2] + 7, (box[1] + box[3]) // 2),
                (boxes[i + 1][0] - 8, (boxes[i + 1][1] + boxes[i + 1][3]) // 2),
                fill=MINT_DARK,
                width=4,
            )

    draw_text(
        draw,
        (330, 592),
        "原图 → 参数 → 像素输出",
        size=26,
        fill=INK,
        bold=True,
    )
    draw_text(
        draw,
        (330, 638),
        "AI 给出起点，人工调整仍走同一参数与渲染链。",
        size=21,
        fill=MUTED,
    )

    # Outputs.
    draw_text(draw, (1370, 374), "输出", size=20, fill=MUTED, bold=True, anchor="mm")
    pill(draw, (1352, 410, 1532, 466), "本地导出", fill=WHITE, text_fill=INK, outline=HAIRLINE)
    pill(draw, (1352, 490, 1532, 546), "可选回传", fill=WHITE, text_fill=INK, outline=HAIRLINE)
    arrow(draw, (1241, 438), (1342, 438), fill=MINT_DARK, width=5)
    arrow(draw, (1241, 518), (1342, 518), fill=MINT_DARK, width=5)

    # Narrow network lane: clearly optional and not mixed into the pixel path.
    draw_text(draw, (800, 758), "OPTIONAL NETWORK LANE", size=16, fill=MUTED, mono=True, anchor="mm")
    pill(
        draw,
        (445, 786, 730, 842),
        "授权校验（无图像载荷）",
        fill=WHITE,
        text_fill=MUTED,
        outline=HAIRLINE,
    )
    pill(
        draw,
        (870, 786, 1155, 842),
        "用户主动选择云空间同步",
        fill=WHITE,
        text_fill=MUTED,
        outline=HAIRLINE,
    )
    arrow(draw, (730, 814), (860, 814), fill=HAIRLINE, width=3, dashed=True)

    draw_text(draw, (96, 850), "实线：本机精修主链路", size=16, fill=MINT_DARK)
    draw_text(draw, (300, 850), "虚线：可选网络行为", size=16, fill=MUTED)

    save(canvas, "local-first-architecture")


def paste_cover(
    canvas: Image.Image,
    image: Image.Image,
    box: tuple[int, int, int, int],
    *,
    radius: int,
    shadow: bool = False,
) -> None:
    x0, y0, x1, y1 = box
    size = (x1 - x0, y1 - y0)
    fitted = ImageOps.fit(
        image.convert("RGB"),
        size,
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )
    mask = rounded_mask(size, radius)
    if shadow:
        shadow_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        shadow_shape = rounded_mask(size, radius).filter(ImageFilter.GaussianBlur(18))
        shadow_layer.paste((0, 0, 0, 30), (x0, y0 + 14), shadow_shape)
        canvas.alpha_composite(shadow_layer)
    canvas.paste(fitted, (x0, y0), mask)


def diagram_node(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    eyebrow: str,
    title: str,
    subtitle: str,
    *,
    active: bool = False,
    accent: str = MINT_DARK,
) -> None:
    fill = "#E9FBF5" if active else WHITE
    outline = MINT if active else HAIRLINE
    draw.rounded_rectangle(box, radius=18, fill=fill, outline=outline, width=3 if active else 2)
    draw_text(draw, (box[0] + 24, box[1] + 24), eyebrow, size=16, fill=accent, mono=True)
    draw_text(draw, (box[0] + 24, box[1] + 58), title, size=25, fill=INK, bold=True)
    draw_text(draw, (box[0] + 24, box[1] + 99), subtitle, size=17, fill=MUTED)


def render_editable_ai() -> None:
    canvas = Image.new("RGBA", (W, H), WHITE)
    draw = ImageDraw.Draw(canvas)

    draw_text(draw, (96, 76), "AI 给起点，参数仍归你。", size=62, fill=INK, bold=True)
    draw_text(draw, (98, 158), "AI proposes. You decide.", size=24, fill=MINT_DARK, mono=True)
    draw_text(
        draw,
        (98, 203),
        "分析只负责提出建议；曝光、白平衡、HSL、曲线与风格强度继续可见、可改、可撤销。",
        size=23,
        fill=MUTED,
    )

    diagram_node(
        draw,
        (96, 320, 320, 474),
        "01  ANALYZE",
        "图像分析",
        "场景 · 人脸 · 光影",
    )
    diagram_node(
        draw,
        (362, 320, 586, 474),
        "02  PROPOSE",
        "参数建议",
        "给出可解释起点",
        active=True,
    )
    arrow(draw, (320, 397), (350, 397), fill=MINT_DARK, width=4)
    arrow(draw, (586, 397), (626, 397), fill=MINT_DARK, width=4)

    stack_box = (638, 270, 1082, 648)
    draw.rounded_rectangle(stack_box, radius=24, fill=SURFACE)
    draw_text(draw, (674, 310), "EDITABLE PARAMETER STACK", size=17, fill=MINT_DARK, mono=True)
    draw_text(draw, (674, 355), "可编辑参数工作栈", size=30, fill=INK, bold=True)

    sliders = [
        ("曝光", 0.63),
        ("白平衡", 0.48),
        ("HSL", 0.72),
        ("曲线", 0.57),
        ("风格强度", 0.38),
    ]
    for index, (label, value) in enumerate(sliders):
        y = 420 + index * 42
        draw_text(draw, (674, y), label, size=18, fill=MUTED, anchor="lm")
        draw.line((806, y, 1034, y), fill=HAIRLINE, width=5)
        knob_x = int(806 + (1034 - 806) * value)
        draw.line((806, y, knob_x, y), fill=MINT_DARK, width=5)
        draw.ellipse((knob_x - 8, y - 8, knob_x + 8, y + 8), fill=WHITE, outline=MINT_DARK, width=3)

    pill(
        draw,
        (672, 592, 1038, 634),
        "撤销 · 复制 · 批量同步",
        fill=WHITE,
        text_fill=INK,
        outline=HAIRLINE,
    )

    # Human decisions enter the same visible stack instead of a hidden second path.
    pill(
        draw,
        (1200, 120, 1484, 164),
        "用户继续调整",
        fill=WHITE,
        text_fill=INK,
        outline=MINT,
    )
    arrow(draw, (1200, 142), (1074, 282), fill=MINT_DARK, width=4)

    renderer_box = (1142, 320, 1392, 474)
    diagram_node(
        draw,
        renderer_box,
        "03  RENDER",
        "同一渲染器",
        "同一套参数逻辑",
    )
    arrow(draw, (1082, 397), (1130, 397), fill=MINT_DARK, width=4)

    pill(
        draw,
        (1434, 320, 1540, 376),
        "预览",
        fill="#E9FBF5",
        text_fill=MINT_DARK,
        outline=MINT,
    )
    pill(
        draw,
        (1434, 418, 1540, 474),
        "导出",
        fill=WHITE,
        text_fill=INK,
        outline=HAIRLINE,
    )
    arrow(draw, (1392, 365), (1422, 348), fill=MINT_DARK, width=4)
    arrow(draw, (1392, 430), (1422, 446), fill=MINT_DARK, width=4)

    draw.line((96, 734, 1504, 734), fill=HAIRLINE, width=2)
    footer = [
        ("原图", "不被覆盖"),
        ("AI 建议", "不是烤死像素"),
        ("人工调整", "全程保留控制权"),
        ("预览 / 导出", "共享参数与渲染逻辑"),
    ]
    for x, (title, subtitle) in zip([98, 458, 818, 1178], footer):
        draw_text(draw, (x, 778), title, size=24, fill=INK, bold=True)
        draw_text(draw, (x, 818), subtitle, size=18, fill=MUTED)

    save(canvas, "editable-ai-pipeline")


def render_multi_model() -> None:
    canvas = Image.new("RGBA", (W, H), WHITE)
    draw = ImageDraw.Draw(canvas)

    draw_text(draw, (96, 76), "多模型协同，不是一个黑盒滤镜。", size=58, fill=INK, bold=True)
    draw_text(
        draw,
        (98, 158),
        "人脸、区域、蒙版与全局色彩各司其职；结果汇入同一个可编辑工作栈。",
        size=24,
        fill=MUTED,
    )

    input_box = (70, 328, 272, 514)
    diagram_node(draw, input_box, "INPUT", "一张照片", "原图保持不变")

    analysis_group = (306, 204, 968, 612)
    draw.rounded_rectangle(analysis_group, radius=26, fill=SURFACE)
    draw_text(draw, (336, 229), "PARALLEL VISUAL ANALYSIS", size=15, fill=MUTED, mono=True)

    model_boxes = [
        ((342, 252, 610, 388), "01  FACE", "人脸检测", "位置 · 类别 · 单人作用域", MINT_DARK),
        ((342, 430, 610, 566), "02  PORTRAIT", "人像区域", "皮肤 · 五官 · 身体区域", MINT_DARK),
        ((668, 252, 936, 388), "03  MASK", "场景蒙版", "主体 · 背景 · 天空", "#2D8DA0"),
        ((668, 430, 936, 566), "04  COLOR", "全局色彩", "影调 · 白平衡 · 色彩", "#2D8DA0"),
    ]
    for box, eyebrow, title, subtitle, accent in model_boxes:
        diagram_node(draw, box, eyebrow, title, subtitle, accent=accent)

    arrow(draw, (272, 421), (294, 421), fill=HAIRLINE, width=3, dashed=True)

    orchestration = (1004, 290, 1278, 528)
    draw.rounded_rectangle(orchestration, radius=22, fill="#E9FBF5", outline=MINT, width=3)
    draw_text(draw, (1040, 328), "ORCHESTRATION", size=16, fill=MINT_DARK, mono=True)
    draw_text(draw, (1040, 374), "任务路由与", size=29, fill=INK, bold=True)
    draw_text(draw, (1040, 414), "参数融合", size=29, fill=INK, bold=True)
    draw_text(draw, (1040, 468), "全局层 + 局部层", size=18, fill=MUTED)

    arrow(draw, (968, 409), (992, 409), fill=MINT_DARK, width=4)

    output_box = (1344, 328, 1544, 514)
    diagram_node(draw, output_box, "OUTPUT", "统一合成", "可预览 · 可撤销")
    arrow(draw, (1278, 409), (1332, 409), fill=MINT_DARK, width=4)

    draw.rounded_rectangle((96, 668, 1504, 806), radius=22, fill=SURFACE)
    draw_text(draw, (132, 707), "边界说明", size=18, fill=MINT_DARK, mono=True)
    draw_text(
        draw,
        (132, 750),
        "这张图只解释模块关系，不公开模型结构、权重、风格配方或核心算法。",
        size=25,
        fill=INK,
        bold=True,
    )
    draw_text(
        draw,
        (132, 786),
        "模型输出先变成参数与区域，再进入产品工作栈；用户仍可逐项调整。",
        size=19,
        fill=MUTED,
    )

    save(canvas, "multi-model-orchestration")


def render_open_core() -> None:
    height = 820
    canvas = Image.new("RGBA", (W, height), WHITE)
    draw = ImageDraw.Draw(canvas)

    draw_text(draw, (96, 70), "开放通用零件，守住产品核心。", size=58, fill=INK, bold=True)
    draw_text(
        draw,
        (98, 150),
        "Open Core 在这里首先是一条清晰边界：能运行的标准组件公开，正式引擎与模型商业授权。",
        size=23,
        fill=MUTED,
    )

    columns = [
        (
            (70, 248, 550, 650),
            "MIT",
            "开源零件",
            [
                ("liangzai-cube-kit", ".cube 读写 · 三线性插值"),
                ("liangzai-plugin-sdk", "类型与 Hello 示例"),
                ("可独立运行", "npm / playground / demo host"),
            ],
            "#E9FBF5",
            MINT,
            MINT_DARK,
        ),
        (
            (580, 248, 1020, 650),
            "CC BY 4.0",
            "产品技术总览",
            [
                ("liangzai", "本仓库不是完整产品源码"),
                ("README / 技术图", "产品说明与开源导航"),
                ("透明边界", "公开什么，也说明不公开什么"),
            ],
            SURFACE,
            HAIRLINE,
            MUTED,
        ),
        (
            (1050, 248, 1530, 650),
            "COMMERCIAL",
            "正式产品核心",
            [
                ("桌面工作台", "Mac / Windows 正式应用"),
                ("引擎与模型", "人像 · 蒙版 · 色彩 · 渲染"),
                ("企业合作", "私有化 / OEM / NDA 后审计"),
            ],
            "#F3F6F7",
            "#BFC8CD",
            "#58666D",
        ),
    ]

    for box, license_name, title, rows, fill, outline, accent in columns:
        draw.rounded_rectangle(box, radius=24, fill=fill, outline=outline, width=3 if outline == MINT else 2)
        draw_text(draw, (box[0] + 30, box[1] + 32), license_name, size=17, fill=accent, mono=True)
        draw_text(draw, (box[0] + 30, box[1] + 78), title, size=31, fill=INK, bold=True)
        y = box[1] + 150
        for row_title, row_subtitle in rows:
            draw.line((box[0] + 30, y - 17, box[2] - 30, y - 17), fill=HAIRLINE, width=2)
            draw_text(draw, (box[0] + 30, y + 8), row_title, size=21, fill=INK, bold=True)
            draw_text(draw, (box[0] + 30, y + 45), row_subtitle, size=17, fill=MUTED)
            y += 88

    arrow(draw, (550, 449), (568, 449), fill=HAIRLINE, width=3, dashed=True)
    arrow(draw, (1020, 449), (1038, 449), fill=HAIRLINE, width=3, dashed=True)

    draw_text(
        draw,
        (96, 715),
        "开源仓均可独立验证；plugin-sdk 当前不是正式 App 的第三方插件入口。",
        size=21,
        fill=INK,
        bold=True,
    )
    draw_text(
        draw,
        (96, 758),
        "github.com/18818474455/liangzai-cube-kit   ·   github.com/18818474455/liangzai-plugin-sdk",
        size=17,
        fill=MINT_DARK,
        mono=True,
    )

    save(canvas, "open-core-map")


def render_proof_pair(
    stem: str,
    title: str,
    subtitle: str,
    left_name: str,
    left_label: str,
    right_name: str,
    right_label: str,
) -> None:
    canvas = Image.new("RGBA", (W, H), WHITE)
    draw = ImageDraw.Draw(canvas)

    draw_text(draw, (96, 76), title, size=58, fill=INK, bold=True)
    draw_text(draw, (98, 158), subtitle, size=23, fill=MUTED)

    left_box = (70, 242, 784, 688)
    right_box = (816, 242, 1530, 688)
    paste_cover(canvas, Image.open(ASSETS / left_name), left_box, radius=20, shadow=True)
    paste_cover(canvas, Image.open(ASSETS / right_name), right_box, radius=20, shadow=True)

    draw_text(draw, (70, 746), left_label, size=27, fill=INK, bold=True)
    draw_text(draw, (816, 746), right_label, size=27, fill=INK, bold=True)
    draw_text(draw, (70, 793), "真实界面实拍", size=17, fill=MINT_DARK, mono=True)
    draw_text(draw, (816, 793), "真实界面实拍", size=17, fill=MINT_DARK, mono=True)

    save(canvas, stem, png=False)


def render_product_proofs() -> None:
    render_proof_pair(
        "portrait-proof",
        "合影不必一刀切。",
        "人像精修与多人脸作用域在同一个工作台完成。",
        "shot-beauty.png",
        "人像精修 · 参数继续可调",
        "shot-faces.png",
        "多人脸识别 · 按人作用",
    )
    render_proof_pair(
        "mask-proof",
        "局部区域，独立控制。",
        "主体、背景与颜色范围可以形成多层局部参数。",
        "shot-mask-subject.png",
        "主体蒙版 · 可继续细修",
        "shot-multimask.png",
        "多层蒙版 · 参数互不覆盖",
    )
    render_proof_pair(
        "image-tools-proof",
        "从证件照到现场外景。",
        "抠图、换底与换天空都留在统一的精修流程里。",
        "shot-idred.png",
        "证件照换底 · 羽化与透明度可调",
        "shot-sky.png",
        "智能换天空 · 强度可调",
    )


def render_video_poster() -> None:
    source = MEDIA / "product-tour-frame.jpg"
    if not source.exists():
        return

    canvas = Image.new("RGBA", (W, H), "#050607")
    frame = ImageOps.fit(
        Image.open(source).convert("RGB"),
        (W, H),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )
    canvas.paste(frame, (0, 0))

    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle((0, 0, W, H), fill=(5, 6, 7, 52))
    overlay_draw.rectangle((0, 590, W, H), fill=(5, 6, 7, 206))
    canvas.alpha_composite(overlay)
    draw = ImageDraw.Draw(canvas)

    # Play control is intentionally simple and reads at mobile width.
    draw.ellipse((700, 300, 900, 500), fill=(255, 255, 255, 238))
    draw.polygon([(782, 350), (782, 450), (864, 400)], fill=MINT_DARK)

    pill(
        draw,
        (96, 624, 286, 672),
        "完整实机录屏",
        fill=MINT,
        text_fill="#06241B",
    )
    draw_text(draw, (96, 724), "四分钟，看完整精修过程。", size=43, fill=WHITE, bold=True)
    draw_text(
        draw,
        (98, 786),
        "真实软件界面 · H.264 720p · 04:11 · 点击观看",
        size=22,
        fill="#D7DEE2",
    )
    save(canvas, "product-tour-poster", png=False)


def render_social_preview() -> None:
    width, height = 1280, 640
    canvas = Image.new("RGBA", (width, height), WHITE)
    draw = ImageDraw.Draw(canvas)

    icon = Image.open(ASSETS / "pc-icon.png").convert("RGBA").resize((36, 36), Image.Resampling.LANCZOS)
    canvas.alpha_composite(icon, (62, 60))
    draw_text(draw, (112, 78), "云享传靓仔", size=23, fill=INK, bold=True, anchor="lm")
    draw_text(draw, (64, 176), "本机出片。", size=57, fill=INK, bold=True)
    draw_text(draw, (64, 252), "AI 起稿，参数可编辑。", size=38, fill=INK, bold=True)
    draw_text(draw, (66, 326), "活动摄影精修工作台", size=21, fill=MUTED)
    draw_text(draw, (66, 370), "LOCAL-FIRST  ·  EDITABLE AI  ·  OPEN CORE", size=16, fill=MINT_DARK, mono=True)

    screenshot = Image.open(ASSETS / "shot-color.png")
    paste_rounded(canvas, screenshot, (588, 108, 1230, 510), radius=18, shadow=True)

    draw.line((64, 552, 1216, 552), fill=HAIRLINE, width=2)
    draw_text(draw, (64, 590), "liangzai-cube-kit", size=18, fill=INK, bold=True)
    draw_text(draw, (320, 590), "liangzai-plugin-sdk", size=18, fill=INK, bold=True)
    draw_text(draw, (1216, 590), "ybpbyxc.com", size=17, fill=MUTED, mono=True, anchor="rm")

    OUT.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUT / "social-preview.png", optimize=True)


if __name__ == "__main__":
    render_hero()
    render_local_first()
    render_editable_ai()
    render_multi_model()
    render_open_core()
    render_product_proofs()
    render_video_poster()
    render_social_preview()
    for path in sorted(OUT.glob("*")):
        if path.is_file():
            print(path)
