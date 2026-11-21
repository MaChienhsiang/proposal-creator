---
name: proposal-creator
description: >-
  面向多方向理工科科研项目申请书的五角色协作入口，适用理论、实验、计算、工程及交叉研究；按资助机构、项目类型、指南和研究方法适配，不限低空或 NSFC。统筹论证、研究目标与评价、基础、文献、配图和独立评审。支持 auto-pilot 全自动与 co-write 共同写作，后者贯穿架构、逐节起草和修订。A 编写与 domain-modeling，B 基础，C 绘图，D 依据，E 评审与 grilling；支持五角色单独调用。
---

# Proposal Creator

把用户的研究意图、适用申报要求和团队积累转化为可追溯、可检验的申请方案与文稿。既支持有任务指南的项目，也支持自由探索课题。保持五个专业角色，按需要调度，不把角色数量当作并发数量。

## 调用方式

| 调用示例 | 模式 | 主要责任 |
|---|---|---|
| `$proposal-creator` | auto-pilot / co-write | 全自动或与用户共同写作，协调五角色 |
| `$proposal-creator writer` | [A / writer](references/writer.md) | 方案与正文 |
| `$proposal-creator foundation` | [B / foundation](references/foundation.md) | 内部研究基础 |
| `$proposal-creator figure` | [C / figure](references/figure.md) | 图件与验收 |
| `$proposal-creator evidence` | [D / evidence](references/evidence.md) | 外部依据与引用 |
| `$proposal-creator reviewer` | [E / reviewer](references/reviewer.md) | 独立评审、grilling 与复核 |

同一入口接受自然语言参数，例如 `$proposal-creator auto-pilot …`、`$proposal-creator co-write …`、`$proposal-creator reviewer …`。`co-pilot` 和旧 `co-design` 是 `co-write` 的别名。这些是本 skill 的参数约定，不宣称宿主支持冒号命令。

## 启动

1. 读取 [共同规则](references/common.md)、[项目适配](references/project-adaptation.md) 和 [依赖路由](references/dependencies.md)。先提取资助类型、领域、研究方法、正式要求和证据判据；独立角色只提取相关部分。
   用户仅咨询、比较或审阅本套件时，只完成该请求，不启动申请书项目。
2. 根据最新明确指令选路，其次沿用项目已记录的模式；“共同写作”“一起写”“逐节讨论”等均进入 co-write。只有新任务既无模式、也无共同参与意图时才默认 auto-pilot。用户只要求某个角色，读取对应角色文件并仅完成该职责；不要顺势启动全流程。
3. 全流程读取 [自动与共同写作流程](references/workflow.md)、[文档与交接](references/artifacts.md)，以及 [A 角色](references/writer.md)。co-write 另读 [共同写作](references/co-write.md)。A 做整章文风对齐时另读 [语言语域统一](references/language-register.md)。其他角色在派发时读取自己的文件。
4. 优先复用当前项目资料和已确认决定。沿用已有产物目录；没有时采用项目内 `proposal-work/`。尊重用户指定路径，不将申请书存进技能安装目录。
5. 如需检查依赖，可运行 `python scripts/check_dependencies.py`；只读取检查结果，不自动安装或上传任何材料。

## 主控执行方式

全流程由主对话负责调度、转达用户反馈和交付。按任务需要分别委派 A、B、C、D、E 子 agent，A 负责方案与正文；E 保留独立评审上下文。使用宿主实际提供的委派工具，不创建用户拥有的新聊天。

读取当前并发上限。若主对话加工作者最多四个，先安排 A 起草结构，B、D 可并行整理材料，随后 E 评审结构，然后按空闲额度安排 C 和后续补证。完整五角色可以分阶段执行。若宿主不能结束已完成工作者，使用有空闲容量的执行方式；确实无法创建时串行执行对应角色并报告独立性限制，不假称已启动独立 agent。

派发任务只给：目标、必要输入、相关来源、当前模式与授权范围、确定与待定事项、角色文件、可写文件、交付物及完成判据。每个角色按需读取原始依赖 skill；不要把所有 skill 全文塞给每个工作者。

## Auto-pilot and Co-write

- auto-pilot：本次明确委托授权在任务范围内设计、代拟、修订、绘图和内部复审。E 提问，A 在授权下回答并记录为 agent 决定；不反复要求用户批准每一段或每轮方案。
- co-write：用户与 A 共同确定架构、指标及当前写作单元；A 提供可审阅草稿，用户反馈或局部委托，A 修订，E 按需质询和复核。模式贯穿正文与修订，结构确认不会自动切回 auto-pilot。具体节奏见共同写作说明。
- 在 plan.md 保留模式、当前单元、用户保留的决定和已委托范围。局部授权只作用于指定问题、章节或阶段；代拟答案默认是建议，沉默或超时不是确认。
- 未知事实需要证据，自动模式也不例外。依赖不足的段落标记缺口，继续其他分支。
- 先交付任务范围内可完成且经过检查的成果。正式提交等外部动作另需用户明确指令。

## 完成

由 E 根据完成判据复核重要问题，A 检查术语、图文、指标和事实状态。交付实际文件、剩余缺口、已完成的核验及适用限制；仅通过的检查才称通过。`draft-with-gaps` 不是 `ready-for-human-finalization`。需要 Word、PDF 或幻灯片时，再按宿主对应技能创建与验收。

仅在低空相关任务需要时读取 [低空指南示例](references/low-altitude-example.md)。其他方向依据自己的对象、方法和要求组织，不加载该案例作为默认结构。项目适配不增加常驻 agent，也不改变共同写作的授权边界。
