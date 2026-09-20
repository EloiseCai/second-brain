$ErrorActionPreference='Stop'
$doc='VKB1dMwh8ou6APxpUDkcOKSDnbf'
$content=lark-cli docs +fetch --doc $doc --as user --detail full --jq '.data.document.content'
[xml]$xml='<root>'+($content -join "`n")+'</root>'
$nodes=@($xml.root.ChildNodes)
function Replace-Node($node,$value){
 $file=Join-Path $PSScriptRoot '008_B写入片段.xml'
 [IO.File]::WriteAllText($file,$value,[Text.UTF8Encoding]::new($false))
 $rel=Resolve-Path -LiteralPath $file -Relative
 $r=lark-cli docs +update --doc $doc --as user --command block_replace --block-id $node.id --content ('@'+$rel) | ConvertFrom-Json
 if($r.data.result -ne 'success'){throw ($r|ConvertTo-Json -Depth 8)}
}
foreach($node in $nodes){
 $t=$node.InnerText
 if($t.StartsWith('当前阶段：') -or $t.StartsWith('当前状态：')){Replace-Node $node '<p>当前状态：用户已选B｜B44单品配方组。标题“孕期早餐喝什么？6款豆浆换着喝🥛”保持。整组7页：本次已生成封面1张，等待封面审阅；6张内页与正式正文尚未生成。</p>'}
 elseif($t -eq 'A｜B43 整餐搭配组（推荐）'){Replace-Node $node '<h3>A｜B43 整餐搭配组（未选）</h3>'}
 elseif($t -eq 'B｜B44 单品配方组'){Replace-Node $node '<h3>B｜B44 单品配方组（已选）</h3>'}
 elseif($t.StartsWith('本阶段通过项：')){Replace-Node $node '<p>本阶段复核：B44整组7页已核验并由用户选定；本篇六款配方已重新组合。封面逐项检查主标题、01—06顺序、配料克数、水量、杯碗差异、两列三行布局，无遗漏或明显错字。实际文件1086×1448、RGB、3:4。仅封面完成；6张内页、正文及整篇审查仍待完成，不判定整组已交付。完整逐页内容与检查清单保存在制作材料/008_B44_整组制作清单.md。</p>'}
}
$file=Join-Path $PSScriptRoot '008_B封面锚点.xml'
[IO.File]::WriteAllText($file,'<h3>封面审阅｜B44</h3><p>有效封面：6款孕期早餐豆浆。参考B44第01张，保留红色标题、花叶边角、编号卡片与杯碗层次；浅盘按已选方案改为可盛豆浆的同色深碗。整组应交付7张，当前仅封面待审阅。</p>',[Text.UTF8Encoding]::new($false))
$rel=Resolve-Path -LiteralPath $file -Relative
$anchor=($nodes|Where-Object {$_.InnerText.StartsWith('已选标题保持：')})[0].id
$r=lark-cli docs +update --doc $doc --as user --command block_insert_after --block-id $anchor --content ('@'+$rel) | ConvertFrom-Json
if($r.data.result -ne 'success'){throw ($r|ConvertTo-Json -Depth 8)}
lark-cli docs +media-insert --doc $doc --as user --file './05_内容草稿/008_孕期豆浆怎么搭/制作材料/008_B44_01_封面.png' --width 1080 --height 1440
lark-cli docs +fetch --doc $doc --as user --detail full --jq '.data.document.content' | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot '008_B封面写入后.xml')
