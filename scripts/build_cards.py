"""
ux-hub build_cards.py
将散乱需求文本整理为结构化 Markdown 需求卡片。
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = SKILL_DIR / "templates"


def parse_args():
    parser = argparse.ArgumentParser(description="整理散乱需求文本为需求卡片")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input", type=str, help="直接输入散乱文本")
    group.add_argument("--file", type=str, help="从文本文件读取")
    parser.add_argument("--output", type=str, default=None, help="输出文件路径")
    return parser.parse_args()


def load_input(args) -> str:
    if args.input:
        return args.input.strip()
    filepath = Path(args.file)
    if not filepath.exists():
        raise FileNotFoundError(f"文件不存在: {filepath}")
    return filepath.read_text(encoding="utf-8").strip()


def preprocess_text(text: str) -> str:
    """预处理：统一换行、清理重复编号噪声。"""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # 清理形如 "7——7." 的重复编号
    text = re.sub(r"(\d+)[——\-—.]+(\1)[\.\。]?", r"\1.", text)
    # 清理 "8.——8." 形式
    text = re.sub(r"(\d+)\.[——\-—]+(\d+)[\.\。]?", r"\1.", text)
    return text.strip()


def split_requirements(text: str) -> list[str]:
    """按编号切分需求条目。"""
    # 匹配 "数字." 或 "数字。" 开头的段落
    pattern = re.compile(r"(?:^|\n)\s*(\d+)[\.\。]", re.MULTILINE)
    matches = list(pattern.finditer(text))

    if not matches:
        # 无编号，整段作为一条
        return [text.strip()] if text.strip() else []

    blocks = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end].strip()
        if block:
            blocks.append(block)

    return blocks


def normalize_title(block: str) -> str:
    """从需求块中提炼需求名称。"""
    # 去除开头编号
    cleaned = re.sub(r"^\s*\d+[\.\。]", "", block).strip()
    # 取第一句话或破折号/冒号前的部分作为标题核心
    # 优先按结束标点截断
    title_match = re.match(r"^(.+?)[。：:\-—]", cleaned)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = cleaned.strip()

    # 清理残留噪声
    title = re.sub(r"^\s*——\s*", "", title)
    title = title.strip()

    return title if title else "未命名需求"


def build_description(block: str) -> str:
    """从需求块中整理需求描述。"""
    # 去除开头编号
    cleaned = re.sub(r"^\s*\d+[\.\。]", "", block).strip()
    return cleaned


def refine_card(block: str) -> dict:
    """汇集整理后的单条卡片数据。"""
    title = normalize_title(block)
    description = build_description(block)
    return {"title": title, "description": description}


def render_markdown(cards: list[dict]) -> str:
    """渲染 Markdown 文档。"""
    lines = [
        "# 需求卡片",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
    ]

    for i, card in enumerate(cards, start=1):
        lines.append(f"## 需求 {i}")
        lines.append(f"- **需求名称**：{card['title']}")
        lines.append(f"- **需求描述**：{card['description']}")
        lines.append("")

    return "\n".join(lines)


def save_output(markdown: str, output_path: str):
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(markdown, encoding="utf-8")
    print(f"✅ 已生成 {len(list(filter(lambda s: s.startswith('## 需求'), markdown.splitlines())))} 条需求卡片 → {out.resolve()}")


def main():
    args = parse_args()
    raw_text = load_input(args)
    clean_text = preprocess_text(raw_text)
    blocks = split_requirements(clean_text)

    if not blocks:
        print("⚠️ 未识别到需求条目，请检查输入格式。", file=sys.stderr)
        sys.exit(1)

    cards = [refine_card(block) for block in blocks]
    markdown = render_markdown(cards)

    output_path = args.output or "requirements_cards.md"
    save_output(markdown, output_path)


if __name__ == "__main__":
    main()
