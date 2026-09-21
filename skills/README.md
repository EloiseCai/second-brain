# 项目共享 Skills

本目录保存本项目全部自定义 Skill，是团队唯一维护源。其他 Agent 在这个项目中工作时，应先阅读项目根目录的 `agents.md`，再读取任务对应的 `skills/<skill-name>/SKILL.md` 及其 `references/`、`agents/` 等配套文件。

## 维护规则

1. 新建自定义 Skill 时，完整目录必须先写入本目录，包括 `SKILL.md` 和实际使用的配套文件。
2. 更新 Skill 时，先修改本目录中的项目版本，再将完全一致的版本同步到个人安装目录，以便 Codex 发现和运行。
3. 提交前比较项目版本与个人运行副本，确认同名 Skill 的文件内容一致，并运行 Skill 校验。
4. 项目目录已有、个人目录缺失的 Skill，需要安装运行副本；个人目录新增且属于本项目的 Skill，需要同步回本目录。
5. 项目无关的系统 Skill、插件 Skill 和第三方 Skill 不复制到本目录。

## 规则更新与运行副本部署

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

- `audience-report`：从真实用户素材库整理可追溯的痛点与受众洞察。
- `content-collector`：筛选、采集和入库内容素材。
- `content-writer`：调研确认后的内容初稿、图片与正文生产。
- `pattern-extractor`：从素材中提取标题、开头、正文、图片和视频规律。
- `product-amplify`：增强产品表达并维护产品宣传图库。
- `review`：维护发布数据与内容复盘。
- `site-review`：执行网站复盘并写入飞书知识库。
- `topic-generator`：通过两轮调研生成选题与文本方向。
