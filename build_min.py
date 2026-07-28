#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Peroxide 压缩构建脚本
将 CSS/ 下的 5 个核心源文件合并并压缩为 peroxide.min.css。

特性：
- 按与原 build.bat 相同的顺序拼接（Variables -> Base -> Elements -> Capabilities -> Localization）
- 删除 /* */ 注释、压缩空白与无意义空格
- 用「单遍扫描」把字符串、url() 以及 calc/min/max/clamp/color-mix/var/rgb/... 等
  函数内部文本整体保护，避免破坏 calc(100% - 2rem)、color-mix(in srgb, ...) 等必需空格
- 纯标准库实现，无任何第三方依赖

用法：
    python build_min.py [输出路径]
默认输出到脚本所在目录的 peroxide.min.css
"""

import os
import re
import sys

# 拼接顺序（与原 build.bat 保持一致）
SOURCE_FILES = ["Variables", "Base", "Elements", "Capabilities", "Localization"]

# 这些函数括号内的空格具有语法意义，必须整体保护
PROTECTED_FUNCS = (
    "calc", "min", "max", "clamp", "color-mix",
    "rgb", "rgba", "hsl", "hsla", "hwb",
    "lab", "lch", "oklab", "oklch", "var", "url",
)

NULL = "\x00"  # 占位符分隔符，不会出现在正常 CSS 中


def minify(css):
    """单遍扫描：将受保护片段（字符串 / 受保护函数）整体抽离为占位符，
    其余文本做激进压缩。"""
    protected = []
    out = []          # 交替存放：普通文本片段 与 占位符
    buf = []
    i = 0
    n = len(css)

    def flush():
        out.append("".join(buf))
        buf.clear()

    def emit_placeholder():
        flush()
        out.append(NULL + str(len(protected) - 1) + NULL)

    while i < n:
        c = css[i]

        # 1) 字符串字面量（支持转义）
        if c in ('"', "'"):
            flush()
            q = c
            seg = [c]
            j = i + 1
            while j < n:
                seg.append(css[j])
                if css[j] == "\\":
                    j += 1
                    if j < n:
                        seg.append(css[j])
                elif css[j] == q:
                    j += 1
                    break
                j += 1
            protected.append("".join(seg))
            emit_placeholder()
            i = j
            continue

        # 2) 注释
        if c == "/" and i + 1 < n and css[i + 1] == "*":
            flush()
            k = css.find("*/", i + 2)
            i = n if k == -1 else k + 2
            continue

        # 3) 受保护函数：关键字后紧跟 '('，且关键字前为词边界
        matched = None
        for f in PROTECTED_FUNCS:
            if css[i:i + len(f)] == f and i + len(f) < n and css[i + len(f)] == "(":
                prev = css[i - 1] if i > 0 else ""
                if prev == "" or not (prev.isalnum() or prev == "_"):
                    matched = f
                break
        if matched:
            flush()
            depth = 0
            j = i + len(matched)          # '(' 的位置
            seg_start = i
            while j < n:
                ch = css[j]
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
                j += 1
            protected.append(css[seg_start:j])
            emit_placeholder()
            i = j
            continue

        buf.append(c)
        i += 1

    flush()

    # 压缩普通文本片段（占位符不含空白，不会被误伤）
    text = "".join(out)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s*([{};,>~+])\s*", r"\1", text)
    text = re.sub(r"\s*\(\s*", "(", text)
    text = re.sub(r"\s*\)\s*", ")", text)
    text = re.sub(r":\s+", ":", text)
    text = re.sub(r";}", "}", text)
    text = text.strip()

    # 还原占位符（循环处理嵌套占位，如 url(\x000\x00)）
    pat = re.compile(re.escape(NULL) + r"(\d+)" + re.escape(NULL))
    prev = None
    while text != prev:
        prev = text
        text = pat.sub(lambda m: protected[int(m.group(1))], text)

    return text


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    css_dir = os.path.join(script_dir, "CSS")
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(script_dir, "peroxide.min.css")

    parts = []
    for name in SOURCE_FILES:
        fpath = os.path.join(css_dir, name + ".css")
        if not os.path.isfile(fpath):
            sys.exit("找不到源文件: " + fpath)
        with open(fpath, "r", encoding="utf-8") as fh:
            parts.append(fh.read())

    raw = "\n".join(parts)
    minified = minify(raw)

    header = (
        "/* Peroxide base theme (minified) | CC-BY-SA 4.0 | "
        "built from CSS/{}.css */\n".format(",".join(SOURCE_FILES))
    )
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(header + minified)

    raw_size = len(raw.encode("utf-8"))
    out_size = len(header.encode("utf-8")) + len(minified.encode("utf-8"))
    ratio = (1 - out_size / raw_size) * 100 if raw_size else 0
    print("构建完成: {}".format(out_path))
    print("原始合计: {:,} bytes -> 压缩后: {:,} bytes (节省 {:.1f}%)".format(raw_size, out_size, ratio))


if __name__ == "__main__":
    main()
