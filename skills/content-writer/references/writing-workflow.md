# 写作总流程与细调位置

本图是流程细调期间唯一维护的总图。状态表示规则细调进度，不表示当前文章已经生成。“已确认”只表示节点方向获确认，节点内旧参数仍须按下方待核对项区分，不能当作全部逐条获批。每轮保持节点和整体范围，更新细调位置；不以当前模块局部图替代。所有生产模块均执行“写/生成 → critique → 修改复查 → 放行”。

```mermaid
flowchart TD
 E["writing-router：统一入口"] --> I["第一步：初始化／恢复<br/>内部调用workspace-initializer<br/>存储、主题、DIY、分发平台"] --> G["至少10条有效对标<br/>不足请用户补链接→content-collector入库"]
 G -.-> K
 G --> A["writing-router：继续调度<br/>主题、目标、指定题与否"] --> RS{"热点雷达开关<br/>妈妈善食默认关闭"}
 RS -->|开启| R["topic-radar 通用模块＋主题包<br/>热点报告"]
 RS -->|关闭，直接进入| B
 R --> B["audience-report 通用模块＋主题包<br/>用户洞察与真实场景"]
 B --> T["topic-generator 通用模块＋主题包<br/>未指定：第一轮→用户选择→第二轮<br/>已指定：直接第二轮"]
 T -.-> C["content-collector：第二轮至少新增1篇<br/>定向采集，不自动调用pattern-extractor"]
 C -.->|采集结果交回第二轮| T
 T --> P["content-planner<br/>统一Creative Brief、内容包、信息量与拆篇规划"]
 P --> PA["product-amplify：启用篇的功能证据与承接规划<br/>故事类在分镜定稿前完成解决方案融入"]
 PA -.-> S
 P --> PL["知识型／故事型／产品型<br/>长文、短图文、短漫画、视频等"]
 PL --> H["hook-generator：钩子与注意力设计"]
 H --> S["story-builder：真实场景与故事方案"]
 S --> F{"各平台正式制作"}
 F --> X["content-writer：小红书"]
 X --> X1["title-writer＋image-copy-writer<br/>两套内容→文字审查"]
 X1 --> X2["cover-generator→image-generator<br/>封面选择与内页"]
 X2 --> XB["body-writer：正文与互动"]
 XB --> XP["product-amplify：按篇启用<br/>产品图＋正文搜索承接句；关闭则跳过"]
 XP --> X3["hashtag-writer：10个标签"]
 X3 --> X4["pinned-comment-writer"]
 F --> W["wechat-writer：公众号"]
 W --> W1["title-writer＋body-writer<br/>标题与完整正文"]
 W1 --> W2["image-copy-writer<br/>按正文规划横版配图→审查"]
 W2 --> W3["cover-generator→image-generator"]
 F --> N["抖音／视频号／自定义平台<br/>缺流程先DIY配置，生产协议待细调"]
 X4 --> Z["整篇验收→已选后端交付与图片归档"]
 W3 --> WP["product-amplify：按篇启用<br/>文末产品承接；关闭则跳过"]
 WP --> Z
 Z --> RV["review：发布后复盘"]
 K["独立对标建库任务<br/>content-collector→pattern-extractor"] --> DB["对标素材／规律库"]
 DB -.->|按题引用，缺项定向补齐| T
 D["主题包→内容包按章节交接"] -.-> P
 K -.->|洞察增量经统一关口| B
 T -.->|交接前增量回写| B
 RV -.->|新证据与组合表现| B
 style B fill:#dcfce7,stroke:#15803d,stroke-width:3px
 style RS fill:#fef3c7,stroke:#b45309
 style I fill:#fef3c7,stroke:#b45309
 style G fill:#fef3c7,stroke:#b45309
 style T fill:#fef3c7,stroke:#b45309
 style P fill:#fef3c7,stroke:#b45309
 style PL fill:#fef3c7,stroke:#b45309
 style PA fill:#fef3c7,stroke:#b45309
 style XP fill:#fef3c7,stroke:#b45309
 style WP fill:#fef3c7,stroke:#b45309
 style K fill:#fef3c7,stroke:#b45309
```

两条分支均完整执行；指定题只跳过第一轮选题生成，第二轮调研照常完成。每个生产模块执行 critique、修改复查与放行。公众号 WX1—WX8 于2026-10-07确认为暂定固定基线；单篇内容参数仍随对标、主题与批准方案确定。


