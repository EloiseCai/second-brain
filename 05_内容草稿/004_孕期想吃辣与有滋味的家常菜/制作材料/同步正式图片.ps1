$ErrorActionPreference='Stop'
$dir004='05_内容草稿/004_孕期想吃辣与有滋味的家常菜/制作材料'
[xml]$old004='<root>'+(Get-Content -LiteralPath "$dir004/内容页同步前.xml" -Raw)+'</root>'
$images004=@(Get-Content -LiteralPath "$dir004/正式图片飞书资源.json" -Raw | ConvertFrom-Json)
$content004=Get-Content -LiteralPath "$dir004/完整图片章节模板.xml" -Raw
for($i004=0;$i004 -lt $images004.Count;$i004++){
$tag004='<img src="'+$images004[$i004].file_token+'" width="543" height="724" name="'+$images004[$i004].name+'"/>'
$content004=$content004.Replace('{{IMAGE'+$i004+'}}',$tag004)
}
$content004 | Set-Content -LiteralPath "$dir004/完整图片章节.xml" -Encoding utf8
$head004=$old004.root.SelectSingleNode('h2[text()="图片方案与完整提示词"]')
$remove004=@()
$node004=$head004.NextSibling
while($null -ne $node004){
if($node004.Name -eq 'h2'){break}
if($node004.id){$remove004+=$node004.id}
$node004=$node004.NextSibling
}
$update004=lark-cli docs +update --doc EVwxdQk5IoQ0hOxsiAKchBUsn3d --command block_replace --block-id $head004.id --content "@$dir004/完整图片章节.xml" --as user | ConvertFrom-Json
if(-not $update004.ok){throw ($update004|ConvertTo-Json -Depth 5)}
Write-Output 'New production section written'
$remove004+=@($images004|ForEach-Object{$_.block_id})
$delete004=lark-cli docs +update --doc EVwxdQk5IoQ0hOxsiAKchBUsn3d --command block_delete --block-id ($remove004 -join ',') --as user | ConvertFrom-Json
if(-not $delete004.ok){throw ($delete004|ConvertTo-Json -Depth 5)}
Write-Output 'Superseded production blocks removed'
$title004=$old004.root.SelectSingleNode('h3[text()="标题候选"]').NextSibling
$titles004='<ol><li>孕期想吃辣？6道家常菜附做法🌶️</li><li>孕期吃点有滋味的｜6道菜照着做🍚</li><li>小米椒能吃吗？孕期家常菜这样做🌶️</li></ol>'
$r004=lark-cli docs +update --doc EVwxdQk5IoQ0hOxsiAKchBUsn3d --command block_replace --block-id $title004.id --content $titles004 --as user | ConvertFrom-Json
if(-not $r004.ok){throw 'title update failed'}
$stage004=$old004.root.SelectSingleNode('p[b="阶段说明："]')
$r004=lark-cli docs +update --doc EVwxdQk5IoQ0hOxsiAKchBUsn3d --command block_replace --block-id $stage004.id --content '<p><b>阶段说明：</b>已按用户选定A完成7张图片与3个标题候选。待选定标题后，按图中6道菜和具体做法核对并写正文。下方现有正文保留待处理，不计作本轮完成稿；旧制作备注中的“两道菜”等描述也待正文阶段同步。</p>' --as user | ConvertFrom-Json
if(-not $r004.ok){throw 'stage update failed'}
$check004=lark-cli docs +fetch --doc EVwxdQk5IoQ0hOxsiAKchBUsn3d --detail full --as user | ConvertFrom-Json
if(-not $check004.ok){throw 'verification failed'}
$check004.data.document.content|Set-Content -LiteralPath "$dir004/飞书当前全文.xml" -Encoding utf8
[xml]$v004='<root>'+$check004.data.document.content+'</root>'
[pscustomobject]@{Images=$v004.SelectNodes('//img').Count;TitleCandidates=$v004.root.SelectSingleNode('h3[text()="标题候选"]').NextSibling.InnerText;ProductionSections=$v004.SelectNodes('//h2[text()="图片方案与完整提示词"]').Count}

