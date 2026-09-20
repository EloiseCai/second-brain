$ErrorActionPreference = 'Stop'
$dir = Join-Path $PSScriptRoot '008_写入片段'
New-Item -ItemType Directory -Force -Path $dir | Out-Null
$doc = 'VKB1dMwh8ou6APxpUDkcOKSDnbf'
$updates = @(
@('doxcn4tK3Dz8w23i0JImf4NyG6Y','<p>当前阶段：用户已选A｜B05配方卡整组和标题1“孕期早餐喝什么？6款豆浆换着喝🥛”。封面已生成，待用户审阅；整组基准7张（1封面＋6内页），内页及正式正文尚未生成。</p>'),
@('doxcn1UlmlqrPEM9FFshoC51S0c','<p><b>已选标题：</b>孕期早餐喝什么？6款豆浆换着喝🥛</p><p><b>已选模板：</b>A｜B05配方卡整组。当前有效内容采用下表A五项配料，B方案仅保留为未选调研记录，不参与生成。</p><h3>封面审阅</h3><p>01｜6款孕期早餐豆浆。对应B05_01原帖封面；当前只交封面，02—07待封面确认后生成。</p>'),
@('doxcn5xQLI3oQg5wzzguNoD4RUd','<h3>图片模板选择记录（A已选，B未选）</h3>'),
@('doxcngfRdn3UoGkBU6RJyCvmOyg','<p>当前有效整组：01封面＋02—07六款配方卡，全部对应B05原组同页码。只执行下表A五项配料；B三项方案未选，不作为当前配方。每款是编辑根据食材改拟的制作起点，未经厨房实测，不写亲测或保证口感；不是孕妇每日规定量。</p>'),
@('doxcnXRHKnq49Rjnzp5ek4d78Ye','<p>封面阶段critique：原图与成图均为六格，主标题保留“孕期、早餐、六款豆浆”；六格名称与A配方一一对应，原热量标签改为“加水500mL”，不新增文字层级。第一轮退回：左上大米重复、画幅偏长；第二轮已去掉重复米堆，实测1086×1448、RGB无透明。未采用原图养颜等功效，读者文字未发现需修改的违禁词或导流项。当前只验收封面；内页和正文仍待完成。</p>'),
@('doxcn4OeML7V7zpNt0KMrczuJTd','<p>生产记录：封面生成2轮，第一轮退回，第二轮为当前有效图。文件：制作材料/008_01_封面.png；完整提示词和修正提示词保存在008_封面提示词.txt、008_封面修正提示词.txt；七页上图文案和范围基准保存在008_A生成清单.md。已选A，无A/B发布实验结论。未补造工时，未启动定时任务。</p>'),
@('doxcn6NvFK2HJH8RiGyTzEvgZze','<p>当前停止点：标题1和A模板已选。等待用户审阅封面；通过后按B05_02—07对应生成六张内页，再进行正文写作。</p>')
)
for($i=0;$i -lt $updates.Count;$i++) {
  $file=Join-Path $dir ($i.ToString()+'.xml')
  [IO.File]::WriteAllText($file,$updates[$i][1],[Text.UTF8Encoding]::new($false))
  $relative=Resolve-Path -LiteralPath $file -Relative
  $result=lark-cli docs +update --doc $doc --as user --command block_replace --block-id $updates[$i][0] --content ('@'+$relative) | ConvertFrom-Json
  if($result.data.result -ne 'success'){throw ($result | ConvertTo-Json -Depth 10)}
  Write-Output ('Updated '+$updates[$i][0])
}
lark-cli docs +update --doc $doc --as user --command str_replace --pattern '用水500mL' --content '加水500mL'
