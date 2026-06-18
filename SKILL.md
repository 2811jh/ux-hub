---
name: ux-hub
description: |
  用户研究项目管理工具集。
  当用户说"整理需求"、"生成需求卡片"、"项目管理"、"需求梳理"、
  "调研管理"、"用研工具"等类似表达时触发此 skill。
  即使用户没有明确说工具名，只要涉及用研项目管理的场景也应触发。
---

# UX Hub — 用户研究项目管理工具集

你是用户研究项目管理的专家，提供一系列用研项目管理工具。

## 子能力列表

| 子 skill | 路径 | 状态 | 功能 |
|----------|------|------|------|
| demand-cards | `references/demand-cards/` | ✅ 已上线 | 散乱文本 → 结构化需求卡片 |
| card-manager | `references/card-manager/` | 🔲 预留 | 卡片增删改、合并、去重 |
| report-tpl | `references/report-tpl/` | 🔲 预留 | 满意度报告模板生成 |
| schedule | `references/schedule/` | 🔲 预留 | 项目排期/时间线管理 |
| data-hub | `references/data-hub/` | 🔲 预留 | 问卷数据/分析结果关联 |

## 使用方式

触发本 skill 后，根据用户意图路由到对应子能力。各子 skill 的 `SKILL.md` 中有详细的使用说明。

### 示例

```
用户："帮我把这段需求整理成卡片"
→ 路由到 demand-cards，按 demand-cards/SKILL.md 规范执行
```

## 共享模块

主 `scripts/` 目录下包含所有子 skill 共享的工具模块：

- `scripts/_shared/utils.py` — 文本预处理、条目切分
- `scripts/_shared/format.py` — 统一输出格式渲染

子 skill 的脚本引用共享模块：
```python
import sys
sys.path.insert(0, str(ROOT_DIR / "scripts"))
from _shared.utils import preprocess_text, split_requirements
from _shared.format import render_cards_markdown
```

## 目录结构

```text
ux-hub/
├─ SKILL.md                          # 本文件（主入口）
├─ requirements.txt
├─ scripts/
│  ├─ _shared/
│  │  ├─ __init__.py
│  │  ├─ utils.py                    # 公共文本处理
│  │  └─ format.py                   # 统一输出格式
│  └─ ux_hub.py                      # 主调度脚本（预留）
├─ references/
│  ├─ demand-cards/                  # ✅ 需求卡片整理
│  │  ├─ SKILL.md
│  │  ├─ card_template.md
│  │  ├─ sample_input_output.md
│  │  └─ scripts/
│  │     └─ build_cards.py
│  ├─ card-manager/                  # 🔲 预留
│  ├─ report-tpl/                    # 🔲 预留
│  ├─ schedule/                      # 🔲 预留
│  └─ data-hub/                      # 🔲 预留
└─ output/                           # 统一输出目录
```

## 扩展新子能力

1. 在 `references/` 下创建子目录，放入 `SKILL.md` 和 `scripts/`
2. 更新本文件子能力列表，标注状态
3. 如需共享逻辑，抽取到 `scripts/_shared/`
4. 子 skill 独立触发，也可被 ux-hub 主 skill 路由调度