当前已落实：正文三部分规则组合；正文与评论钩子的交付结构，产品承接按篇启用并由product-amplify提供；对标逐句语气与文本结构映射；逐句四项 critique 和逐模块放行；图文互补与评论逆向提问。`hashtag-writer` 已拆分并固定10个；取消固定求赞。搜索关键词与标签的强制映射已确认，下游环节继续逐项细调。妈妈善食统一封面标准已确认，读取 pregnabite-writing 的飞书规范与标准图，不从新对标自动更换。

## 当前流程修正位置

2026-10-10统一分发：当前位置为 writing-router 就绪状态提示与安装验收。沿用上方同一总图；所有人共用 routes.json，小红书图文和公众号长文 ready，其余分支施工中。新分支完成后更新状态并同步即可使用。待细调清单见 ../../RELEASE-BACKLOG.md；topic-radar 延期。

2026-10-10当前：所有来源统一经audience-report写入关口使用最新规则。有增量写入与回读成功再交接，无新增记录后继续，失败保留待回写；独立对标、两轮选题、writer补查和review同样适用。协议只维护在 audience-report/references/writeback-gate.md。

2026-10-09当前细调：六维整表按通用字段标准重写，具体任务用完整自然语言、身份用人群标签、关切归核心痛点、情绪只写感受、障碍解释做不到的原因。audience-report 新增搜索栏长尾词逐词查量；六维允许基于具体处境推理情绪与关注点；实际困惑改为原话优先的自然语言记录，取消人工审核占位。唯一规则见 audience-report/references/insight-recording.md。此次整理既有资料，不代表已执行新一轮搜索。

2026-10-09：热点雷达改为可选开关，妈妈善食流程默认关闭；规则已确认。关闭后从洞察继续，热点报告不作为必备输入，旧雷达补查不自动恢复。开关唯一协议见 writing-router/references/orchestration.md。

2026-10-08当前细调：对用户统一使用writing-router；workspace-initializer只是第一步内部子模块。初始化入口、飞书/Obsidian存储映射、主题包发现、DIY覆盖、平台选择与10条对标准备门已写入规则，新的初始化尚未实机试跑。

2026-10-08已确认主线：指定题调用topic-generator第二轮，未指定题从头执行；content-research合回。按初始化选择的平台规划，content-planner按知识点、例子、依赖与载体容量拆篇。对标建库是独立工作流；单篇优先引用与定向补缺。wechat-writer为统一新名称。本轮已固定至少1篇新增对标的定向采集、通用六维方法与可选product-amplify。钩子、故事及抖音制作细则仍待细调。

### 已固定的平台分支

2026-10-07 当前修正：公众号正文先行流程固定，由 writing-router 进入 wechat-writer 的 WX1—WX8，执行其 execution.md 放行与续做规则。首篇按用户指令收尾，制作交付、发布端排版预览、实际发布分别记录；不宣称已执行发布。小红书新增 L2，位于 L Hashtag 后、M 整篇验收前。本轮先建评论对标库，具体承接形式待调研后选择，不默认固定某种引流话术。

research-core 维护通用调研，pregnabite-research 维护主题范围与资料位置，wechat-writer 维护公众号正文先行分支。资料、通用写法和模块 critique 继续引用唯一来源；两组图片候选及图片文字审批放在配图阶段。小红书的图片先行、短正文容量、20字、10个Hashtag等不自动移植。下方历史确认记录和图文逐页数量规则按其小红书作用域保留。公众号稿单独建文档，不能合并进小红书原稿。

断点继续执行 [断点恢复协议](resume-contract.md)：同时记录平台与阶段。既有小红书编号保留用于旧任务恢复，L 后新增 L2 置顶评论；公众号按 wechat-writer 的阶段恢复，不能把公众号记录为 O。历史案例的暂停记录不代表当前任务进度。

## 历史确认记录（历史单篇进度不代表当前状态）

- 2026-10-01已完成洞察链路回查：60篇图文＋7篇视频的需求记录、原对标分析需求段及问题回链均已修正；飞书《用户洞察》保留具体场景与来源，修正六维、问题卡、关键词关联及受影响方案。68篇文档回读通过，原有用户退回决定、90个关键词的指数与排序保留。`audience-report`已加入逐条原文验收与联动修正规则。此完成状态仅指洞察与对标需求链路，020稿件尚未重制。

