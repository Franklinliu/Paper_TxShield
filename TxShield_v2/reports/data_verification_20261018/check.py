import csv,json,re
from pathlib import Path
from collections import Counter
base=Path('pic/file/data');out=Path('reports/data_verification_20261018')
def read(n):return list(csv.DictReader((base/n).open(encoding='utf-8-sig')))
full=read('defiattack_with_xgboost_728.csv');abl=read('ablation_study_kimi_k3.csv');old=read('defiattack_original_noxgboost_728.csv');hist=read('history_knowledge.csv')
f={r['tx_hash']:r for r in full};a={r['tx_hash']:r for r in abl}
metrics=[]
for name,rows,label in [('with',full,'label'),('ablation',abl,'predicated_label'),('without',old,'Label')]:
 print(name,'rows',len(rows),'unique',len({r['tx_hash'] for r in rows}),'labels',dict(Counter(r[label] for r in rows)),'same hashes',set(f)=={r['tx_hash'] for r in rows},'label differences',sum(r[label]!=f[r['tx_hash']]['label'] for r in rows))
 for col in rows[0]:
  if col in ['tx_hash',label]:continue
  valid=[r for r in rows if r[col] in ['0','1']];c=Counter((r[label],r[col]) for r in valid)
  tp,fp,tn,fn=[c[x] for x in [('1','1'),('0','1'),('0','0'),('1','0')]]
  m=dict(file=name,model=col,N=len(valid),invalid=len(rows)-len(valid),TP=tp,FP=fp,TN=tn,FN=fn,accuracy=100*(tp+tn)/len(valid),precision=100*tp/(tp+fp),recall=100*tp/(tp+fn),f1=200*tp/(2*tp+fp+fn))
  metrics.append(m);print(m)
trans=[]
for h,r in f.items():
 trans.append(dict(tx_hash=h,label=r['label'],without=a[h]['wo_xgboost'],with_xgb=r['Kimi_k3']))
print('TRANSITIONS',dict(Counter((r['label'],r['without'],r['with_xgb']) for r in trans)))
for name,rows in [('all_transitions',trans),('zero_to_one',[r for r in trans if r['without']=='0' and r['with_xgb']=='1']),('metrics',metrics)]:
 with (out/(name+'.csv')).open('w') as w:
  cw=csv.DictWriter(w,fieldnames=list(rows[0]));cw.writeheader();cw.writerows(rows)
over=[dict(**r,test_label=f[r['hash']]['label']) for r in hist if r['hash'] in f]
print('HISTORY',len(hist),'unique hashes',len({r['hash'] for r in hist}),'overlap',len(over),'overlap label counts',dict(Counter(r['test_label'] for r in over)))
with (out/'knowledge_overlap.csv').open('w') as w:
 cw=csv.DictWriter(w,fieldnames=list(over[0]));cw.writeheader();cw.writerows(over)
for p,col in [(Path('pic/file/detailed_results_Kimi_k3.json'),'Kimi_k3'),(Path('pic/file/detailed_results_GPT-5.6-luna'),'GPT-5.6-luna'),(Path('pic/file/detailed_results_DeepSeek-v4-pro_xgboost.json'),'Deepseek-v4-pro')]:
 d=json.loads(p.read_text());rows=d['detailed_results'];mp={'Attack':'1','Benign':'0'}
 mism=[];lab=[];mentions=[];response_mismatch=[]
 for r in rows:
  h=r['file_name'].split('_')[0]
  if not h.startswith('0x'): h='0x'+h
  if mp.get(r['predicted_label'])!=f[h][col]:mism.append(h)
  if mp.get(r['expected_label'])!=f[h]['label']:lab.append(h)
  txt=r.get('answer_content',r['response']);m=re.match(r'^\s*\[?(Attack|Benign)\b',txt,re.I)
  if m and m.group(1).lower()!=r['predicted_label'].lower():response_mismatch.append(h)
  if re.search(r'\b(?:ML|XGBoost|classifier|machine.learning)\b',txt,re.I):mentions.append({'tx_hash':h,'response':txt})
 print('JSON',col,'N',len(rows),'csv prediction mismatch',len(mism),'label mismatch',len(lab),'response label mismatch',len(response_mismatch),'ML mentions',len(mentions),'keys',list(rows[0]))
 (out/(col+'_ml_mentions.json')).write_text(json.dumps(mentions,ensure_ascii=False,indent=2))
 (out/(col+'_csv_mismatches.json')).write_text(json.dumps(mism))
