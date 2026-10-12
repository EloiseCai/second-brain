# coding: utf-8
import json,re,subprocess
from pathlib import Path
tokens={'003':'KbH0dnVz6opMzzxoP5tcUyQrn1g','004':'PiUadG4U6ojNP5x10Vwc7ExnnVI','005':'EnLldY67BoCI5exqso2cWm7fnOg','006':'RlD1dRA4toJ5HqxRnURchUZmnce','007':'NuhWdi3E4oq7hQxzkewcu9VrnHd','008':'QTTGdkGPkofU6xxIXYycSIuNneb','009':'Cwr1d1z0aoYSDuxXOEFcKXRhn6b','010':'SyAtd6MFXoLMNyxfhJFcthAEngf','011':'A0MXd4jfaoA27wxYvegcYDl1ntf','012':'J16UdZNAZoVZrXxOTPFcPcTBnxh','013':'NEusdAEcIo7yD1xPh9ncjOZ1nlh','014':'E4NRdzfZao8FY9xbwzlcYy1Jn8c','015':'IsRnd6zW2oKcOSxYBDbcudNCnUd','016':'UfgCdJC2LoHLCOxvrNfcO10fn7d','017':'FpYPdAV9boRt2jxuf0DcMuLFnkf','019':'Euj5dIT98ouvnaxBMMgcraxhn9c'}
for n,tok in tokens.items():
 if Path(f'.codex-tmp/detail-{n}-1009.md').exists():continue
 p=subprocess.run(['lark-cli','docs','+fetch','--doc',tok,'--doc-format','markdown','--as','user'],capture_output=True,text=True);d=json.loads(p.stdout);assert d['ok'],n;s=d['data']['document']['content'];Path(f'.codex-tmp/review-{n}-1009-before.md').write_text(s)
 ids=re.findall(r'[a-f0-9]{24}',s);assert ids,n
 id=ids[0];url='https://creator.xiaohongshu.com/statistics/note-detail?noteId='+id
 for attempt in range(3):
  p=subprocess.run(['browser-act','--session','review-1009','navigate',url],capture_output=True,text=True)
  if p.returncode==0:break
 assert p.returncode==0,(n,p.stderr)
 p=subprocess.run(['browser-act','--session','review-1009','get','markdown'],capture_output=True,text=True);assert p.returncode==0,(n,p.stderr)
 Path(f'.codex-tmp/detail-{n}-1009.md').write_text(p.stdout)
 cuts=re.findall(r'数据更新至(\d\d-\d\d \d\d:\d\d)',p.stdout)
 print(n,id,sorted(set(cuts)),flush=True)
