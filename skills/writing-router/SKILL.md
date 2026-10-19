---
name: writing-router
description: "统一内容写作入口；第一步内部完成工作间初始化或配置检查，再调度调研、选题、策划和各平台制作，支持换主题与断点续做。"
---

# 写作入口

内容包统一策划后，按[逐条制作与独立稿协议](references/serial-production.md)调度：一次只制作一条，当前稿完成全部适用制作、审查和归档后再取下一条；每个平台、形式、篇次独立文档与Creative Brief。每次恢复先确定唯一当前稿。

用户统一调用writing-router，无需另记初始化入口。写作规则直接加载writing-core、平台包与主题包，资料及授权绑定读取workspace-initializer配置；在WorkBuddy等宿主同样按这些文件执行，不以根目录agents.md是否加载为前提。

初始化前先读取 [当前可用分支与启动提示](references/distribution.md) 和 [routes.json](references/routes.json)。所有人使用同一套规则，按分支 ready 状态提示可用平台；已授权开始或续做直接执行，不重复询问启动。

## 第一步：初始化或恢复工作间

workspace-initializer是本入口内部调用的初始化子模块，不作为替代入口向用户推荐。首先读取当前工作间的配置。首次使用、配置缺失、换主题或用户要求修改工作间时，执行 [workspace-initializer](../workspace-initializer/SKILL.md)，完成存储、主题包、DIY、平台选择与至少10条有效对标检查。配置存在时复用并核验，不重复初始化。每个下游模块须接收有效存储映射与DIY路由；存储适配按 [后端协议](../workspace-initializer/references/storage.md) 执行。

## 后续：调度内容协作

漫画分支由 [comic-writer](../comic-writer/SKILL.md) 串联既有底座。每轮漫画制作、细调与进度答复展示其[固定完整流程图](../comic-writer/references/workflow.md)，保持节点，仅更新状态；分别记录规则细调与本稿进度。分支仍试行，不因有Skill文件改为ready。

网页调研工具及断点恢复统一按 [research-core浏览器固定入口](../research-core/references/browser-route.md) 执行，将已验证浏览器会话与读取范围交给下游；不因切换Skill或新会话重新选浏览器。

涉及需求、选题或对标研究时先加载 `../research-core/SKILL.md`，再组合当前平台研究规则与研究主题包；妈妈善食用 `../pregnabite-research/SKILL.md`。写作包和研究主题包分别加载，不让领域搜索词进入通用方法。

完整新写作与独立模块的调度先执行 [三层调度与恢复](references/orchestration.md)，按其中 radar_mode 开关执行；妈妈善食流程默认关闭热点雷达。

先读 [配置与交接](references/handoff.md)，依据语义与已有任务识别需求，不用单个词硬匹配账号。

每次调度执行[通用底座与主题补充协议](references/topic-overlay.md)。按节点组合模块方法、平台要求、主题资料与本稿决定；读取Skill不等于已执行模块。产品开启的故事稿必须在策划和分镜定稿前执行product-amplify，回传实际功能匹配和承接文字，不以列出名称或读完功能表代替。

1. 新任务确定账号/主题、选题来源与目标，读取初始化确认的分发平台，不默认三个平台；类型与载体由内容策划细化；续做先通读飞书当前稿与执行状态。用户已说清的字段直接沿用，仅对有歧义的组合确认一次。
2. 加载 `../writing-core/SKILL.md`、当前平台包及当前主题资料。小红书用 `../xiaohongshu-writing/SKILL.md`；公众号用 `../wechat-writer/SKILL.md`；仅妈妈善食用 `../pregnabite-writing/SKILL.md`。账号不明不能默认妈妈善食。
3. 漫画优先按comic-writer执行：取材与题意确定 → story-builder＋product-amplify联合完成含产品动作与帮助的完整故事首稿 → 漫画对标适配及content-planner/hook-generator改编策划 → 全量分镜文案 → 出图。以下一般顺序适用于其他分支：选题确定后先执行 `../content-planner/SKILL.md` 的内容包策划、各稿独立Creative Brief与研究，策划初期即调用hook-generator共同确定具体钩子，再进入story-builder；完成适用方案后，小红书知识型图文执行 `../content-writer/SKILL.md` 及其总流程（Hashtag 后进入 L2 置顶评论）；公众号知识型长文执行 `../wechat-writer/SKILL.md` 的 WX1—WX8。公众号使用本入口恢复和分流，不另造一套资料配置。其他组合缺执行包时先细调该分支，不宣称已支持。
4. 事实、对标分析、洞察、产品能力保留原位置引用，写作与 critique 使用同一套要求。切换公众号从平台入口分支，独立重走调研、对标分析、正文 Brief、完整正文、按正文规划配图与生成、合并验收。不同平台创建独立飞书稿及断点，共享资料只引用原链接。指定题调用topic-generator从第二轮开始；未指定题从第一轮开始。已核验事实可复用引用，不能代替目标平台研究。
5. 平台切换不继承另一平台的字数、标签数、Emoji、封面比例或页数。账号表达偏好继续使用；旧要求范围不清时列为待核对，不擅自推广或取消。
6. 每模块交接前执行 [用户洞察统一写入关口](../audience-report/references/writeback-gate.md)。每模块执行通用、平台、主题三部分 critique。状态写入已选存储后端；“继续”只推进记录中的下一步，不代替新功能说法、改题或方案选择的批准。

规则可迁移；飞书权限、登录态、工具与账号素材需接通。新主题先绑定自己的资料，缺素材进入研究，缺权限报告具体缺口。相同规则保证相同要求和检查点，不承诺逐字相同。未跑完实稿的分支标为试行。
