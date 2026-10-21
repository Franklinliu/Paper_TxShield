from pathlib import Path
import csv, io, json, re
from collections import Counter
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'pic/file'
OUT = Path(__file__).resolve().parent

def read(name):
    b = (SRC/name).read_bytes()
    try: s = b.decode('utf-8-sig')
    except UnicodeDecodeError: s = b.decode('gb18030')
    return list(csv.DictReader(io.StringIO(s)))

def metrics(pairs):
    c = Counter((y,p) for y,p in pairs)
    tp,tn,fp,fn = [c[x] for x in [(1,1),(0,0),(0,1),(1,0)]]
    n = len(pairs)
    invalid = sum(p not in (0,1) for y,p in pairs)
    return dict(n=n,tp=tp,tn=tn,fp=fp,fn=fn,invalid=invalid,
      accuracy=(tp+tn)/n,precision=tp/(tp+fp) if tp+fp else 0,
      recall_valid=tp/(tp+fn) if tp+fn else 0,
      f1_valid=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0,
      recall_all_attacks=tp/sum(y==1 for y,p in pairs))

def pred(v): return {'0':0,'1':1,'Attack':1,'Benign':0}.get(v)

old = [r for r in read('原多模型测试结果（728）.csv') if r['Label'] in ('0','1')]
new = [r for r in read('加入XGBoost.csv') if r['label'] in ('0','1')]
audit = dict(csv={},json={},mismatches={})
for name,rows,label in [('old',old,'Label'),('new',new,'label')]:
    audit[name+'_ids'] = dict(rows=len(rows),unique=len({r['tx_hash'] for r in rows}),labels=dict(Counter(r[label] for r in rows)))
    for col in rows[0]:
        if col not in ('tx_hash',label,''):
            pairs=[(int(r[label]),pred(r[col])) for r in rows]
            audit['csv'][name+':'+col] = metrics(pairs)
            audit['csv'][name+':'+col]['invalid_by_label'] = dict(Counter(y for y,p in pairs if p is None))
maps={}
for file,col in [('detailed_results_Kimi_k3.json','Kimi_k3'),('detailed_results_GPT-5.6-luna','GPT-5.6-luna'),('detailed_results_DeepSeek-v4-pro_xgboost.json','Deepseek-v4-pro')]:
    d=json.loads((SRC/file).read_text()); rows=d['detailed_results']
    pairs=[(pred(r['expected_label']),pred(r['predicted_label'])) for r in rows]
    m={'0x'+r['file_name'].split('_')[0].lower().removeprefix('0x'):r for r in rows}
    maps[col]=m
    times=np.array([r['processing_time_seconds'] for r in rows])
    audit['json'][col] = dict(file=file,metrics=metrics(pairs),summary=d['summary']['metrics'],date=d['summary']['test_date'],unique=len(m),labels=dict(Counter(r['predicted_label'] for r in rows)),times=dict(mean=float(times.mean()),median=float(np.median(times)),p95=float(np.percentile(times,95)),min=float(times.min()),max=float(times.max())),correct_flag_disagreements=sum(r['is_correct'] != (r['expected_label']==r['predicted_label']) for r in rows),id_difference=len(set(m)^{r['tx_hash'].lower() for r in new}))
    audit['mismatches'][col]=[dict(hash=r['tx_hash'],csv=r[col],json=m[r['tx_hash'].lower()]['predicted_label'],label=r['label']) for r in new if pred(r[col]) != pred(m[r['tx_hash'].lower()]['predicted_label'])]
oldmap={r['tx_hash'].lower():r for r in old}
newmap={r['tx_hash'].lower():r for r in new}
audit['old_new_id_difference']=len(set(oldmap)^set(newmap))
audit['old_new_label_difference']=sum(r['Label'] != newmap[h]['label'] for h,r in oldmap.items())
hist=read('history_knowledge.csv'); result=read('result.csv')
hs={r['hash'].lower() for r in hist}; rs={r['hash'].lower() for r in result}; attacks={h for h,r in newmap.items() if r['label']=='1'}
audit['data_split']=dict(history_rows=len(hist),history_unique=len(hs),result_rows=len(result),result_unique=len(rs),history_test_overlap=sorted(hs&set(newmap)),result_history_overlap=len(rs&hs),result_test_attacks_overlap=len(rs&attacks),result_minus_history_equals_attacks=(rs-hs==attacks),history_test_shared_contracts=sorted({r['contract_name'] for r in hist}&{r['contract_name'] for r in result if r['hash'].lower() in attacks}))
audit['data_split']['overlap_by_label']=dict(Counter(newmap[h]['label'] for h in hs&set(newmap)))
audit['data_split']['invalid_length_ids']=[h for h in newmap if not re.fullmatch(r'0x[0-9a-f]{64}',h)]
overlap=[dict(identifier=h,test_label=newmap[h]['label'],history_contract=next(r['contract_name'] for r in hist if r['hash'].lower()==h),test_file=maps['Kimi_k3'][h]['file_name']) for h in sorted(hs&set(newmap))]
with (OUT/'knowledge_test_overlap.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(overlap[0]));w.writeheader();w.writerows(overlap)
q=[(int(oldmap[h]['Label']),pred(oldmap[h]['Qwen3-8B']),pred(newmap[h]['Qwen3_8B'])) for h in oldmap]
audit['qwen_paired']=dict(n=sum(a is not None and b is not None for y,a,b in q),old=metrics([(y,a) for y,a,b in q if a is not None and b is not None]),new=metrics([(y,b) for y,a,b in q if a is not None and b is not None]),transitions={str(k):v for k,v in Counter((y,a,b) for y,a,b in q if a is not None and b is not None).items()})
audit['standalone']=metrics([(1,1)]*323+[(0,0)]*304+[(0,1)]*60+[(1,0)]*41)
audit['old_full_paper']=metrics([(1,1)]*308+[(0,0)]*302+[(0,1)]*62+[(1,0)]*56)
audit['common_missed_attacks']=[dict(hash=h,contract=next((r['contract_name'] for r in result if r['hash'].lower()==h),''),type=next((r['Matched_Attack_Type'] for r in result if r['hash'].lower()==h),'')) for h in attacks if all(m[h]['predicted_label']!='Attack' for m in maps.values())]
(OUT/'audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
print(json.dumps(audit,ensure_ascii=False,indent=2))
