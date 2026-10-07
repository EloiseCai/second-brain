# 项目共享 Skills

本目录保存本项目全部自定义 Skill，是团队唯一维护源。其他 Agent 在这个项目中工作时，应先阅读项目根目录的 `agents.md`，再读取任务对应的 `skills/<skill-name>/SKILL.md` 及其 `references/`、`agents/` 等配套文件。

## 维护规则

1. 新建自定义 Skill 时，完整目录必须先写入本目录，包括 `SKILL.md` 和实际使用的配套文件。
2. 更新 Skill 时，先修改本目录中的项目版本，再将完全一致的版本同步到个人安装目录，以便 Codex 发现和运行。
3. 提交前比较项目版本与个人运行副本，确认同名 Skill 的文件内容一致，并运行 Skill 校验。
4. 项目目录已有、个人目录缺失的 Skill，需要安装运行副本；个人目录新增且属于本项目的 Skill，需要同步回本目录。
5. 项目无关的系统 Skill、插件 Skill 和第三方 Skill 不复制到本目录。

## 规则更新与运行副本部署

用户提出长期规则修改时，先确认适用范围为通用写作、平台还是主题专属，列出实际 Skill 名称及其文件/飞书条目；同时区分仅本篇修改。已有明确确认不重复询问，不把一次修稿自动升级为通用规则。流程梳理期间按用户要求每轮细调一个环节，展示现行要求、重复/缺口及 content-writer/references/writing-workflow.md 中同一张写作总流程图，仅更新已确认/待细调状态和当前优化位置；规则已确认与已部署分别报告。

每轮细调先列“当前实际规则、继承的旧条款、重复/冲突/缺口、拟调整项”，再接收用户补充。用户明确提出的修改可直接落实；AI新增会影响内容、数量、风格、停顿或验收范围的要求须标待确认，不得把实施完成写成用户确认。技能命名、同步和引用等实现细节可自主完成。历史条款没有本轮确认记录时标“旧规则沿用／待核对”，不能凭文件存在声称用户已逐项确认。

用户确认新规则后，由当前 agent 完成以下流程，不把同步留作用户手动操作：

1. 通读项目 `skills/<skill-name>/SKILL.md` 及受影响的引用文件，检查 Git 工作区和个人运行副本差异。保留其他 agent 的有效改动；运行副本独有的规则先核对、合并回项目，不能盲目覆盖。两个 agent 不同时编辑或部署同一 skill。
2. 将新规则融入对应章节，检查是否与现有规则冲突。通用执行要求放 `SKILL.md`，详细检查表放 `references/` 并从主文件链接；保留 `agents/` 的有效配置。一次图片纠错只能作为示例，不能变成所有笔记的固定模板。
3. 运行 skill-creator 的 `scripts/quick_validate.py` 校验项目目录，检查本地引用文件存在，并审阅本次差异。典型命令为 `python -X utf8 "$env:USERPROFILE/.codex/skills/.system/skill-creator/scripts/quick_validate.py" ./skills/content-writer`；安装位置不同时使用当前 skill-creator 实际路径。
4. 在项目根目录执行下方同步命令。同步包含整个 skill 目录，包括 `SKILL.md`、`references/`、`agents/` 和脚本；不会触碰其他 skill。脚本备份被覆盖的运行文件到临时目录，并逐文件校验 SHA256。发现运行副本独有文件时停止且不删除，先检查它是否应回收进项目或移出运行目录，再重试。
5. 再运行只读检查，并对运行目录执行同样的 skill 校验。交付时写清源目录、实际运行目录和校验结果；仅修改仓库不能称为后台已更新。
6. 当前 agent 重新读取更新后的规则；其他正在进行的任务也要在下一步执行前重新读取，已加载的会话上下文不保证自动热更新。若应用未发现新增 skill，再刷新或重开会话。

```powershell
# 部署；默认为 content-writer
./skills/sync-skill.ps1 -Name content-writer
# 只读检查，不一致时以错误退出
./skills/sync-skill.ps1 -Name content-writer -Check
```

默认运行位置为 `$CODEX_HOME/skills/<skill-name>`；未设置 `CODEX_HOME` 时使用 `$env:USERPROFILE/.codex/skills/<skill-name>`。可用 `-TargetRoot '实际运行的 skills 根目录'` 显式指定其他安装位置，必须先确认该 agent 实际读取此位置。

