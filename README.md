# HGNC-to-OWL

A Python tool to convert HGNC dataset to OWL format.

## Installation
```
$ git clone https://github.com/musen-lab/hgnc2owl.git
$ cd hgnc2owl
$ pip install .
```

## Running command
```
$ hgnc2owl http://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json \
           http://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/withdrawn.json \
           -o hgnc.owl
```
