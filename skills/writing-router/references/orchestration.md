# 三层调度与文档交接

多平台和多形式执行[逐条制作协议](serial-production.md)：可统一策划内容包，正式生产按队列逐稿完成。下文“各平台”“双形式”表示规划范围，不表示并行制作；每稿的独立文档、Creative Brief和放行条件以该协议为准。

## 顶层：writing-router

用户统一进入writing-router；其第一步内部执行workspace-initializer或读取已有配置；configured与素材门production_ready分开。用户DIY覆盖在本工作间保存，router合并生成当前有效步骤，不修改共享基线。

一句话识别账号/主题、指定题与否、内容目标及断点。读取workspace-initializer确认的多平台选择，不默认三平台；用户明确限定本轮范围时遵从。

漫画顺序优先：取材与题意确定 → topic-generator按漫画类型与本题共同匹配至少3篇对标、自行拆解，content-collector定向采集 → story-builder＋product-amplify联合完成含产品动作与帮助的完整故事首稿 → 对照漫画原帖检查故事 → content-planner与hook-generator完成改编Brief → 分镜文案 → 图片。具体调用和断点见[漫画完整流程](../../comic-writer/references/workflow.md)。产品开关先读用户已确认任务输入，再写入后续独立Brief，不要求先完成Brief才能写故事。

其他分支完整新写作：topic-radar（可选，按下方开关）→ audience-report → topic-generator（未指定题从第一轮开始；指定题从第二轮开始）→ content-planner构建内容包与Creative Brief（初期即调用hook-generator，共同确定具体钩子及内容展开，写前复查）→ story-builder → 各平台正式写作。未指定题的第一轮候选由用户选择，再执行第二轮；已指定题不重复要求选题。

Topic Generator第二轮验证题意、答案依据、内容可展开性并寻找相近参考；完成后交策划师，不另设content-research重复研究。已有同轮研究复用补缺。独立模块只运行指定模块，续做恢复当前步骤，不从头重跑。

## 热点雷达开关

以 radar_mode=on/off 保存流程选择，随任务交接；优先采用用户本轮明确选择，其次工作间已保存选择。2026-10-09 用户确认“妈妈善食”流程默认 off，之前试跑雷达不视为启用配置。其他流程首次未配置时询问开启或关闭，已有选择不重复询问。用户明确单独调用雷达仅启用该次，不自动修改长期配置。

off 时跳过 topic-radar，直接进入 audience-report；不创建、更新或要求读取热点报告，不因报告缺失/过期阻塞，不恢复旧雷达补查待办。记录 radar_status=skipped_by_config，保留历史报告。用户重新开启后才恢复雷达步骤。已有新鲜资料可以作为普通相关证据使用，不因此隐式启动扫描。需求验证、搜索词研究、事实核验与每题新增对标照常执行。

on 时传入工作间 `radar_sources`，来源平台与 `selected_platforms` 分发平台独立。按 [社媒来源与平台适配协议](../../topic-radar/references/social-sources.md) 调度固定博主、关键词/话题发现及各平台断点；官方资料仅作事实核验。平台采集状态、扫描状态、素材入档状态分别返回，不能因某个平台缺写作包跳过采集，也不能因规则已支持就声称已接通。没有来源配置时复用用户明确范围，否则补问；不静默以新闻扫描代替。

## 独立对标库工作流

专门收集/扩充对标：content-collector → pattern-extractor → 对标素材与规律库（交接前执行audience-report统一写入关口）。这条独立流程不作为每篇写作的必跑主线。

单篇选题研究按当前类型与主题共同匹配同一组对标，小红书至少3篇、本轮至少1篇新增。topic-generator负责检索、完整阅读、内容与呈现方式拆解及方向交接，content-collector负责定向完整采集；此路径不调用pattern-extractor。已有同轮研究复用补缺，不另拆主题组和表达组。独立建库或后续深入分析才按实际任务调用pattern-extractor，不能把两条路径混为必跑主线。具体门槛统一执行topic-generator/references/second-round.md。

## 中层与底层

逐节点执行[通用底座与主题补充协议](topic-overlay.md)，用实际产物判定执行完成。产品开启时，策划初期即调product-amplify做问题与能力匹配；故事分镜定稿前回传具体承接文字，再交writer整合。不能直到结尾才临时找功能，也不能把读过模块当作执行完模块。

中层是雷达、洞察、两轮选题、策划、钩子、故事和各平台writer。底层为各模块内部步骤和title-writer、image-copy-writer、body-writer、cover-generator、image-generator、hashtag-writer、pinned-comment-writer。

每个模块自身维护通用方法，主题包统一提供人群、六维配置、搜索种子、报告/素材位置、产品事实和品牌引用。audience-report和topic-radar均按“通用模块＋主题包”组合，不能把账号资料硬编码进去。内容包交接只通过主题包读取业务资料；平台执行时另加载对应平台规则，策划不以当前平台模板限制信息范围。

## 用户洞察写入与模块放行

所有模块统一执行 [audience-report写入关口](../../audience-report/references/writeback-gate.md)。有新洞察，调用其增量模式并按当前规则写入、回读后放行；无新增直接记录并继续；待回写不得标完成。此关口也适用于独立对标、选题、writer补查、review及用户纠正，不触发整轮研究。规则和状态字段只引用该协议。

## 内容包与恢复

执行 content-planner/references/content-package.md。一个选题可拆多篇、多个载体，每篇记录独立承诺和信息范围；规划不等于自动制作发布。按已选择平台规划，抖音/漫画等未细调生产协议时如实标注。

交接存已选飞书或Obsidian文档：task_id、内容包ID、主题包、报告/问题/参考ID及位置、输入版本、具体场景、产物、critique、批准范围、下一步。下游回读来源，聊天摘要不替代交接。产品、文案与图片审批点保留。

## 可选产品承接

逐篇读取content-planner的product_mode。off跳过product-amplify；on按其载体协议执行图文产品图＋正文搜索句、公众号末尾话术、漫画故事中的产品解决方案。漫画故事与story-builder同节点联合写作，首次交付即落实具体产品动作与帮助；图文/公众号在主体后落实，最终验收前完成。body-writer不重复生产产品段。
