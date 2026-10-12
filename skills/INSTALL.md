# 安装与启动

下载发布的统一 ZIP，完整解压；也可从仓库获取最新 skills 目录。私有 GitHub 仓库需要访问权限；也可以由维护者下载 ZIP 后内部发送。

Windows 使用 PowerShell；其他系统需要 PowerShell 7（pwsh）。在解压目录运行：

```powershell
./skills/install-writing-pack.ps1
./skills/install-writing-pack.ps1 -Check
```

若运行环境限制脚本，交给当地 IT 按公司策略处理。自定义 Codex 路径可传 `-TargetRoot`。安装器保留有差异的旧文件备份；发现运行目录独有文件会停止，先核对，不能直接删除个人改动。新会话可让 Codex 执行上述安装，不需要自己逐个复制 Skill。

安装后新开会话输入：

> 使用 writing-router，读取当前分支就绪状态，告诉我当前可用的写作流程，再询问是否开始。

入口显示实际版本及开放平台。之后输入“开始，给妈妈善食写一篇小红书图文”，或指定具体选题。可用分支读取 `writing-router/references/routes.json`：目前小红书图文和公众号长文 ready，其他载体施工中。

首次需要：当前员工自己的飞书 CLI 授权及 lark 工具 Skill、知识库访问权限、可用浏览器研究工具、图片生成工具、当前电脑图片归档目录。工具/权限不随包复制。复用团队已经确认的账号资料和规范；不把维护者电脑的绝对路径当成员工路径。缺少依赖时列出缺口，不能以安装成功声称笔记生产成功。

每篇仍执行研究、方案选择、图片文字审批、逐模块 critique 与最终验收。生成的文章和图片存入工作间；不会自动发布平台。

升级：拉取团队仓库更新或下载最新 ZIP，重新安装与 Check；新会话重新读取 router。新分支标记 ready 并同步后即可使用，不需要另外解锁。版本规则一致不保证生成文字逐字相同。

## WorkBuddy等其他宿主

写作流程通过writing-router加载完整Skill依赖，并读取初始化保存的账号资料与工具配置，不依赖仓库根目录agents.md。先在目标宿主确认实际支持的Skill导入方式和目录，再完整导入本套件；不要只复制writing-router一个目录。

现有PowerShell安装脚本默认目标是Codex。用于其他宿主时，必须显式传入已经确认的Skill目录：`./skills/install-writing-pack.ps1 -TargetRoot '实际目录'`，随后用相同TargetRoot加`-Check`。不要猜WorkBuddy目录。目标工具支持何种格式、能否发现Skills及工具能否调用，需在员工环境验证；本包的文件同步校验不代表已完成WorkBuddy实跑。

首次运行由workspace-initializer询问或发现该使用者的知识库父位置、定位总览、写作原则及飞书连接配置，完成本机授权验证；已有团队配置可复用，个人授权重新确认。凭据与登录态不随包分发。