- 2026-10-02继续纠正020结构适配：已选B16为6页，首页7项提醒、后5页各2项推荐。通用规则已固定“原图信息需求与数量→查证选材→逐页写作”，修正先写少量内容再自行减页的冲突。020飞书文案按此重写并完成结构及逐句审查，当前待用户审查图片文字；未生成新图、未完成正文，不能称整篇已完成。

- 用户明确确认且已落实：三部分规则组合、对标信息关系、两套内容、Brief末尾文字审批、正文固定三部分、逐句模仿与 critique、固定10个标签、取消固定求赞。
- 本轮新增模仿检查是对用户“标题与图片也需加强”的落实；不得声称已经通过实际写作质量测试。
- 旧参数本轮已确认：三个不同成品标题分别模仿三个不同标题对标；小红书发布标题20汉字以内归平台包；正文对标篇幅约±100字只作参考，以适中讲清主题为准；第二轮总计至少3篇，其中本轮至少新增1篇对标并完成入库（现行定向采集不自动分析），writer复用不重跑。
- 已确认：按现有位置和数量强制添加Emoji；采用的评论必须有评论自身的非零点赞或可核验回复，无互动不采用。
- 已确认：搜索词与Hashtag逐项对应，来源及本篇回答位置可追溯；不再重复请求确认。本轮旧参数核对结束。
- 实施细节（本轮未单独询问）：独立Skill名称、引用路径、句子ID/审查记录格式及同步方式。属于执行安排，不称为用户指定格式；不得据此要求用户填写更多表格。
- 妈妈善食封面视觉已确认并由 cover-generator 执行，唯一规范引用见 pregnabite-writing；内页仍沿用其获批方案，不能将封面模板强套全部内页。

## 全流程规则核对索引（2026-10-02）

本表指向唯一规则来源，不复制方法或账号知识。节点确认记录仍按上文区分；本次只清理已确认要求的执行冲突，不将规则检查称为实稿质量测试。

| 已确认要求 | 唯一执行来源 |
| --- | --- |
| 语义路由、通用/平台/主题组合；写作与 critique 共同使用 | content-writer 模块路由、writing-core、xiaohongshu-writing、pregnabite-writing |
| 指定题从topic-generator第二轮开始；定向研究至少3篇、至少1篇新增入库（小红书，定向采集不自动分析）；writer复用并定向补缺 | topic-generator；用户明确单篇豁免仅限该篇 |
| 对标分析原位保存、准确需求回写、形式分类、知识核验及正文互补 | pattern-extractor/references/benchmark-analysis.md、audience-report |
| 每篇写前实际读取已存分析；继承逐页功能、信息关系和数量，再查证选材 | image-copy-writer 前置门槛及信息需求规则 |
| A/B 两组独立全套内容；更换整组重新适配 | production-review.md 两套内容方案验收 |
| 3个不同发布标题分别模仿3个来源；小红书20汉字以内；图片标题增强、人群标签 | title-writer、xiaohongshu-writing |
| 搜索词引用洞察词表；产品具体说法复核；Brief末尾全量图片文字获批后出图 | brief-approval.md |
| 封面选择后生成所选内页；分析、原图、获批文本与实图逐页核对 | cover-generator、image-generator |
| 正文补充图片，逐句模仿；正文与评论钩子完整；启用时含产品承接；逐句四项审查 | body-writer、writing-core、stage-critique.md |
| 评论有自身点赞/回复证据，用于补充写法与反推互动；强制Emoji、无固定求赞；恰好10个标签 | writing-core、xiaohongshu-writing、hashtag-writer |

已清理旧顺序：先写文案再定页数、先想菜再找图片、按现成密度逐页找模板、无批准自行减页；已清理固定第一篇正文结构与至少三个正文模块的要求。妈妈善食封面现执行已确认统一标准，结构复刻不自动更换账号风格。

## L2 置顶评论（2026-10-07新增）

唯一执行规则为 `../../pinned-comment-writer/SKILL.md`：先读取真实评论对标及逐句分析，再逐句对应写作和 critique；有来源、评论自身互动、完整映射及通过审查的独立草稿才进入M。与正文评论钩子分开，发布/置顶动作不自动执行。首次无库先调研入库，之后复用并补缺，研究不重复整轮选题。
