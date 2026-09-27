#!/usr/bin/env python3
"""
生成 Hello-Tauri-Log-Parase 应用图标。

设计：现代渐变圆角方块（靛蓝→紫→青） + 白色日志卡片（若干长短不一的日志行）
      + 放大镜（检视/解析日志），体现「日志解析」业务功能。

输出：
  src-tauri/icons/icon.ico   多分辨率 Windows 图标（exe 嵌入用）
  src-tauri/icons/icon.png   512px PNG（备用）
  src-tauri/icons/icon.svg   矢量源文件（便于后续手工微调）

依赖：Pillow（仅标准库之外）。运行：python scripts/gen-icon.py
"""
import math
import os
from PIL import Image, ImageDraw

S = 512  # 矢量画布基准尺寸


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# 三段对角渐变：靛蓝 -> 紫 -> 青
C1 = (79, 70, 229)    # #4F46E5 靛蓝
C2 = (139, 92, 246)   # #8B5CF6 紫
C3 = (6, 182, 212)    # #06B6D4 青


def build_raster():
    # 1) 对角渐变底
    base = Image.new("RGBA", (S, S))
    px = []
    for y in range(S):
        for x in range(S):
            t = (x + y) / (2 * S)
            col = lerp(C1, C2, t / 0.5) if t < 0.5 else lerp(C2, C3, (t - 0.5) / 0.5)
            px.append(col + (255,))
    base.putdata(px)

    # 2) 圆角遮罩（裁掉四角）
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=255)
    base.putalpha(mask)

    # 3) 顶部高光（轻微内发光，增强立体感）
    hi = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(hi).rounded_rectangle(
        [int(S * 0.04), int(S * 0.02), int(S * 0.96), int(S * 0.5)],
        radius=int(S * 0.2), fill=(255, 255, 255, 38),
    )
    base = Image.alpha_composite(base, hi)

    d = ImageDraw.Draw(base)

    # 4) 白色日志卡片
    card = [int(S * 0.20), int(S * 0.16), int(S * 0.80), int(S * 0.84)]
    d.rounded_rectangle(card, radius=int(S * 0.06), fill=(255, 255, 255, 238))

    # 5) 卡片上的日志行（长短不一，模拟日志条目）
    line_color = C1 + (225,)
    lx = card[0] + int(S * 0.07)
    ly = card[1] + int(S * 0.12)
    inner_w = (card[2] - card[0]) - int(S * 0.14)
    lengths = [0.95, 0.72, 1.0, 0.6, 0.85]
    for i, frac in enumerate(lengths):
        yy = ly + i * int(S * 0.115)
        w = int(inner_w * frac)
        d.rounded_rectangle([lx, yy, lx + w, yy + int(S * 0.032)], radius=int(S * 0.016), fill=line_color)

    # 6) 放大镜（检视/解析日志）
    # 使用主色 C1（靛蓝）以在白色日志卡片上保持高对比度；镜面做轻微白色雾化。
    cx, cy = int(S * 0.685), int(S * 0.70)
    R = int(S * 0.135)
    ring = int(S * 0.028)
    # 镜环
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=C1 + (245,), width=ring)
    # 磨砂玻璃镜面（白色不透明但柔和，不透视背景）
    d.ellipse([cx - R + ring, cy - R + ring, cx + R - ring, cy + R - ring],
              fill=(255, 255, 255, 200))
    # 手柄（右下 45°）
    ang = math.radians(45)
    hx0, hy0 = cx + R * math.cos(ang), cy + R * math.sin(ang)
    L = int(S * 0.13)
    hx1, hy1 = cx + (R + L) * math.cos(ang), cy + (R + L) * math.sin(ang)
    d.line([(hx0, hy0), (hx1, hy1)], fill=C1 + (245,), width=int(S * 0.05), joint="curve")
    # 手柄圆头
    d.ellipse([hx1 - int(S * 0.03), hy1 - int(S * 0.03), hx1 + int(S * 0.03), hy1 + int(S * 0.03)],
              fill=C1 + (245,))

    return base


def write_svg(path):
    """矢量源：与栅格设计同构，便于手工微调。"""
    stops = (
        f'<stop offset="0%" stop-color="#{C1[0]:02x}{C1[1]:02x}{C1[2]:02x}"/>'
        f'<stop offset="50%" stop-color="#{C2[0]:02x}{C2[1]:02x}{C2[2]:02x}"/>'
        f'<stop offset="100%" stop-color="#{C3[0]:02x}{C3[1]:02x}{C3[2]:02x}"/>'
    )
    r = 112  # 圆角(512*0.22)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="512" y2="512" gradientUnits="userSpaceOnUse">
      {stops}
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="512" height="512" rx="{r}" ry="{r}" fill="url(#g)"/>
  <rect x="20" y="10" width="472" height="246" rx="102" ry="102" fill="#ffffff" opacity="0.15"/>
  <rect x="102" y="82" width="308" height="346" rx="31" ry="31" fill="#ffffff" opacity="0.93"/>
  <rect x="132" y="128" width="248" height="16" rx="8" ry="8" fill="#4F46E5" opacity="0.88"/>
  <rect x="132" y="171" width="188" height="16" rx="8" ry="8" fill="#4F46E5" opacity="0.88"/>
  <rect x="132" y="214" width="262" height="16" rx="8" ry="8" fill="#4F46E5" opacity="0.88"/>
  <rect x="132" y="257" width="156" height="16" rx="8" ry="8" fill="#4F46E5" opacity="0.88"/>
  <rect x="132" y="300" width="222" height="16" rx="8" ry="8" fill="#4F46E5" opacity="0.88"/>
  <circle cx="351" cy="358" r="69" fill="none" stroke="#4F46E5" stroke-width="14" opacity="0.96"/>
  <circle cx="351" cy="358" r="55" fill="#ffffff" opacity="0.78"/>
  <line x1="400" y1="407" x2="455" y2="462" stroke="#4F46E5" stroke-width="26" stroke-linecap="round" opacity="0.96"/>
</svg>
'''
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    icons = os.path.join(os.path.dirname(here), "src-tauri", "icons")
    os.makedirs(icons, exist_ok=True)

    img = build_raster()

    # 多分辨率 ICO（exe 嵌入）
    # 关键坑：Pillow 的 IcoImagePlugin._save 用【基准图(首帧)尺寸】过滤每个 size，
    # 若首帧不是最大尺寸，更大的帧会被 size>width 直接 continue 丢弃。
    # 因此必须把最大的 256 帧作为基准图，其余尺寸经 append_images 提供。
    sizes = [16, 24, 32, 48, 64, 128, 256]
    frames = {s: img.resize((s, s), Image.LANCZOS) for s in sizes}
    base = frames[256]                       # 基准图取最大尺寸
    others = [frames[s] for s in sizes if s != 256]
    base.save(
        os.path.join(icons, "icon.ico"),
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=others,
    )

    # 512 PNG 备用
    img.save(os.path.join(icons, "icon.png"), "PNG")

    # 矢量源
    write_svg(os.path.join(icons, "icon.svg"))

    print("icon.ico / icon.png / icon.svg 已生成于", icons)


if __name__ == "__main__":
    main()
