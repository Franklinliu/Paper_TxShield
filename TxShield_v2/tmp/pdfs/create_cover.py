from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from pathlib import Path
out=Path('deliverables/TxShield_TIFS_Cover_Letter.pdf')
style=ParagraphStyle('body',fontName='Times-Roman',fontSize=11,leading=14.5,spaceAfter=10,alignment=TA_LEFT)
paras=[
'20 October 2026',
'Editor-in-Chief<br/>IEEE Transactions on Information Forensics and Security',
'Dear Editor-in-Chief,',
'Please consider our manuscript, “TxShield: Transaction-level RAG-enabled DeFi Attack Detection,” for publication in <i>IEEE Transactions on Information Forensics and Security</i>.',
'Detecting attacks on decentralized finance (DeFi) protocols requires distinguishing malicious behavior from legitimate transactions that involve similar contract interactions, asset transfers, and flash loans. TxShield addresses this challenge by combining execution-trace analysis, retrieval of historical attack cases, and numerical risk guidance for large language model (LLM) reasoning.',
'The distinctive contribution is how these components cooperate. Historical cases help the LLM interpret transaction behavior, while an XGBoost classifier estimates attack probability from ten transaction features. This score guides whether retrieved cases are retained and, when available, is included in the prompt to encourage scrutiny of potential false positives. The LLM makes the final decision based on transaction evidence. This design aims to limit misleading historical context while preserving the LLM’s ability to recognize attacks from execution behavior.',
'On 728 transactions comprising 364 attacks and 364 benign transactions, TxShield achieves 92.93% F1 and 97.87% precision. Compared with direct XGBoost classification, it reduces false positives from 60 to 7 while maintaining comparable recall. A complementary evaluation detects 86 of 91 price-manipulation attacks. Component and backbone ablations examine the contributions of retrieval, XGBoost guidance, and LLM choice.',
'The manuscript fits TIFS through its focus on detecting security attacks in financial smart-contract systems using transaction evidence. Its practical significance lies in reducing false alarms and supporting evidence-based analysis, helping security analysts prioritize suspicious activity.',
'Wei Ma is currently an Assistant Professor at Blekinge Institute of Technology (BTH), Sweden. This work was mainly carried out while he was at Singapore Management University (SMU). Wei Ma and Shiya Li contributed equally as joint first authors; Ye Liu is the corresponding author.',
'Thank you for considering our manuscript.',
'Sincerely,<br/>Wei Ma, Shiya Li, Jiayi Xu, Ye Liu, Junjie Shi, Cong Wu, Jing Chen,<br/>Lingxiao Jiang, and Zijian Zhang<br/><br/>Correspondence: Ye Liu, Beijing Institute of Technology<br/>ye.liu@bit.edu.cn'
]
doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=54,leftMargin=54,topMargin=45,bottomMargin=45,title='Cover Letter - TxShield',author='Wei Ma and coauthors')
doc.build([Paragraph(p,style) for p in paras])
print(out)
