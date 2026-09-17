# 项目共享 Skills

本目录保存本项目全部自定义 Skill，是团队唯一维护源。其他 Agent 在这个项目中工作时，应先阅读项目根目录的 `agents.md`，再读取任务对应的 `skills/<skill-name>/SKILL.md` 及其 `references/`、`agents/` 等配套文件。

## 维护规则

1. 新建自定义 Skill 时，完整目录必须先写入本目录，包括 `SKILL.md` 和实际使用的配套文件。
2. 更新 Skill 时，先修改本目录中的项目版本，再将完全一致的版本同步到个人安装目录，以便 Codex 发现和运行。
3. 提交前比较项目版本与个人运行副本，确认同名 Skill 的文件内容一致，并运行 Skill 校验。
4. 项目目录已有、个人目录缺失的 Skill，需要安装运行副本；个人目录新增且属于本项目的 Skill，需要同步回本目录。
5. 项目无关的系统 Skill、插件 Skill 和第三方 Skill 不复制到本目录。

## 当前项目 Skills

- `content-collector`：筛选、采集和入库内容素材。
- `content-writer`：调研确认后的内容初稿、图片与正文生产。
- `pattern-extractor`：从素材中提取标题、开头、正文、图片和视频规律。
- `product-amplify`：增强产品表达并维护产品宣传图库。
- `review`：维护发布数据与内容复盘。
- `site-review`：执行网站复盘并写入飞书知识库。
- `topic-generator`：通过两轮调研生成选题与文本方向。
