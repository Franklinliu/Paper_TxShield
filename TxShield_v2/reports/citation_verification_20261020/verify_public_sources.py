from pathlib import Path
import re,json,requests,concurrent.futures,time
from difflib import SequenceMatcher
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent
bib=Path('sample-base.bib').read_text()
keys=re.findall(r'\\bibitem\{([^}]+)\}',Path('main_submission.bbl').read_text())
def fields(block):
 out={}
 for m in re.finditer(r'(\w+)\s*=\s*',block):
  i=m.end()
  if i>=len(block):continue
  if block[i]=='{':
   level=1;j=i+1
   while j<len(block) and level:
    if block[j]=='{' and block[j-1]!='\\':level+=1
    if block[j]=='}' and block[j-1]!='\\':level-=1
    j+=1
   val=block[i+1:j-1]
  elif block[i]=='"':
   j=block.find('"',i+1);val=block[i+1:j]
  else:val=block[i:].split(',')[0].strip()
  out[m[1].lower()]=re.sub(r'\s+',' ',val)
 return out
entries={}
for b in re.split(r'@\w+\s*\{',bib)[1:]:
 k=b.split(',',1)[0].strip();entries[k]=fields(b.split(',',1)[1])
refs=[dict(n=i+1,key=k,**entries[k]) for i,k in enumerate(keys)]
(ROOT/'references.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2))
def norm(s):return re.sub('[^a-z0-9]+',' ',s.lower()).strip()
def sim(a,b):return SequenceMatcher(None,norm(a),norm(b)).ratio()
def get(url,params=None):
 r=requests.get(url,params=params,timeout=25,headers={'User-Agent':'TxShield-Bibliography-Verification/1.0'});r.raise_for_status();return r
nonacademic={1,2,3,6,8,17,18,19,30,34,35,36,37}
def check(ref):
 result={'n':ref['n'],'key':ref['key'],'input':ref,'evidence':[]};title=ref.get('title','').replace('{','').replace('}','')
 if ref['n'] not in nonacademic:
  try:
   url='https://api.crossref.org/works';data=get(url,{'query.title':title,'rows':3}).json()['message']['items'];matches=[]
   for x in data:
    t=(x.get('title') or [''])[0];matches.append({'similarity':round(sim(title,t),3),'title':t,'doi':x.get('DOI'),'author':x.get('author'),'year':x.get('published'),'venue':x.get('container-title'),'page':x.get('page'),'volume':x.get('volume'),'url':x.get('URL')})
   result['crossref']=sorted(matches,key=lambda x:x['similarity'],reverse=True)
  except Exception as e:result['crossref_error']=str(e)
  if not result.get('crossref') or result['crossref'][0]['similarity']<.9:
   try:
    x=get('https://api.openalex.org/works',{'search':title,'per-page':3}).json()['results'];result['openalex']=[{'similarity':round(sim(title,a.get('title','')),3),'title':a.get('title'),'doi':a.get('doi'),'year':a.get('publication_year'),'authors':[z['author']['display_name'] for z in a.get('authorships',[])],'url':a.get('primary_location',{}).get('landing_page_url')} for a in x]
   except Exception as e:result['openalex_error']=str(e)
 url=ref.get('url')
 if not url:
  u=re.search(r'https?://[^}\s]+',ref.get('howpublished',''));url=u[0] if u else None
 if not url and ref.get('eprint'):url='https://arxiv.org/abs/'+ref['eprint']
 if url:
  try:
   response=get(url);result['source_url']=response.url;result['source_status']=response.status_code
   if 'pdf' not in response.headers.get('Content-Type',''):
    soup=BeautifulSoup(response.text,'html.parser');result['source_title']=soup.title.get_text() if soup.title else ''
    result['source_metadata']=[dict(m.attrs) for m in soup.find_all('meta') if re.search('citation|dc\.|og:title|article:',str(m.get('name',''))+str(m.get('property','')),re.I)]
    for tag in soup(['script','style','nav','footer']):tag.decompose()
    result['source_text']=soup.get_text(' ',strip=True)[:40000]
  except Exception as e:result['source_error']=str(e)
 (ROOT/f'ref_{ref["n"]:02}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 best=(result.get('crossref') or [{}])[0];print(ref['n'],ref['key'],best.get('similarity','web'),best.get('title',result.get('source_title',result.get('source_error',''))),flush=True)
 return result
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:results=list(ex.map(check,refs))
 (ROOT/'all_evidence.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
