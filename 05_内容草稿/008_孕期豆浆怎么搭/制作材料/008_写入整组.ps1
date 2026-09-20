$ErrorActionPreference='Stop'
$doc='VKB1dMwh8ou6APxpUDkcOKSDnbf'
[xml]$xml='<root>'+((Get-Content -LiteralPath (Join-Path $PSScriptRoot '008_整组写入前.xml')) -join "`n")+'</root>'
$nodes=@($xml.root.ChildNodes)
function ReplaceNode($node,$value){
 $f=Join-Path $PSScriptRoot '008_整组片段.xml'
 [IO.File]::WriteAllText($f,$value,[Text.UTF8Encoding]::new($false))
 $rel=Resolve-Path -LiteralPath $f -Relative
 $r=lark-cli docs +update --doc $doc --as user --command block_replace --block-id $node.GetAttribute('id') --content ('@'+$rel)|ConvertFrom-Json
 if($r.data.result -ne 'success'){throw ($r|ConvertTo-Json -Depth 8)}
}
foreach($node in $nodes){
 if($node.InnerText.StartsWith('当前状态：')){ReplaceNode $node '<p>当前状态：B44整组图片已生成7张，封面六个名称按用户要求放大约15%。01为总览，02—07依次为黄豆燕麦、玉米小米、山药莲子、花生黑米、南瓜腰果、黑芝麻核桃。正式正文尚未写作。</p>'}
 elseif($node.InnerText -eq '封面审阅｜B44'){ReplaceNode $node '<h3>整组图片｜B44（7张）</h3>'}
 elseif($node.InnerText.StartsWith('有效封面：')){ReplaceNode $node '<p>有效图片顺序：封面＋六张单品配方页。封面保留已认可设计，仅六个配方名称放大约15%；内页逐一参考B44对应原图，保留食材栏、不同步骤格数和器皿。下方7张为当前有效成图。</p>'}
 elseif($node.InnerText.StartsWith('本阶段复核：')){ReplaceNode $node '<p>本阶段复核：7张均已实际查看，六款名称、顺序和克数一致；内页原料条目3、4、5、4、4、4，步骤格数3、3、4、3、5、4，与B44逐页对应。06按原内页使用瓷碗。配方均写明完整加热豆浆程序；无功效保证、亲测声明或导流。配方为未厨房实测的编辑起点，图片为示意。正文和整篇发布审查尚未完成。</p>'}
}
$c=lark-cli docs +fetch --doc $doc --as user --detail full --jq '.data.document.content'
[xml]$fresh='<root>'+($c -join "`n")+'</root>'
$anchor=@($fresh.root.ChildNodes|Where-Object {$_.InnerText.StartsWith('有效图片顺序：')})[0].GetAttribute('id')
$names=@('008_B44_01_封面_标题放大.png','008_B44_02_黄豆燕麦豆浆.png','008_B44_03_玉米小米豆浆.png','008_B44_04_山药莲子豆浆.png','008_B44_05_花生黑米豆浆.png','008_B44_06_南瓜腰果豆浆.png','008_B44_07_黑芝麻核桃豆浆.png')
$records=@()
foreach($name in $names){
 $rel=Resolve-Path -LiteralPath (Join-Path $PSScriptRoot $name) -Relative
 $r=lark-cli docs +media-insert --doc $doc --as user --file $rel --width 1080 --height 1440 | ConvertFrom-Json
 if(-not $r.ok -or -not $r.data.block_id){throw ($r|ConvertTo-Json -Depth 8)}
 $id=$r.data.block_id
 $m=lark-cli docs +update --doc $doc --as user --command block_move_after --block-id $anchor --src-block-ids $id | ConvertFrom-Json
 if($m.data.result -ne 'success'){throw ($m|ConvertTo-Json -Depth 8)}
 $records+=@{file=$name;block_id=$id;token=$r.data.file_token}
 $records|ConvertTo-Json -Depth 8|Set-Content -Encoding utf8 (Join-Path $PSScriptRoot '008_整组交付记录.json')
 $anchor=$id
 Write-Output ('Saved '+$name)
}
$r=lark-cli docs +update --doc $doc --as user --command block_delete --block-id doxcnkMhcCZpFpv6y6MFU8fctZe | ConvertFrom-Json
if($r.data.result -ne 'success'){throw ($r|ConvertTo-Json -Depth 8)}
lark-cli docs +fetch --doc $doc --as user --detail full --jq '.data.document.content' | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot '008_整组写入后.xml')

