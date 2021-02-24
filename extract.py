import sys
import re

buf = ""
n = 0

def process_sentences(data):
	
	global n
	
	item = {'id': '', 'en': '', 'es': '', 'fr': '', 'it': ''}

	
	lines = data.replace('\t', '').split("\n")[1:-1]

		
	x1 = re.match("(.*) rdfs:label \"(.*)\"@(.*) ;", lines[0])
	x2 = re.match("(.*) a wikibase:Item ;", lines[0])

	if x1 != None or x2 != None:
			
		if x1 != None:
			
			item['id'] = x1.group(1)
			
			if x1.group(3) == "es":
				item['es'] = x1.group(2)
			
			if x1.group(3) == "en":
				item['en'] = x1.group(2)
					
			if  x1.group(3) == "fr":
				item['fr'] = x1.group(2)
				
			if  x1.group(3) == "it":
				item['it'] = x1.group(2)
				
		else:
			
			item['id'] = x2.group(1)
		
		
		for l in lines[1:]:
			
			#print(l)
			
			z = re.match("rdfs:label \"(.*)\"@(.*) ;", l)
		
			if z != None and z.group(2) == "es":
				item['es'] = z.group(1)
	
			if z != None and z.group(2) == "en":
				item['en'] = z.group(1)
				
			if z != None and z.group(2) == "fr":
				item['fr'] = z.group(1)
				
			if z != None and z.group(2) == "it":
				item['it'] = z.group(1)
				
	if item['id'] != '':
		print(item['id'], item['en'], item['es'], item['it'], item['fr'], sep="\t")
		
		if n%100 == 0:		
			print("Extracted:",n,"terms",file=sys.stderr, flush=True, end="\r")
		
		n+=1



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

