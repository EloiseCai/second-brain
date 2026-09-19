from pathlib import Path
import xml.etree.ElementTree as ET
import subprocess,shutil
base=Path(__file__).parent
root=ET.fromstring('<root>'+ (base/'007_整理前快照.xml').read_text(encoding='utf-8-sig')+'</root>')
nodes=list(root)
start=next(i for i,n in enumerate(nodes) if n.get('id')=='doxcnLUW2ns5vigjYlq1xBJEnng')
end=next(i for i,n in enumerate(nodes) if n.get('id')=='doxcnGrKoCBg4tlCBewKPInxg3b')
ids=[n.get('id') for n in nodes[start+1:end]]
cli=shutil.which('lark-cli')
def run(args):
 p=subprocess.run([cli,'docs','+update','--doc','USJQd7Cjvok9erxm6quc85X6nle','--as','user']+args,capture_output=True,text=True,encoding='utf-8')
 print(p.stdout)
 if p.returncode: raise RuntimeError(p.stderr)
# 规划区已成功整理；只执行尚未成功的状态段落替换。
updates={
'doxcnXQpZhIkHoZNQlecsrR0rhh':'未选候选A（B02），仅保留选择记录，不属于当前成稿。',
'doxcnYgzlemqiHwDaorujMy91rf':'当前有效第1张：用户已选B07封面，保持不变。整组共4张，另有早餐与加餐、午晚餐、食材与标签三张内页。',
'doxcnKqZgPcma3Y2GnmgNkcZfqd':'已失效的两页方案内页：重复16菜加配餐，整组展开不足。本图仅保留复盘，不计入当前四张成稿。',
'doxcnU9PERyYaLtjVD7ml7dOfYb':'当前阶段：已选B07封面与发布标题。critique规则已回写项目并同步运行副本；按四页方案生成并验收剩余三页，正文尚未写作。',
'doxcnoht4xbQ4sIGJ1fi8UCGvWf':'标题1已选：孕期人群＋补钙主题＋三餐搭配收藏收益。当前B07四页将餐次例子与标签核对结合，标题保留。',
'doxcnSp2knivf8Op0gwyPttzkmc':'标题及模板选择已完成：使用标题1、候选B（B07）。不再等待重选；critique先核对整组信息，再审每页实际内容。'
}
for k,v in updates.items():
 f=base/('状态_'+k+'.xml')
 f.write_text('<p>'+v+'</p>',encoding='utf-8')
 run(['--command','block_replace','--block-id',k,'--content','@'+str(f.relative_to(Path.cwd()))])
