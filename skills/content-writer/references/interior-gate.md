# 小红书内页生成前检查

本页落实既有选模与结构复刻要求。每批内页调用生成工具前，从刚回读的飞书执行状态导出临时 JSON，运行 `python skills/content-writer/scripts/check-interior-handoff.py <临时JSON>`。未通过不调用生成工具。公众号按其独立流程执行，不套此检查。

## 证据与字段

漫画首页按 [首页即封面的情景建立规则](../../story-builder/references/comic-storyboard.md) 处理。现有脚本的samples路径固定P02，不能用于宣称漫画P01检查通过，也不能把P01伪登记成P02。用户明确批准漫画首页重排或定向修订时，沿用本页“明确批准的结构变更”路径，记录来源、页码变更、全文批准范围和人工情景检查；其余已选内页仍按适用脚本执行。不为补脚本字段重新生成通用封面。

- `mode`：`samples`仅生成两套已批P02比较样张；`selected`生成或修改已选整组内页。
- `schemes`：每套包含`id`、`note_id`、`analysis_ref`、`source_manifest_ref`、`text_version`、`text_approval_ref`、`expected_pages`、`planned_pages`。
- 两份页面清单均用有序数组，每页包含`output_page`、`note_id`、`source_page`、`task`、`units`（各区独立条目数）、`relations`（信息关系）。expected从实际原图和已存分析继承，执行首页去重；planned从本篇实际Image Brief提取。samples时expected保留完整原图结构，planned仅需P02；selected时只检查所选方案，planned须覆盖所选完整组；未选方案可仅保留样张记录，不作为出图前置。两者独立回读核对，禁止复制计划冒充原图基准。通用品牌封面不占内页清单。
- `outputs`：本批每页的`scheme`、`output_page`、`text_version`。
- `selection_version`：方案被选时的样张版本。选择后补齐剩余文字可更新text_version及其文案批准，但保持selection_version和原选择记录，不能因此重新选模。
- `selected_scheme`及`selection`：用户所选方案；selection包含`scope=whole_scheme`、`scheme`、`note_id`、`text_version`、`user_message_ref`、`user_quote`、`prompt_ref`（当时请用户选择的消息）、`display_ref`（实际展示的原图/样张）。真实“选第二个”可结合当时展示顺序解释为B；“继续写、改标题、封面可以”不得扩大为选模。

保存可定位的用户原话及上下文，不能用agent写的“用户已确认”自我证明。没有批准证据就保持未选；已经明确选过则沿用其真实记录。换对标、拼接模板、合并或删除内容页不属于局部文案修改。

每个方案只以一篇完整对标控制内页结构。其他材料单列为事实来源，不得充当计算页、总结页等另一套结构来源。知识错误在对应信息位置修正，不能以事实核验为由重新组织整组。

确有用户明确批准结构变更时，另存具体变更前后映射与批准依据，逐项人工核对；当前脚本不提供宽泛豁免开关，不得篡改expected让它通过。报告此路径为“明确批准的结构变更”，不能称严格复刻检查通过。

发现旧执行状态有无依据的“已选/已确认”时，更正为待选择，保留仍有效的研究、标题及局部批准；回到A/B原图与样张展示节点。不得用已出图或正文已写完倒推授权。

## 能力边界

脚本检查登记的一致性，不能判断引用是否真实或成图是否忠于原图。agent仍须实际打开来源、核对用户消息和查看实图。此检查是Skill要求执行的前置步骤，尚未接入宿主工具调用层，不能宣称任何会话都无法跳过。
