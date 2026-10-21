import fitz,math
src=fitz.open('pic/TxHunt.pdf')
def make(path,marked):
 d=fitz.open();p=d.new_page(width=1000,height=625);red=(.78,0,0) if marked else (0,0,0);black=(0,0,0)
 def copy(r,t):p.show_pdf_page(fitz.Rect(t),src,0,clip=fitz.Rect(r))
 copy((0,0,938,184),(0,0,938,184));copy((0,184,289,450),(0,184,289,450))
 copy((305,246,506,450),(520,356,721,560));copy((536,353,576,387),(790,459,830,493))
 def txt(r,s,size=20,c=None,font='tiro'):
  assert p.insert_textbox(fitz.Rect(r[0],r[1],r[2],r[3]+12),s,fontname=font,fontsize=size,color=c or red,align=1,lineheight=1.1)>=0,s
 def arrow(points,c=None):
  c=c or red;sh=p.new_shape();sh.draw_polyline(points);sh.finish(color=c,width=1.5,closePath=False);sh.commit();a,b=points[-2:];t=math.atan2(b[1]-a[1],b[0]-a[0]);p.draw_polyline([b,(b[0]-7*math.cos(t-.4),b[1]-7*math.sin(t-.4)),(b[0]-7*math.cos(t+.4),b[1]-7*math.sin(t+.4))],color=c,fill=c,closePath=True)
 sh=p.new_shape();sh.draw_rect(fitz.Rect(291,235,989,617));sh.finish(color=(.08,.18,.23),width=1,dashes='[3 4] 0');sh.commit()
 txt((320,247,510,277),'3. Assess risk',21,font='tibi')
 txt((330,286,486,313),'XGBoost',22,font='tiit')
 txt((565,247,777,277),'4. Select context',21,font='tibi')
 txt((554,286,788,326),'Retain or omit cases',19)
 arrow([(600,184),(600,235)],black)
 txt((610,196,797,225),'Top-k cases',20,black)
 arrow([(486,302),(554,302)])
 txt((493,272,548,296),'p',19)
 arrow([(668,324),(668,350)])
 # Numerical features are taken from the transaction before LLM inference.
 arrow([(190,419),(310,419),(310,302),(330,302)])
 # Probability is also supplied to the prompt, independently of selected context.
 arrow([(435,316),(435,405),(520,405)])
 txt((440,352,515,392),'Risk hint\n(p)',17)
 txt((533,328,655,350),'Prompt',20,black)
 txt((331,438,510,479),'Low risk: omit cases;\nLLM still decides',17)
 # Transaction evidence reaches the prompt regardless of the gate.
 arrow([(268,419),(281,419),(281,592),(620,592),(620,560)],black)
 txt((331,561,550,587),'Current transaction',18,black)
 arrow([(721,457),(780,457)],black)
 txt((734,416,887,446),'5. Analyze',21,font='tibi')
 txt((782,496,842,524),'LLM',19,black)
 arrow([(843,476),(868,476),(900,442)])
 arrow([(868,476),(900,515)])
 txt((893,416,985,446),'Attack',21)
 txt((891,518,987,549),'Benign',21)
 txt((732,567,981,601),'DeFi Attack Detection',21,black,'tiit')
 d.save(path,garbage=4,deflate=True)
 open(path.replace('.pdf','.svg'),'w').write(d[0].get_svg_image(text_as_path=False))
make('pic/TxHunt_xgb_marked.pdf',True);make('pic/TxHunt_xgb_submission.pdf',False)
d=fitz.open('pic/TxHunt_xgb_marked.pdf');d[0].get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save('/tmp/fig_style_restored.png')
