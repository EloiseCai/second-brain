# 研究与维护边界

所有用户洞察写入与模块完成前的增量处理统一执行 [audience-report写入关口](../../audience-report/references/writeback-gate.md)，重新读取最新分析与写作规则；各模块不维护独立洞察模板。

所有模块通用方法由各自Skill维护，主题包唯一绑定业务资料。topic-radar维护热点，audience-report维护洞察，topic-generator做两轮选题研究。内容策划读取主题包和研究交接，正式生产再适配平台规则。

对标库维护为独立任务：content-collector → pattern-extractor。单篇第二轮重在验证题意和寻找相近参考，优先复用库内原文/分析；只有实际采用的库外材料才做必要补录。批量扩库或跨篇规律汇总不自动触发。小红书至少新增1篇继续保留，调用content-collector定向采集，不自动触发pattern-extractor。
