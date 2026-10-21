from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
root=Path(__file__).resolve().parents[2]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13,'text.color':'blue','axes.labelcolor':'blue','xtick.color':'blue','ytick.color':'blue','axes.edgecolor':'blue','pdf.fonttype':42})
names=['GPT-5.6-luna','DeepSeek-v4-pro','Kimi-k3']
files=['detailed_results_GPT-5.6-luna','detailed_results_DeepSeek-v4-pro_xgboost.json','detailed_results_Kimi_k3.json']
values=[]
for f in files:
 rows=json.loads((root/'pic/file'/f).read_text())['detailed_results']
 assert len(rows)==728
 tp=sum(r['expected_label']=='Attack' and r['predicted_label']=='Attack' for r in rows)
 fp=sum(r['expected_label']=='Benign' and r['predicted_label']=='Attack' for r in rows)
 tn=sum(r['expected_label']=='Benign' and r['predicted_label']=='Benign' for r in rows)
 fn=sum(r['expected_label']=='Attack' and r['predicted_label']=='Benign' for r in rows)
 values.append([(tp+tn)/728,tp/(tp+fp),tp/(tp+fn),2*tp/(2*tp+fp+fn)])
# Original six-model values verified against the original vector PDF bars and draft table.
old_names=['GPT-4.1-mini','Baidu ERNIE-Speed-128k','Llama3-8B','Qwen3-8B','DeepSeek-R1-Distill-Qwen-7B','InternLM3']
old_values=[[.838,.832,.846,.839],[.794,.755,.871,.809],[.778,.741,.854,.793],[.702,.719,.662,.690],[.702,.702,.698,.700],[.551,.533,.827,.649]]
all_names=old_names+names
v=np.array(old_values+values)*100
import csv
with (root/'reports/revision_20261011/fig5_data.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['model','source','accuracy_percent','precision_percent','recall_percent','f1_percent'])
 for i,(name,row) in enumerate(zip(all_names,v)):
  w.writerow([name,'original_paper' if i<6 else files[i-6],*[round(z,6) for z in row]])
fig,ax=plt.subplots(figsize=(11,4.8),layout='constrained')
x=np.arange(9);width=.2
colors=['#156082','#e97132','#196b24','#0f9ed5']
for j,label in enumerate(['Accuracy','Precision','Recall','F1']):
 bars=ax.bar(x+(j-1.5)*width,v[:,j],width,label=label,color=colors[j],linewidth=.65,zorder=3)
 for i,bar in enumerate(bars):
  if i>=6:bar.set_edgecolor('blue')
ax.set_xticks(x,['GPT-4.1\nmini','Baidu ERNIE\nSpeed-128k','Llama3-8B','Qwen3-8B','DeepSeek-R1-Distill\nQwen-7B','InternLM3','GPT-5.6\nluna*','DeepSeek-v4\npro*','Kimi-k3*'])
ax.tick_params(axis='x',labelsize=11)
for i,t in enumerate(ax.get_xticklabels()):t.set_color('black' if i<6 else 'blue')
ax.set_ylim(0,105);ax.set_yticks(np.arange(0,101,20))
ax.set_ylabel('Metric (%)')
ax.grid(axis='y',color='#888888',alpha=.15,zorder=0)
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='upper center',bbox_to_anchor=(.5,1.14),ncol=4,frameon=False,labelcolor='black')
fig.savefig(root/'pic/model_performance_column_chart.pdf',bbox_inches='tight')
fig.savefig(root/'pic/model_performance_column_chart.png',dpi=180,bbox_inches='tight')
