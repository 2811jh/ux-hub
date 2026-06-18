"""ux-hub 统一输出格式模块。"""
from datetime import datetime

CARD_FIELDS = ["需求名称", "需求描述", "需求来源", "指派人"]
CARD_DEFAULTS = {"需求来源": "UX和策划合议需求", "指派人": ""}


def render_cards_markdown(cards: list[dict]) -> str:
    """渲染需求卡片 Markdown。"""
    lines = [
        "# 需求卡片",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
    ]

    for i, card in enumerate(cards, start=1):
        lines.append(f"## 需求 {i}")
        lines.append(f"- **需求名称**：{card.get('title', '')}")
        lines.append(f"- **需求描述**：{card.get('description', '')}")
        lines.append(f"- **需求来源**：{CARD_DEFAULTS['需求来源']}")
        lines.append(f"- **指派人**：{CARD_DEFAULTS['指派人']}")
        lines.append("")

    return "\n".join(lines)
