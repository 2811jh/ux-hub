---
name: demand-cards
description: |
  将散乱不固定的项目需求文本整理为结构化 Markdown 需求卡片。
  当用户说"整理需求"、"生成需求卡片"、"把这些需求整理成卡片"、
  "需求梳理"、"帮我整理这些项目"等类似表达时触发。
---

# Demand Cards — 需求卡片整理

将散乱需求文本整理为统一格式的需求卡片。

## 脚本路径

```
{SKILL_DIR}/scripts/build_cards.py
```

其中 `{SKILL_DIR}` 是本 skill 所在目录的绝对路径。

## 使用方式

```bash
python {SKILL_DIR}/scripts/build_cards.py --file input.txt
python {SKILL_DIR}/scripts/build_cards.py --input "散乱文本"
python {SKILL_DIR}/scripts/build_cards.py --file input.txt --output requirements_cards.md
```

## 输出格式（强制）

```md
## 需求 {序号}
- **需求名称**：{提炼后的项目名称}
- **需求描述**：{整理后的结构化描述}
- **需求来源**：UX和策划合议需求
- **指派人**：
```

## 整理规则

1. 保留原始含义，不凭空添加
2. 去除噪声编号（`7——7.`、`8.——8.`）
3. 提炼准确名称，统一大小写和格式
4. 描述聚焦调研目标、关注重点、输出物，1～3句
5. 逐条处理，按输入顺序编号

## 职责边界

脚本仅做切分+格式框架。AI 必须亲自完成语义整理，输出以 AI 整理结果为准。
