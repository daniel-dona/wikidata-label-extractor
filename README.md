# wikidata-label-extractor

# The problem

Processing large numbers of triples can be slow, especially if they are not already indexed in some triplet store capable of returning the desired subset in a reasonable time.

In our case we want to get all the `rdfs:label` and `rdfs:altLabel` properties from Wikidata, which is done from the regular dumps in TTL (~ 700GB). 

# The solution

Using pipes we can download, decompress and filter the triples in a continuous flow of about 15MB/s, but that is still slow and takes about 12 hours. The bottleneck is the filtering part, that hits the processor single-thread limit.

As a solution, a mechanism has been designed to partition the TTL file and thus parallelize the filtering of its triples with an arbitrary number of threads, at the user's discretion.

Effectively, with 20 threads, the time has been reduced to just over half an hour. 
