import requests
import json

from hgnc2owl.ontology import HGNCOntology


def run(args):
    """
    """
    #Opening JSON file
    # f = open('/Users/johardi/Downloads/hgnc_complete_set.json')

    # # returns JSON object as a dictionary
    # data = json.load(f)

    o = HGNCOntology.new()
    for url in args.input_urls:
        json_obj = json.loads(requests.get(url).text)
        data = json_obj
        if 'response' in json_obj:
            data = json_obj['response']['docs']
        for doc in data:
            o = o.mutate(doc)

    o.serialize(args.output)
