from rdflib.term import URIRef
from hgnc2owl.namespace import DefinedNamespace, Namespace


class HGNC(DefinedNamespace):
    """
    HGNC Vocabulary
    """

    _fail = True

    # http://www.w3.org/2002/07/owl#AnnotationProperty
    status: URIRef # status
    locus_group: URIRef # locus_group
    locus_type: URIRef # locus_type
    gene_group: URIRef # gene_group
    gene_group_id: URIRef # gene_group_id
    chromosomal_location: URIRef # chromosomal_location
    symbol: URIRef # symbol
    prev_symbol: URIRef

    # http://www.w3.org/2002/07/owl#Class
    gene: URIRef # gene

    _NS = Namespace("http://purl.bioontology.org/ontology/HGNC/")