# 工作流待细调清单 · 2026-10-10

用途：维护待办，不表示本轮重新跑完内容生产。员工开放范围由版本包的 release-profile.json 单独确定。topic-radar 留到个人自媒体流程再调，妈妈善食保持关闭。

## 各 Skill 当前成熟度

|Skill|当前状态与下一步|
|---|---|
|writing-router|调度已拆；本轮增加员工范围与启动确认。需要新机器断点续做回归。|
|workspace-initializer|初始化规则已写，飞书/Obsidian、新主题、DIY尚未逐场景实跑；重点验证权限与素材映射。|
|research-core|通用取证、六维、场景交接已调；跨主题取值与各平台边界需回归。|
|pregnabite-research|主题研究与洞察规则已调；更新后需一次真实增量研究验证。|
|audience-report|近期已细调六维、原话、长尾词及统一回写；需实跑搜索指标和增量去重。|
|topic-generator|两轮、指定题入口、新增对标已固定；第一轮候选质量、排序、成篇判断细则仍需逐项细调。|
|topic-radar|延期，个人自媒体流程再调；妈妈善食 off。|
|content-collector|采集规则已有；独立建库与选题定向采集的调用边界需统一复核。|
|pattern-extractor|逐模块、逐句、信息关系与洞察交接已调；新素材增量分析需回归。|
|content-planner|职责与信息容量已定；方案评判、拆篇边界、各形式容量尚待细调。|
|hook-generator|仅职责和交接框架；候选生成、注意力机制与验收细则待调。|
|story-builder|仅职责和真实场景边界；故事节奏、篇幅、漫画分镜与验收待调。|
|writing-core|图文互补、主题一致、逐句 critique 已调；洞察旧状态措辞需与新规则核对。|
|xiaohongshu-writing|图文平台规则已调；员工环境实稿验收待做。|
|pregnabite-writing|品牌、主题资料与表达偏好已有；新机器资料和资产访问待验。|
|content-writer|图文主链已有实际制作；新调度器整合后需断点回归。|
|title-writer|三标题、三对标、人群标签与标题角色已调；持续随实稿复核。|
|image-copy-writer|先结构后信息、两套内容、文字审批已调；核对新对标分析缺口处理。|
|cover-generator|品牌样式、字体、高亮与候选选择已调；确认员工可读取规范原图。|
|image-generator|信息数量、版式、间距和实图验收已调；工具和归档路径需新机验证。|
|body-writer|主题互补、逐句对标与 critique 已调；产品段启用条件需全链一致。|
|hashtag-writer|固定10个、关键词映射已调；平台作用域维持小红书。|
|pinned-comment-writer|作者置顶、触达/内测、逐句参考已调；长度区间与逐篇内测选择复核。|
|product-amplify|按篇开关及三种载体分工已定；故事型植入待细调，现有正文旧必选要求需审计。|
|wechat-writer|正文先行 WX1—WX8 暂定基线；平台研究门槛、复制排版、发布端验收仍待完善。|
|review|复盘及洞察回流已写；真实发布数据权限、采集和复盘闭环待验证。|
|site-review|网站独立模块，不在写作安装包；无需强塞进笔记链路。|

## 流程缺口与潜在规则冲突

|编号|位置|问题与后续动作|状态|
|---|---|---|---|
|F01|content-planner P0 / writing-router orchestration|雷达关闭仍要求热点报告；改为仅开启时读取。|本轮修复|
|F02|content-collector / pattern-extractor|独立入库必须分析，但第二轮定向采集不自动调用提取器；检查所有入口是否准确区分。正式制作前仍必须有完整分析。|待细调|
|F03|writing-core 表达与信息取舍 / audience-report|“审核状态、待审核线索”可能重新引入已取消的人工审核。需统一为证据和适用性核验，保留有据推理与事实的区别。|待细调|
|F04|content-writer、wechat-writer、body-writer / product-amplify|部分历史正文三段要求可能被理解为产品段必选；逐处核对 product_mode。|待审计|
|F05|research-core / 写作评论规则|发现问题阶段与定题后评论补充的权限不同，不能将禁止评论改题误读为研究不看评论。|作用域回归|
|F06|workspace-initializer / 各写作引用|存储支持飞书和Obsidian，但部分下游仍写“飞书”；需检查真实读写是否按映射，不能只改措辞称支持。|待验证|
|F07|content-planner→hook-generator→story-builder|细调未完成的模块已串入；知识图文应保留有据场景，不能强制扩写故事。|待细调|
|F08|员工分发|安装文件≠授权工具≠工作间配置≠端到端试稿；需验证飞书权限、原图、图片生成及归档路径。|待员工实机验收|
|F09|发布与更新|员工固定版本使用，不直接追主分支施工规则；发布包应仅含技能、安装器与说明。|本轮建设|

## 建议后续顺序（供之后选择）

先解决 F02—F04 的规则衔接，再细调 topic-generator → content-planner → hook-generator → story-builder；公众号排版与跨主题初始化分别试跑。topic-radar 暂不展开。

总流程图仍只维护在 content-writer/references/writing-workflow.md，不另起第二套总图。当前工作位置：规则审计、员工分发与安装验收。