同机、同一运行目录的 agent 共用部署后的文件；其他电脑或不同配置目录需要先取得项目更新，再在各自机器运行同步与校验。Git 提交或拉取不会自动部署，复制文件也不会自动提交或推送 Git。按用户授权处理 Git 同步，不宣称未验证的另一台机器已更新。

回滚时先将需要恢复的规则整理回项目源文件，再执行同一同步流程；临时备份用于恢复误覆盖文件，不成为第二个长期维护源。同步失败时保留具体错误，修复后重新校验，不继续使用“已更新”的状态。

## 当前项目 Skills

- `research-core`：通用写作调研入口、证据标准与职责交接。
- `pregnabite-research`：妈妈善食研究范围、检索种子、产品筛选和洞察位置；与写作主题包共享事实引用。

- `writing-router`：跨平台、账号与载体入口，恢复飞书断点并隔离平台要求。
- `wechat-writing`：公众号知识型长文固定分支，WX1—WX8及断点放行；正文先行、按正文配图，制作与发布分别记录。

- `audience-report`：通过六维组合、短关键词及指数、热门笔记、真实反馈和同类孕妈 App／小程序研究，维护具体问题、困惑、情绪与解决方案机会。
- `content-collector`：筛选、采集和入库内容素材。
- `content-writer`：调研确认后的内容初稿、图片与正文生产；引用统一的对标分析与标题规则。
- `writing-core`：通用表达、实际场景、评论转化和逐模块 critique。
- `xiaohongshu-writing`：小红书平台写作适配与规则引用。
- `pregnabite-writing`：妈妈善食主题包，引用飞书洞察、写作原则和产品资料。
- `image-copy-writer`：图片预设文本写作与三部分组合审查。
- `cover-generator`：获批封面候选的生成与实图验收。
- `image-generator`：选定方案内页的生成与实图验收。
- `pinned-comment-writer`：评论承接对标调研入库、逐句映射写作与审查；小红书 Hashtag 后调用。
- `hashtag-writer`：同主题对标选源、固定10个标签及逐项核验。
- `body-writer`：发布正文、图文分工及文末提问设计。
- `title-writer`：发布标题、封面标题、内页标题及小标题的共用写作和 critique；按角色引用平台及主题要求。
- `pattern-extractor`：统一执行“对标分析”（需求、形式、标题图片正文、核验、借鉴 critique 与洞察回写交接）；跨篇提炼规律，维护封面点击机制与本账号CTR反馈。
- `product-amplify`：增强产品表达并维护产品宣传图库。
- `review`：维护发布数据与内容复盘。
- `site-review`：执行网站复盘并写入飞书知识库。
- `topic-generator`：承接人群问题与情绪研究，通过两轮调研生成多角度选题、文本方向及功能验证计划。

## 当前研究与反馈链路

### 整包安装与可移植状态

`writing-pack.json` 列出当前套件版本与依赖。取得完整 `skills/` 目录后，在 PowerShell 执行：

```powershell
./skills/install-writing-pack.ps1
./skills/install-writing-pack.ps1 -Check
```

支持 `-TargetRoot` 指向实际运行目录。安装复用 sync-skill.ps1 的备份与 SHA256 校验；某包失败即停止，此前成功的包可能已部署，修复后重新校验。安装不包含第三方工具、飞书权限和账号数据，不自动提交或推送。新会话从 writing-router 开始。

当前规则已持久化；公众号流程已按2026-10-07确认固定，实际发布端验证单独记录；旧研究模块仍有账号专属内容，跨账号需继续绑定和迁移，不能称任意主题开箱即用。其他电脑可以安装当前完整目录副本；通过 Git 获取之前必须确认新增文件已提交、推送。相同规则不保证模型逐字生成相同文本。

### 既有研究链路

PregnaBite于2026-09-24确认以孕妈各类问题为探索范围：audience-report六维选项列举与组合假设、搜索双向取证、问题ID与方案ID → topic-generator匹配解决方案并展开不同角度 → content-writer按已确认方向生产 → review结合实际封面与数据复盘 → audience-report按问题＋角度＋方案回填多篇表现统计（单篇诊断与优化留在review），同时pattern-extractor维护封面规律与验证记录。所有人群研究统一归纳进固定飞书《用户洞察》，用户审核与外部证据分开保留。功能尚未存在时可以先验证问题和方案，不能宣传为已上线能力。当前优先完善前期调研，封面实验留作后续执行；18%为用户确认的官方CTR中位数及本账号优化目标。
