from pathlib import Path
import re,json,html
p=Path(__file__).resolve().parents[1]/'dist';old=(p.parent/'data/research-original.html').read_text();prefix=old.split('<main>')[0];suffix=old.split('</main>')[1];articles=re.findall(r'<article class="project-detail">.*?</article>',old);pubs={x['index']:x for x in json.load(open(p.parent/'data/publications.json'))};esc=html.escape
areas=[('ai-security-privacy-forensics', 'AI Security, Privacy & Forensics', 'area-forensics.webp', 'Investigating how intelligent systems expose information, fail under attack, and leave evidence that can be examined.', 'Evaluate threats to learning systems and consumer AI while developing reproducible methods for privacy and forensic analysis.', 'Connect model behavior, user-facing tools and recoverable digital evidence rather than treating these as isolated problems.', [3, 4, 6, 7]), ('secure-sustainable-ai', 'Secure & Sustainable AI Systems', 'area-systems.webp', 'Understanding the joint costs of intelligence, robustness and resource use across learning and deployment.', 'Measure predictive utility, adversarial resilience, energy and latency together, including resource-constrained settings.', 'Make security–sustainability tradeoffs explicit and comparable across methods and system conditions.', [0, 1, 2]), ('quantum-ai-security', 'Quantum AI & Security', 'area-quantum.svg', 'Exploring quantum learning architectures and the questions that arise when trainability, reliability and security are considered together.', 'Study localized quantum architectures and rigorous evaluation of hybrid quantum–classical learning. Security evaluation remains an emerging direction.', 'Investigate how circuit structure and locality affect trainability while separating observed simulator results from claims of practical quantum advantage.', []), ('cyber-physical-systems', 'Cyber-Physical Systems', 'abstract-wearable-lifecycle.webp', 'Connecting sensing, learning and physical environments under privacy, reliability and resource constraints.', 'Evaluate trustworthy sensor interpretation and language-assisted cyber-physical workflows.', 'Relate characteristics of physical signals and distributed devices to the behavior of the models that interpret them.', [3, 5]), ('llms-multimodal-agentic-ai', 'LLMs, Multimodal & Agentic AI', 'abstract-future-infrastructure.webp', 'Studying systems that interpret language, images and sensor signals, and the emerging behaviors of interacting AI agents.', 'Evaluate multimodal capabilities and vulnerabilities, privacy in AI assistance, and agent interactions.', 'Connect evidence across modalities and interaction settings, testing reliability instead of assuming that fluent output is correct.', [4, 5])]
areas=[areas[0],areas[4],areas[1],areas[2],areas[3]]
def reflist(area):
 ids=[x["index"] for x in pubs.values() if area in x.get("researchAreaIds",[])]
 out=''
 for i in ids:
  x=pubs[i];url=x['url'];out+=f'<li><span class="tag">{esc(x["type"])} · {x["year"]}</span><a href="{esc(url)}">{esc(x["title"])} ↗</a><p>{esc(x["venue"])}</p></li>'
 return '<ul class="area-publications">'+out+'</ul>'
def project(title,status,desc,goal,merit,app,impact):
 return f'<article class="research-project"><span class="tag">{status}</span><h3>{title}</h3><p>{desc}</p><div class="research-pair"><div><h4>Goals</h4><p>{goal}</p></div><div><h4>Intellectual Merit</h4><p>{merit}</p></div></div><div class="research-pair"><div><h4>Applications</h4><p>{app}</p></div><div><h4>Impact</h4><p>{impact}</p></div></div></article>'
for slug,name,img,desc,goal,merit,inds in areas:
 body=f'<main class="research-page"><section class="page-intro"><a class="text-link" href="research.html">← All research areas</a><h1>{esc(name)}</h1><p>{desc}</p></section><figure class="area-hero"><img src="assets/{img}" alt="Conceptual illustration of {esc(name.lower())}" width="1400" height="788"></figure><section class="research-pair section"><div><h2>Research Goals</h2><p>{goal}</p></div><div><h2>Intellectual Merit</h2><p>{merit}</p></div></section><section class="section"><h2>Projects & directions</h2>'
 for i in inds:
  a=articles[i]
  # Keep original project substance, avoid repeating large project illustrations and faces.
  a=re.sub(r'<figure.*?</figure>','',a);a=a.replace('class="project-detail"','class="research-project"')
  body+=a
 if slug=='quantum-ai-security':
  body+=project('Localized quantum learning with Q-Capsule','Preprint · architecture research','Q-Capsule studies a localized capsule-based quantum neural architecture for barren plateau mitigation.','Investigate trainability through localized quantum structure.','Examine architectural alternatives to broadly entangled circuits without assuming quantum advantage.','Hybrid quantum–classical machine-learning research and reproducible simulator evaluation.','A research basis for studying trainability. Practical quantum advantage and deployed security benefits are not established by this page.')
  body+=json.loads((p.parent/'data/ictai-quantum-project-source.json').read_text())['projectHtml']
  body+=project('Security and reliability of quantum AI','Emerging direction','A prospective agenda for evaluating how quantum and hybrid learning systems behave under unreliable or adversarial conditions.','Develop carefully controlled comparisons with classical baselines.','Separate architectural effects, noise sensitivity and security assumptions.','Future robustness evaluation of quantum learning pipelines.','Research questions rather than demonstrated defenses or operational deployments.')
 if slug=='llms-multimodal-agentic-ai':
  body+=project('Multimodal robustness and agent interactions','Published foundations and emerging preprints','Research spans adversarial evaluation of vision–language models and analysis of emotional dynamics in agent-to-agent interactions. VetClaw explores an edge–cloud multimodal agentic screening prototype.','Characterize reliability across modalities and interactions, with explicit evaluation limits.','Study the relationship between input evidence, interaction behavior and system constraints.','Driving-scene understanding, consumer AI tools and exploratory veterinary screening.','Evidence for evaluating vulnerabilities and prototype behavior, not validated autonomous driving or clinical performance.')
 body+='</section><section class="section"><h2>Selected publications</h2>'+reflist(slug)+'</section></main>'
 out=prefix.replace('<title>Research |','<title>'+esc(name)+' |').replace('</head>','<link rel="stylesheet" href="research-pages.css"></head>')+body+suffix
 (p/(slug+'.html')).write_text(out)
cards=''
for slug,name,img,desc,*_ in areas:
 img=img.replace('.webp','-palette.webp')
 cards+=f'<a class="research-area-card" href="{slug}.html"><img src="assets/{img}" alt="" width="700" height="394" loading="lazy"><div><h2>{esc(name)}</h2><p>{desc}</p><span class="text-link">Explore projects & publications →</span></div></a>'
body='<main class="research-page"><section class="page-intro"><h1>Research</h1></section><section class="research-area-grid" aria-label="Research areas">'+cards+'</section></main>'
(p/'research.html').write_text(prefix.replace('</head>','<link rel="stylesheet" href="research-pages.css"></head>')+body+suffix)

# Canonical area tags, never independently curated area bibliography lists.
import subprocess,sys
subprocess.run([sys.executable,"scripts/build-area-publications.py"],check=True)
