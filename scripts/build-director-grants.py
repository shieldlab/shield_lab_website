"""Director grant section shares announcement dates and records with canonical news."""
import json,html,re
from pathlib import Path
E=html.escape
news=json.loads(Path('data/news.json').read_text())
entries=[dict(x['directorGrant'],date=x['date'],dateLabel=x['dateLabel'],url=x['directorGrant'].get('projectUrl',x.get('projectUrl',''))) for x in news if x.get('directorGrant')]
entries.sort(key=lambda x:x['date'],reverse=True)
entries+=json.loads(Path('data/director-additional-grants.json').read_text())
rows=[]
for x in entries:
 date='<span class="grant-date">Awarded'+(' · '+E(x.get('date','')[:4]) if x.get('dateLabel') else '')+'</span>'
 link='<a class="text-link" href="'+E(x['url'],quote=True)+'">'+('Project details →' if x.get('projectUrl') else 'Workshop program →')+'</a>' if x.get('url') else ''
 rows.append('<li>'+date+'<div><p class="grant-sponsor">'+E(x['sponsor'])+' · '+E(x.get('role','PI'))+'</p><h3>'+E(x['title'])+'</h3><p>'+E(x['support'])+'</p>'+link+'</div></li>')
honors='<div class="director-honors"><h3>Selected Honors</h3><ul><li>Summer Research Faculty Award, Robert Morris University (2022)</li><li>Dissertation Year Fellowship, Florida International University (2019)</li><li>Best Graduate Student in Research, Florida International University (2019)</li></ul></div>'
section='<section class="section director-grants" id="grants-awards"><h2>Grants &amp; Awards</h2><ul class="grant-list">'+''.join(rows)+'</ul>'+honors+'<a class="director-back-top" href="#director-top">↑ Back to top</a></section>'
p=Path('dist/director.html');s=p.read_text()
if 'id="grants-awards"' in s:s=re.sub(r'<section class="section director-grants".*?</section>',lambda m:section,s,flags=re.S)
else:s=s.replace('<section class="section"><h2>Teaching &amp; mentorship</h2>',section+'<section class="section"><h2>Teaching &amp; mentorship</h2>').replace('<section class="section"><h2>Teaching & mentorship</h2>',section+'<section class="section"><h2>Teaching & mentorship</h2>')
if 'href="director-grants.css"' not in s:s=s.replace('</head>','<link rel="stylesheet" href="director-grants.css"></head>')
p.write_text(s)
assert s.count('id="grants-awards"')==1
print('Director grants:',len(entries))
