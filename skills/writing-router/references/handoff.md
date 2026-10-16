# 配置与交接

配置放在已选后端00_账号背景/工作间配置及任务制作备注；完整字段与存储适配引用workspace-initializer。以下是字段约定，不复制账号知识。

| 字段 | 内容 |
| --- | --- |
| storage_provider / workspace_id / selected_platforms / workflow_overrides | 已选后端、工作间标识、分发平台与DIY覆盖 |
| account / account_root | 已确认账号与知识库作用域 |
| positioning / writing_principles | 定位与表达偏好原文链接 |
| radar_mode / radar_status / radar_doc / research_objective | on/off、实际执行或skipped_by_config；热点报告仅开启时为输入，关闭时允许为空；内容选题或产品验证选题 |
| audience / benchmarks / patterns | 洞察关键词、对标库、分析原位置 |
| pinned_comment_benchmarks | 本账号评论区引流对标库链接；小红书 L2 调用 |
| product / brand | 产品与品牌规范链接；无产品账号由用户确认适用结构 |
| platform_policy | 当前平台来源；账号自订限制另标范围 |
| drafts / archive_root | 实际文档交付位置与图片归档根目录 |

路径按当前机器验证，作者电脑的 D 盘路径不作为他人默认路径。授权、密钥和登录态不进入规则包。按 account_root 隔离来源，主题相似不能跨账号读取。

## 任务断点

先按[逐条制作协议](serial-production.md)读取内容包的production_order、active_deliverable_id及各条目的平台、形式、篇次、独立文档、Brief位置、状态和下一步。“每个平台各一个稿”细化为每个平台×形式×篇次各一份独立稿；待审或阻塞不自动切换下一稿。

记录 task_id、平台/形式/主题、规则包版本及校验结果、来源文档与读取版本、平台分支与阶段节点、分支子步骤、已批准原句/图片方案、待审批项、下一步及实际交付清单。写具体值，不只写“已完成”。

同一选题切换平台，为目标平台新建独立创作文档与断点，每个平台×形式×篇次各一份独立 AI 稿；不得把公众号章节插入原小红书稿，也不得覆盖原稿。目标平台从调研开始独立执行完整流程，不能记录为原平台验收后的末尾衍生步骤。共享资料引用原链接。原平台已批准稿保持原样，衍生审批不反写成原平台批准。

公众号阶段放行及收尾状态执行 wechat-writer/references/execution.md。小红书记录 L2 置顶评论的主样本、逐句映射、产品复核与草稿状态；旧任务未包含此环节时标为未做，用户明确要求继续整篇制作再进入，不重开已收尾稿。

## 换机验收

安装后核对包文件哈希，现场读取账号配置和断点，验证飞书、素材、生成工具及归档路径。规则安装成功与端到端跑通分别报告。未提交、推送的工作区文件不会随另一台电脑 git pull 出现。
