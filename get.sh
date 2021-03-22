#!/bin/bash

wget "http://dumps.wikimedia.your.org/wikidatawiki/entities/latest-all.ttl.gz" -q -O - | pv -s 98758217296 | pigz -c -d | python3 extract.py > /mnt/Datos/wikidata-labels2.tsv

