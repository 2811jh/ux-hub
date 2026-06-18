"""
demand-cards build_cards.py
将散乱需求文本整理为结构化 Markdown 需求卡片。
"""

import argparse
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = SKILL_DIR.parent.parent

sys.path.insert(0, str(ROOT_DIR / "scripts"))

from _shared.utils import preprocess_text, split_requirements, normalize_title
from _shared.format import render_cards_markdown


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


def build_description(block: str) -> str:
    import re
    cleaned = re.sub(r"^\s*\d+[\.\。]", "", block).strip()
    return cleaned


def refine_card(block: str) -> dict:
    return {"title": normalize_title(block), "description": build_description(block)}


def save_output(markdown: str, output_path: str):
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(markdown, encoding="utf-8")
    count = len([s for s in markdown.splitlines() if s.startswith("## 需求")])
    print(f"✅ 已生成 {count} 条需求卡片 → {out.resolve()}")


def main():
    args = parse_args()
    raw_text = load_input(args)
    clean_text = preprocess_text(raw_text)
    blocks = split_requirements(clean_text)

    if not blocks:
        print("⚠️ 未识别到需求条目，请检查输入格式。", file=sys.stderr)
        sys.exit(1)

    cards = [refine_card(block) for block in blocks]
    markdown = render_cards_markdown(cards)

    output_path = args.output or "requirements_cards.md"
    save_output(markdown, output_path)


if __name__ == "__main__":
    main()
