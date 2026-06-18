"""ux-hub 公共工具模块。"""

import re


def preprocess_text(text: str) -> str:
    """预处理：统一换行、清理重复编号噪声。"""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"(\d+)[——\-—.]+(\1)[\.\。]?", r"\1.", text)
    text = re.sub(r"(\d+)\.[——\-—]+(\d+)[\.\。]?", r"\1.", text)
    return text.strip()


def split_requirements(text: str) -> list[str]:
    """按编号切分需求条目。"""
    pattern = re.compile(r"(?:^|\n)\s*(\d+)[\.\。]", re.MULTILINE)
    matches = list(pattern.finditer(text))

    if not matches:
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
    cleaned = re.sub(r"^\s*\d+[\.\。]", "", block).strip()
    title_match = re.match(r"^(.+?)[。：:\-—]", cleaned)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = cleaned.strip()
    title = re.sub(r"^\s*——\s*", "", title)
    return title.strip() if title.strip() else "未命名需求"
