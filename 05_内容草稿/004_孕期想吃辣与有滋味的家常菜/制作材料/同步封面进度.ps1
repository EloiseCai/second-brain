$ErrorActionPreference='Stop'
$folder='05_内容草稿/004_孕期想吃辣与有滋味的家常菜/制作材料'
[xml]$doc='<root>'+(Get-Content -LiteralPath "$folder/飞书修改前.xml" -Raw)+'</root>'
function ReplaceBlock($node,$content) {
  $content | Set-Content -LiteralPath "$folder/本次写入.xml" -Encoding utf8
  $res=lark-cli docs +update --doc EVwxdQk5IoQ0hOxsiAKchBUsn3d --command block_replace --block-id $node.id --content "@$folder/本次写入.xml" --as user | ConvertFrom-Json
  if(-not $res.ok){throw ($res|ConvertTo-Json -Depth 6)}
  Write-Output ('Updated '+$node.id)
}
$a=$doc.root.SelectSingleNode('h3[contains(text(),"封面候选 A")]')
$b=$doc.root.SelectSingleNode('h3[contains(text(),"封面候选 B")]')
ReplaceBlock $a.NextSibling '<p><b>具体对标与容量：</b>PregnaBite相关 → 02_内容素材 → B类 图文 → B类-一日餐次搭配 → B类43 → 笔记图片第1张。已看实际原图，真实结构为米色底、深棕宋体大标题、一行副标题、两列三行六盘菜，每盘下方菜名及热量；没有食材栏或步骤图。本篇保留6盘和两级标题，菜名下不写热量。以小米椒牛肉为入口，配咖喱、酸鲜、蒜香和菌香选择；不将所有菜称为辣菜。</p>'
ReplaceBlock $a.NextSibling.NextSibling (Get-Content -LiteralPath "$folder/A_prompt.xml" -Raw)
ReplaceBlock $a '<h3>封面候选 A｜米色六盘菜合集</h3>'
ReplaceBlock $b.NextSibling '<p><b>具体对标与容量：</b>PregnaBite相关 → 02_内容素材 → B类 图文 → B类-营养目标型食谱 → B类01 → 笔记图片第1张。已看实际原图：粉色外框、白底、左侧洋红主标题与右侧紫色两行主题、横线、3×3白碗菜品、紫色菜名和黑色标签。本篇保留9碗、每碗5—7字菜名及2字口味标签；营养标签改为香辣、浓香、酸鲜等口味信息，删除版权水印。主标题“想吃有滋味的”，右侧“孕期／食谱🌶️”。</p>'
ReplaceBlock $b.NextSibling.NextSibling (Get-Content -LiteralPath "$folder/B_prompt.xml" -Raw)
$pause=$doc.root.SelectSingleNode('p[b="暂停点："]')
ReplaceBlock $pause '<p><b>当前阶段（2026-09-14）：</b>A/B两张候选封面已用内置imagegen生成，均为1086×1448、3:4竖版RGB不透明PNG，已检查文字、菜名和布局。文件归档于05_内容草稿/004_孕期想吃辣与有滋味的家常菜/：01A_六道家常菜封面.png、01B_九道家常菜封面.png；完整提示词与原图在制作材料。等待用户选定A或B，再复核并生成内容页、完成标题，最后写正文。现有正文保留待图片和标题定稿后重新核对，不算正文阶段已完成。当前内容页方案及锁定表均为待复核规划，第2页原图结构对应、各页容量和全组风格尚未锁定。</p>'
$ai=$doc.root.SelectSingleNode('h2[text()="AI初稿"]')
$res=lark-cli docs +update --doc EVwxdQk5IoQ0hOxsiAKchBUsn3d --command block_insert_after --block-id $ai.id --content '<p><b>阶段说明：</b>用户已确认执行顺序：先完成图片和标题，再写正文。本节已有文字保留待核对，不作为本轮完成稿，不反向决定图片方案。</p>' --as user | ConvertFrom-Json
if(-not $res.ok){throw 'status insertion failed'}

