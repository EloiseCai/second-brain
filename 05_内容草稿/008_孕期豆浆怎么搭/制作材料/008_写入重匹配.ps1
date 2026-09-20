$ErrorActionPreference='Stop'
$doc='VKB1dMwh8ou6APxpUDkcOKSDnbf'
$content=lark-cli docs +fetch --doc $doc --as user --detail full --jq '.data.document.content'
[xml]$xml='<root>'+($content -join "`n")+'</root>'
$nodes=@($xml.root.ChildNodes)
$start=-1; $end=-1
for($i=0;$i -lt $nodes.Count;$i++) { if($nodes[$i].Name -eq 'h2' -and $nodes[$i].InnerText -eq 'AI初稿'){$start=$i}; if($start -ge 0 -and $i -gt $start -and $nodes[$i].Name -eq 'h2'){$end=$i;break} }
if($start -lt 0 -or $end -lt 0){throw 'AI初稿 boundaries missing'}
$remove=@()
for($i=$start+1;$i -lt $end;$i++){if($nodes[$i].id){$remove+=$nodes[$i].id}else{foreach($child in $nodes[$i].ChildNodes){if($child.id){$remove+=$child.id}}}}
$plan=Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '008_重新匹配.xml') -Relative
$r=lark-cli docs +update --doc $doc --as user --command block_insert_after --block-id $nodes[$start].id --content ('@'+$plan) | ConvertFrom-Json
if($r.data.result -ne 'success'){throw ($r|ConvertTo-Json -Depth 8)}
$r=lark-cli docs +update --doc $doc --as user --command block_delete --block-id ($remove -join ',') | ConvertFrom-Json
if($r.data.result -ne 'success'){throw ($r|ConvertTo-Json -Depth 8)}
$status='<p>当前阶段：已选标题“孕期早餐喝什么？6款豆浆换着喝🥛”保持。B05封面因内容与原帖过近已退回；六款内容已重做，当前待选A｜B43整餐搭配组或B｜B44单品配方组，均为7页。未生成新图片或正文。</p>'
$file=Join-Path $PSScriptRoot '008_当前状态.xml'
[IO.File]::WriteAllText($file,$status,[Text.UTF8Encoding]::new($false))
$relative=Resolve-Path -LiteralPath $file -Relative
foreach($node in $nodes){if($node.Name -eq 'p' -and ($node.InnerText.StartsWith('当前阶段：') -or $node.InnerText.StartsWith('当前停止点：'))){$r=lark-cli docs +update --doc $doc --as user --command block_replace --block-id $node.id --content ('@'+$relative) | ConvertFrom-Json; if($r.data.result -ne 'success'){throw ($r|ConvertTo-Json -Depth 8)}}}
lark-cli docs +update --doc $doc --as user --command str_replace --pattern '第二轮对标调研' --content '前期调研依据（保留来源，配方以AI初稿为准）'
lark-cli docs +fetch --doc $doc --as user --detail full --jq '.data.document.content' | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot '008_重匹配写入后.xml')
Write-Output 'Replaced AI初稿; retained source research; old cover removed from active document.'
