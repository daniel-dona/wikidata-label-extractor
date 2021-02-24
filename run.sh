#!/bin/bash

wget "http://dumps.wikimedia.your.org/wikidatawiki/entities/latest-all.ttl.gz" -q -O - | pigz -c -d | python3 extract.py > /output/labels.tsv
