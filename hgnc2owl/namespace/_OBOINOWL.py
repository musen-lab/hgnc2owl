from rdflib.term import URIRef
from hgnc2owl.namespace import DefinedNamespace, Namespace


class OBOINOWL(DefinedNamespace):
    """
    HGNC Vocabulary
    """

    _fail = True

    # http://www.w3.org/2002/07/owl#AnnotationProperty
    id: URIRef
    hasAlternativeId: URIRef
    hasDate: URIRef
    hasVersion: URIRef
    hasDbXref: URIRef
    hasDefaultNamespace: URIRef
    hasOBONamespace: URIRef
    hasDefinition: URIRef
    hasSynonym: URIRef
    hasExactSynonym: URIRef
    hasNarrowSynonym: URIRef
    hasBroadSynonym: URIRef
    hasRelatedSynonym: URIRef
    hasSynonymType: URIRef
    hasSubset: URIRef
    hasURI: URIRef
    isCyclic: URIRef
    inSubset: URIRef
    savedBy: URIRef
    replacedBy: URIRef
    consider: URIRef

    # http://www.w3.org/2002/07/owl#ObjectProperty
    ObsoleteProperty: URIRef

    # http://www.w3.org/2002/07/owl#Class
    DbXref: URIRef
    Definition: URIRef
    Subset: URIRef
    Synonym: URIRef
    SynonymType: URIRef
    ObsoleteClass: URIRef

    _NS = Namespace("http://www.geneontology.org/formats/oboInOwl#")