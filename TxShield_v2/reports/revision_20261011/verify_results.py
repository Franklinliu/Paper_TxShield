"""Recompute reported results without changing any source experiment data."""
from pathlib import Path
import csv, json, re
from collections import Counter

root = Path(__file__).resolve().parents[2]
out = Path(__file__).parent
def metrics(pairs):
    c=Counter(pairs)
    tp,fp,tn,fn=(c[(1,1)],c[(0,1)],c[(0,0)],c[(1,0)])
    return dict(N=len(pairs),TP=tp,FP=fp,TN=tn,FN=fn,
                accuracy=100*(tp+tn)/len(pairs),precision=100*tp/(tp+fp),
                recall=100*tp/(tp+fn),f1=200*tp/(2*tp+fp+fn))

audit={}
for name,expected in [('Kimi_k3.json',(322,7,357,42)),('DeepSeek-v4-pro_xgboost.json',(325,24,340,39)),('GPT-5.6-luna',(318,29,335,46))]:
    rows=json.loads((root/'pic/file'/('detailed_results_'+name)).read_text())['detailed_results']
    assert len(rows)==728
    assert all(r[k] in ('Attack','Benign') for r in rows for k in ['expected_label','predicted_label'])
    result=metrics([(int(r['expected_label']=='Attack'),int(r['predicted_label']=='Attack')) for r in rows])
    assert tuple(result[k] for k in ['TP','FP','TN','FN'])==expected
    audit[name]=result
    if name=='Kimi_k3.json':
        kimi={re.sub(r'_(attack|benign)\.json$','',r['file_name']).removeprefix('0x'):int(r['predicted_label']=='Attack') for r in rows}

rows=list(csv.DictReader((root/'pic/file/data/ablation_study_kimi_k3.csv').open()))
for col in ['wo_xgboost','test_abl_no_two_stage','norag']:
    valid=[r for r in rows if r[col] in ['0','1']]
    audit[col]=metrics([(int(r['predicated_label']),int(r[col])) for r in valid])
    audit[col]['invalid']=len(rows)-len(valid)
valid=[r for r in rows if r['norag'] in ['0','1']]
audit['full_on_norag_subset']=metrics([(int(r['predicated_label']),kimi[r['tx_hash'].removeprefix('0x')]) for r in valid])
audit['paired_norag_f1_gap']=audit['full_on_norag_subset']['f1']-audit['norag']['f1']

# Verify retained numeric table rows exactly, including the old costs and category rates.
old=(out/'original/evaluation.tex').read_text()
new=(root/'sections/evaluation.tex').read_text()
def rows_for(text,label):
    start=text.index('\\label{'+label+'}')
    end=text.index('\\end{tabular}',start)
    return [x.strip() for x in text[start:end].splitlines() if '&' in x and re.search(r'\d',x) and not x.lstrip().startswith('%')]
for label in ['tab:api_cost_comparison','tab:capability_spectrum','tab:recall-d1-dataset']:
    assert rows_for(old,label)==rows_for(new,label),label
audit['retained_numeric_tables']='identical: efficiency, attack category, price benchmark'
active='\n'.join(x for p in (root/'sections').glob('*.tex') for x in p.read_text().splitlines() if not x.lstrip().startswith('%'))
assert not any(x in active for x in ['0.824','0.586','0.601','95.60'])
(out/'verified_metrics.json').write_text(json.dumps(audit,indent=2))
print(json.dumps(audit,indent=2))

# Preserve Figures 1–4; update Figure 5 in place as requested.
def figures(text):
    text='\n'.join(l for l in text.splitlines() if not l.lstrip().startswith('%'))
    return re.findall(r'\\begin\{figure\*?\}.*?\\end\{figure\*?\}',text,re.S)
def body_without_caption(text):
    a=text.index(r'\caption{'); i=a+len(r'\caption{'); depth=1
    while depth:
        if text[i]=='{':depth+=1
        elif text[i]=='}':depth-=1
        i+=1
    text=text[:a]+text[i:]
    return re.sub(r'\s+','',text.replace(r'\centering',''))
count=0
for name in ['approach','evaluation']:
    originals=figures((out/'original'/f'{name}.tex').read_text())
    revised=figures((root/'sections'/f'{name}.tex').read_text())
    for f in originals:
        if 'model_performance_column_chart.pdf' in f:
            assert any('model_performance_column_chart.pdf' in g for g in revised)
            continue
        assert any(body_without_caption(f)==body_without_caption(g) for g in revised), f
        count+=1
assert count==4
assert len(figures((root/'sections/approach.tex').read_text()))+len(figures(new))==5
print('Figures 1–4 preserved; Figure 5 updated in place; no duplicate Figure 6.')

rows=list(csv.DictReader((out/'fig5_data.csv').open()))
assert len(rows)==9
expected=[[83.8,83.2,84.6,83.9],[79.4,75.5,87.1,80.9],[77.8,74.1,85.4,79.3],[70.2,71.9,66.2,69.0],[70.2,70.2,69.8,70.0],[55.1,53.3,82.7,64.9]]
keys=['accuracy_percent','precision_percent','recall_percent','f1_percent']
for r,e in zip(rows[:6],expected):assert [float(r[k]) for k in keys]==e
for r,f in zip(rows[6:],['GPT-5.6-luna','DeepSeek-v4-pro_xgboost.json','Kimi_k3.json']):
 for col,metric in zip(keys,['accuracy','precision','recall','f1']):assert abs(float(r[col])-audit[f][metric])<1e-5
assert 'pic/model_performance_original.pdf' not in new
assert 'Panel (a)' not in new
print('Fig. 5: nine models on one axis, six original series unchanged, three new series verified against JSON.')
