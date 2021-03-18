import sys
import re

buf = ""
n = 0
n2 = 0

def process_sentences(data):
	
	global n
	global n2
	
	item = {'id': '', 'en': [], 'es': [], 'fr': [], 'it': []}

	
	lines = data.replace('\t', '').split("\n")[1:-1]

		
	x1 = re.match("(.*) rdfs:label \"(.*)\"@(.*) ;", lines[0])
	#x1b = re.match("(.*) skos:altLabel \"(.*)\"@(.*) ;", lines[0])
	x2 = re.match("(.*) a wikibase:Item ;", lines[0])
	
	#if x1b != None:
	#	print(x1b.group(1), file=sys.stderr, flush=True)

	if x1 != None or x2 != None:
			
		if x1 != None:
			
			item['id'] = x1.group(1)
			
			if x1.group(3) == "es":
				item['es'].append(x1.group(2))
			
			if x1.group(3) == "en":
				item['en'].append(x1.group(2))
					
			if  x1.group(3) == "fr":
				item['fr'].append(x1.group(2))
				
			if  x1.group(3) == "it":
				item['it'].append(x1.group(2))
				
		else:
			
			item['id'] = x2.group(1)
		
		
		for l in lines[1:]:
			
			#print(l)
			
			z = re.match("rdfs:label \"(.*)\"@(.*) ;", l)
			zb = re.match("skos:altLabel \"(.*)\"@(.*) ;", l)
			
			if zb != None and zb.group(2) == "es":
				item['es'].append(zb.group(1))
				
			if zb != None and zb.group(2) == "en":
				item['en'].append(zb.group(1))
				
			if zb != None and zb.group(2) == "it":
				item['it'].append(zb.group(1))
				
			if zb != None and zb.group(2) == "fr":
				item['fr'].append(zb.group(1))
		
			if z != None and z.group(2) == "es":
				item['es'].append(z.group(1))
	
			if z != None and z.group(2) == "en":
				item['en'].append(z.group(1))
				
			if z != None and z.group(2) == "fr":
				item['fr'].append(z.group(1))
				
			if z != None and z.group(2) == "it":
				item['it'].append(z.group(1))
				
	if item['id'] != '':
		
		if len(item['en']) == 0:
			item['en'].append("")
		if len(item['es']) == 0:
			item['es'].append("")
		if len(item['it']) == 0:
			item['it'].append("")
		if len(item['fr']) == 0:
			item['fr'].append("")
		
		print(item['id'], "\x1f".join(item['en']),"\x1f".join(item['es']),"\x1f".join(item['it']),"\x1f".join(item['fr']), sep="\t")
		
		if n%1000 == 0:		
			print("\nExtracted: ",n," items with ", n2, " terms",file=sys.stderr, flush=True, end="\n")

		n += 1
		n2 += len(item['en'])+len(item['es'])+len(item['it'])+len(item['fr'])



#f = open("/data/Datos/latest-all.ttl")

for line in sys.stdin:
	
	if line.startswith("@prefix"):
		continue
	
	if line.endswith(" .\n"):
		buf += line
		
		process_sentences(buf)
			
		buf = ""
	else:
		
		buf += line

