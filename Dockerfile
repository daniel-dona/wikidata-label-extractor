FROM ubuntu:18.04

RUN apt-get update
RUN apt-get upgrade -y
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get install wget locales apt-utils pv python3 python3-pip pigz -y

RUN mkdir /tmp/wikidata
RUN mkdir /output

WORKDIR /tmp/wikidata

COPY extract.py extract.py
COPY run.sh run.sh

RUN chmod +x run.sh
CMD /tmp/wikidata/run.sh
