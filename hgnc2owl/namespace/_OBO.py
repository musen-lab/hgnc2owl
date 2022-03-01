from rdflib.term import URIRef
from hgnc2owl.namespace import DefinedNamespace, Namespace


class OBO(DefinedNamespace):
    """
    OBO Vocabulary
    """

    _fail = True

    # http://www.w3.org/2002/07/owl#ObjectProperty

    # http://www.w3.org/2002/07/owl#DataProperty

    # http://www.w3.org/2002/07/owl#AnnotationProperty

    # http://www.w3.org/2002/07/owl#Class
    IAO_0100001: URIRef  # term replaced by

    _NS = Namespace("http://purl.obolibrary.org/obo/")