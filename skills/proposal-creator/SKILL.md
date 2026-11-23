---
name: proposal-creator
description: >-
  理工科科研项目申请书的五角色协作技能，支持 auto-pilot、co-write 及单角色调用。按资助要求与研究方法组织方案、证据、研究基础、配图和独立评审，适用于理论、实验、计算及工程项目。
---

# Proposal Creator

## 调用方式

| 调用示例 | 模式或职责 |
|---|---|
| `$proposal-creator` | auto-pilot 全自动或 co-write 共同写作 |
| `$proposal-creator writer` | [A 方案与正文](references/writer.md) |
| `$proposal-creator foundation` | [B 研究基础](references/foundation.md) |
| `$proposal-creator figure` | [C 配图与验收](references/figure.md) |
| `$proposal-creator evidence` | [D 外部依据](references/evidence.md) |
| `$proposal-creator reviewer` | [E 独立评审](references/reviewer.md) |

## 启动

1. 读取[共同规则](references/common.md)、[项目适配](references/project-adaptation.md)和[依赖路由](references/dependencies.md)。咨询或审阅本套件时，直接回答用户的问题。单角色调用只读取与该任务有关的规则和角色说明。
2. 优先采用用户最新指定的模式，其次沿用项目已有模式。“共同写作”“逐节讨论”及 `co-pilot`、`co-design` 均按 co-write 处理。新任务未指定模式且无共同参与意图时，采用 auto-pilot。
3. 全流程读取[工作流程](references/workflow.md)、[工作文档](references/artifacts.md)和 [A 角色说明](references/writer.md)。auto-pilot 由 A 在委托范围内代拟和决策，E 独立复核。co-write 按[共同写作说明](references/co-write.md)与用户逐节讨论和修订，结构确认后沿用该模式。在 `plan.md` 记录当前单元和授权范围。
4. 沿用现有项目资料和用户指定的产物目录。新项目默认写入项目内的 `proposal-work/`。按需运行只读检查 `python scripts/check_dependencies.py`。低空项目可参考[指南示例](references/low-altitude-example.md)。

## 角色调度

主对话使用宿主的子 agent 委派功能并向用户转达反馈。A 维护主稿，B 和 D 可并行核查内部基础与外部证据，E 独立评审，C 按已定方案配图。派发时给出任务范围、必要来源、已确认和待定事项、角色说明、可写文件及完成判据。

按实际并发上限分批调度。主对话加工作者最多四个时，可先安排 A、B、D，再安排 E 和 C。并发已满时先复用空闲容量。宿主无法派发时串行处理，并如实说明独立评审的完成情况。子任务留在当前项目对话内。

## 交付

A 核对正文和受修订影响的文件，E 复核实质问题。证据不足时注明缺口并推进其余工作。交付实际文件、完成状态及影响定稿的未决事项。正式提交另需用户授权。Word、PDF 或幻灯片按用户需要调用相应技能。
