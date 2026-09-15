$ErrorActionPreference='Stop'
$dir='05_内容草稿/004_孕期想吃辣与有滋味的家常菜/制作材料'
[xml]$original='<root>'+(Get-Content -LiteralPath "$dir/正文前全文.txt" -Raw)+'</root>'
function Update004($args004){
 $result004=& lark-cli @args004 --as user | ConvertFrom-Json
 if(-not $result004.ok){throw ($result004|ConvertTo-Json -Depth 5)}
}
function ReplaceSection004($heading,$file,$boundary){
 $ids004=@()
 $node004=$heading.NextSibling
 while($node004 -and $node004.Name -notin $boundary){
  if($node004.id){$ids004+=$node004.id}
  elseif($node004.Name -in @('ul','ol')){$ids004+=@($node004.ChildNodes | ForEach-Object{$_.id})}
  $node004=$node004.NextSibling
 }
 Update004 @('docs','+update','--doc','EVwxdQk5IoQ0hOxsiAKchBUsn3d','--command','block_replace','--block-id',$heading.id,'--content',"@$dir/$file")
 if($ids004.Count){Update004 @('docs','+update','--doc','EVwxdQk5IoQ0hOxsiAKchBUsn3d','--command','block_delete','--block-id',($ids004 -join ','))}
}
ReplaceSection004 $original.root.SelectSingleNode('h3[text()="正文"]') '当前正文.xml' @('h2','h3')
Write-Output 'Body synchronized'
ReplaceSection004 $original.root.SelectSingleNode('h2[text()="制作备注"]') '当前制作备注.xml' @('h2')
Write-Output 'Production notes synchronized'
'<h3>已选标题</h3><p>小米椒能吃吗？孕期家常菜这样做🌶️</p>' | Set-Content -LiteralPath "$dir/已选标题.xml" -Encoding utf8
ReplaceSection004 $original.root.SelectSingleNode('h3[text()="标题候选"]') '已选标题.xml' @('h2','h3')
Update004 @('docs','+update','--doc','EVwxdQk5IoQ0hOxsiAKchBUsn3d','--command','str_replace','--pattern','已按用户选定A完成7张图片与3个标题候选。待选定标题后，按图中6道菜和做法核对并写正文。下方正文及旧制作备注保留待处理，不计作本轮完成稿；旧备注中的两道菜等描述在正文阶段同步。','--content','用户已选A及标题3，7张图片和标题完成后，已按图中六道菜写正文并同步制作备注。当前为待用户修改的AI初稿；标题无需重选，未代填最终发布稿。')
Update004 @('docs','+update','--doc','EVwxdQk5IoQ0hOxsiAKchBUsn3d','--command','str_replace','--pattern','待选定标题后再写正文。','--content','标题3已确认，正文已按图2—7完成，等待用户修改。')
Update004 @('docs','+update','--doc','EVwxdQk5IoQ0hOxsiAKchBUsn3d','--command','str_replace','--pattern','两道有滋味的菜与做法','--content','六道有滋味的菜与做法')
$final004=lark-cli docs +fetch --doc EVwxdQk5IoQ0hOxsiAKchBUsn3d --detail full --as user | ConvertFrom-Json
if(-not $final004.ok){throw 'fetch failed'}
$final004.data.document.content|Set-Content -LiteralPath "$dir/飞书当前全文.xml" -Encoding utf8
[xml]$check004='<root>'+$final004.data.document.content+'</root>'
[pscustomobject]@{Images=$check004.SelectNodes('//img').Count;AISections=$check004.SelectNodes('//h2[text()="AI初稿"]').Count;BodySections=$check004.SelectNodes('//h3[text()="正文"]').Count;FinalSections=$check004.SelectNodes('//h2[text()="最终发布稿"]').Count;Title=$check004.root.SelectSingleNode('h3[text()="已选标题"]').NextSibling.InnerText}
$body004=$check004.root.SelectSingleNode('h3[text()="正文"]').NextSibling
while($body004 -and $body004.Name -ne 'h2'){Write-Output $body004.InnerText; $body004=$body004.NextSibling}

