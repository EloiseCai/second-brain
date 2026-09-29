import json,subprocess,time
D='YPvUdn51wokFjjx7vjmcQIIonkb';p=f'/open-apis/docx/v1/documents/{D}/blocks/'
def api(m,x,d=None):
 c=['lark-cli','api',m,x,'--as','user'];
 if d:c+=['--data',json.dumps(d,ensure_ascii=False)]
 for a in range(4):
  r=json.loads(subprocess.check_output(c))
  if r.get('ok'):return r['data']['block'] if m=='GET' else r['data']
  if a==3:raise RuntimeError(r)
  time.sleep(2**a)
def patch(bid,parts):
 b=api('GET',p+bid);els=b['text']['elements'];assert len(els)==len(parts),(bid,els)
 for e,v in zip(els,parts):e['text_run']['content']=v
 api('PATCH',p+bid,{'update_text_elements':{'elements':els}});time.sleep(.36)
changes={
'doxcn7lhOvmtHhCtUMtiKmqcMdb':['2014/10=','201'],
'doxcntzXqi9PrvIfqWQDmNegbOd':['11%'],
'doxcnuOeQfUnhbOUAhX5mNNuTgh':['19秒'],
'doxcnJ1K0Q9O47MnwBESYSUkTKh':['7赞/0评/1藏/0分享'],
'doxcnkHx93I7hJNWpQsVmhku8Cg':['涨粉1'],
'doxcniTL2I73SS2HjGe8s0C7035':['1238/11=','113'],
'doxcnda8aRXcTnGXM5ddQNuz48X':['5.7%'],
'doxcnHdWjVodpqV8T7eDUQq4Y7e':['10秒'],
'doxcnUZh1PNjF7CkAUfKoOpJ0hb':['涨粉0'],
'doxcnu8D4QakvtCJGmHt3fp1rUh':['4111/13=','316'],
'doxcnkv3cwlbACb9eWPCSFcIJOc':['7.8%'],
'doxcnrwnMbuDlViH5YdVtfBp1ag':['15秒'],
'doxcnINtlIP4ZGgQlEm2Mp3IzHg':['8赞/0评/7藏/3分享'],
'doxcn8yfR9eINj4YxJKZlOXPAzb':['382/13=','29'],
'doxcncmtFiOcQCvbERiZeKm9DTe':['4.2%'],
'doxcnksNqNCtO2cKgQJEdN3nEac':['14秒'],
'doxcn2vz3kV1CyBsO0dHDsbCJud':['涨粉0'],
'doxcnXp6lwurBtCyNDaRjrLfR4b':['1701/22=','77'],
'doxcngb1vNRT0uOgDYBbNJxfdTd':['7.7%'],
'doxcnYZOmywWwVbVVWZq0R5O34b':['40秒'],
'doxcnxsWcJ2g6LmHaZhryETes2f':['涨粉0']}
for bid,parts in changes.items():patch(bid,parts);print(bid,flush=True)
