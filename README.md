# Proposal Creator

面向多方向理工科科研申请书的五角色工作流，通过一个技能入口调用完整流程或指定角色。主入口明确支持 auto-pilot 全自动和 co-write 共同写作。A 提方案和写作，B 提炼内部基础，C 绘图，D 核外部依据，E 独立追问与评审。

## 适用范围

支持数学、物理、化学、材料、信息、机械、土木、能源、环境、地学、生物工程及交叉方向的申请书起草。按资助机构/项目类型和研究方法分别适配：理论、实验、计算、观测、工程及混合研究可使用同一流程。领域方法和事实仍须由真实材料支撑。

每次先从资料提取项目概况到 plan.md，选择适合的论证、证据、图件和评审重点；不增加管理 agent。没有定向指南的自由探索项目可以从研究问题起草；没有官方定量指标时不补造性能阈值。非 NSFC 项目采用对应机构模板与规则。低空材料只保留为按需读取的领域案例。

具体适配规则见 [Project Adaptation](skills/proposal-creator/references/project-adaptation.md)。

## 调用

| 入口 | 示例 |
|---|---|
| 全自动 | `$proposal-creator auto-pilot 依据这份指南和资料完成申请书工作稿。` |
| 共同写作 | `$proposal-creator co-write 与我先确定结构和指标，再逐节起草、反馈和修订。` |
| A | `$proposal-creator writer 与我讨论整体结构和指标统筹。` |
| B | `$proposal-creator foundation 从这些旧项目报告提炼可支撑本次任务的基础。` |
| C | `$proposal-creator figure 根据已确认方案绘制多尺度测评架构图。` |
| D | `$proposal-creator evidence 核验这些论断和引用是否对应。` |
| E | `$proposal-creator reviewer 用 grilling 检查技术路线和指标验证方案。` |

`co-pilot`、旧 `co-design` 以及“共同写作”“一起写”进入 co-write。指定单个角色时仅运行该职责。

## 依赖

Writer 在中文章节或全文成稿后调用 `lieflat-less-ai-tone` 进行语言润色。

复用现有 `nsfc-write`、`nsfc-literature`、`nsfc-figure`、`nature-figure`、`grilling`、`domain-modeling`、`anti-defensive-writing`、`humanizer-zh`；`nsfc-policy` 仅在 NSFC 相关规则核查时调用。非 NSFC 项目只迁移通用论证和工具，不套 NSFC 专属提纲、页数、定位或评分。`grill-with-docs` 可选作为组合入口；本套件适配为 E 追问、A 维护术语与决定，不改原始 skill。

调用前按角色读取依赖，原始依赖不复制入套件。运行主技能 scripts/check_dependencies.py 可检查本机路径；运行 scripts/validate_suite.py 可检查主入口、五个角色和包内引用。

## 模式与文件

auto-pilot 授权在本次任务内采用工作方案、代拟和修订。E 的设计问题由 A 回答，记录授权决定；未知事实留缺口。

co-write 贯穿整个写作过程：用户与 A 商讨结构和指标 → A 按约定章节起草 → 用户反馈或局部委托 → A 修改 → E 按需复核 → 推进下一单元。A 直接落实已有反馈；不逐句索取确认。用户可以自己回答 E、让 A 代拟建议、授权选择，或暂缓。

模式与授权范围保存在项目 plan.md。结构确认后继续共同写作；“这一节你来定”只授权该节，完成后回到共同写作节奏；“继续”也沿用当前模式。代拟不等于决定，沉默与超时不算确认。只有整个任务被明确委托时才切换全自动。新任务没有模式或共同参与意图时默认 auto-pilot，已有任务优先沿用最新选择。

默认工作输出在调用项目的 proposal-work/，不写入技能安装目录。保留原始资料和可编辑源。正式模板/指南优先于通用技能经验值。只对实际执行过的核验标通过。

## 安装

在 CC Switch 的 Skills 仓库设置中添加本 GitHub 仓库，选择包含此结构的分支，将技能路径设为 `skills`。刷新仓库列表，安装 `proposal-creator` 并为目标宿主启用。安装后，`references/` 包含五份角色说明。手动安装时复制整个 `skills/proposal-creator/` 目录。

在仓库根目录运行 `python skills/proposal-creator/scripts/validate_suite.py` 可校验安装包。

需要在技能选择器中直接调用角色时，在宿主已安装的 `proposal-creator` 目录中运行一次 `python scripts/register_roles.py`，然后新开会话。脚本在同级目录注册 `$proposal-creator-writer`、`$proposal-creator-foundation`、`$proposal-creator-figure`、`$proposal-creator-evidence` 和 `$proposal-creator-reviewer`，五个入口共享主包内的角色说明。也可以从仓库运行脚本，用 `--skills-root` 指定包含已安装主包的宿主技能目录。
