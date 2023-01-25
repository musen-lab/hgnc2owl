from hgnc2owl.namespace import HGNC, OBO, OBOINOWL
from stringcase import lowercase, snakecase

from datetime import date
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import OWL, RDF, RDFS, SKOS, XSD, DC, DCTERMS
from rdflib.extras.infixowl import Ontology, Class, Property


class HGNCOntology:
    """HGNC Ontology
    Represents the HUGO Gene Nomenclature Committee (HGNC) Ontology graph that
    can be mutated by supplying the data objects
    """
    def __init__(self, graph=None):
        self.graph = graph

    @staticmethod
    def new():
        g = Graph()
        g.bind('hgnc', HGNC)
        g.bind('obo', OBO)
        g.bind('oboInOwl', OBOINOWL)

        # Ontology properties
        ontology_iri =\
            URIRef("http://purl.bioontology.org/ontology/HGNC/hgnc.owl")
        Ontology(identifier=URIRef(ontology_iri), graph=g)
        today = str(date.today())
        g.add((ontology_iri, OWL.versionInfo, Literal(today)))
        g.add((ontology_iri, OWL.versionIRI,
               URIRef("http://purl.bioontology.org/ontology/HGNC/releases/" +
                      today + "/hgnc.owl")))
        g.add((ontology_iri, DC.title, Literal("HGNC Ontology")))
        g.add((ontology_iri, DC.title,
              Literal("HUGO Gene Nomenclature Committee (HGNC) Ontology")))
        g.add((ontology_iri, RDFS.comment,
              Literal("This OWL file is autogenerated by a program script " +
                      "called hgnc2owl (https://github.com/johardi/hgnc2owl) " +
                      "that takes an input from the publicly available " +
                      "archive files at https://www.genenames.org/download/" +
                      "archive/")))

        # Some declarations
        Class(HGNC.gene, graph=g)
        Property(HGNC.status, baseType=OWL.AnnotationProperty, graph=g)
        Property(HGNC.locus_group, baseType=OWL.AnnotationProperty, graph=g)
        Property(HGNC.locus_type, baseType=OWL.AnnotationProperty, graph=g)
        Property(HGNC.gene_group, baseType=OWL.AnnotationProperty, graph=g)
        Property(HGNC.gene_group_id, baseType=OWL.AnnotationProperty, graph=g)
        Property(HGNC.chromosomal_location, baseType=OWL.AnnotationProperty, graph=g)
        Property(HGNC.symbol, baseType=OWL.AnnotationProperty, graph=g)
        Property(HGNC.prev_symbol, baseType=OWL.AnnotationProperty, graph=g)
        Property(OBO.IAO_0100001, baseType=OWL.AnnotationProperty, graph=g)
        Property(OBOINOWL.hasSynonym, baseType=OWL.AnnotationProperty, graph=g)
        Property(OBOINOWL.hasDbXref, baseType=OWL.AnnotationProperty, graph=g)

        return HGNCOntology(g)

    def mutate(self, doc):
        """
        """
        status = doc['status']
        if status == "Approved":
            self._add_approved_symbol(doc)
        elif status == "Entry Withdrawn" or status == "Merged/Split":
            self._add_withdrawn_symbol(doc)
        return HGNCOntology(self.graph)

    def _add_approved_symbol(self, doc):
        locus_group = doc['locus_group']
        locus_group_name = snakecase(lowercase(locus_group))
        locus_group_id = self._iri(HGNC._NS + locus_group_name)
        locus_group = Class(locus_group_id,
                            subClassOf=[Class(HGNC.gene)],
                            graph=self.graph)
        gene_id = self._get_gene_id(doc)
        Class(gene_id, subClassOf=[locus_group], graph=self.graph)
        self._annotation(gene_id, RDFS.label,
                         self._string(doc['symbol']))
        self._annotation(gene_id, SKOS.prefLabel,
                         self._string(doc['symbol']))
        self._annotation(gene_id, SKOS.altLabel,
                         self._string(doc['name']))
        self._annotation(gene_id, OBOINOWL.id,
                         self._string(doc['hgnc_id']))
        self._annotation(gene_id, DCTERMS.dateAccepted,
                         self._date(doc['date_approved_reserved']))
        self._annotation(gene_id, HGNC.status,
                         self._string(doc['status']))
        self._annotation(gene_id, HGNC.locus_group,
                         self._string(doc['locus_group']))
        self._annotation(gene_id, HGNC.locus_type,
                         self._string(doc['locus_type']))
        self._annotation(gene_id, HGNC.symbol,
                         self._string(doc['symbol']))
        self._source(gene_id, doc['hgnc_id'])

        if 'gene_group' in doc:
            self._gene_group(gene_id, doc['gene_group'])
        if 'gene_group_id' in doc:
            self._gene_group_id(gene_id, doc['gene_group_id'])
        if 'alias_symbol' in doc:
            self._synonym(gene_id, doc['alias_symbol'])
        if 'prev_symbol' in doc:
            self._prev_symbol(gene_id, doc['prev_symbol'])
        if 'pubmed_id' in doc:
            self._references(gene_id, doc['pubmed_id'])
        if 'location' in doc:
            self._annotation(gene_id, HGNC.chromosomal_location,
                             self._string(doc['location']))
        if 'date_modified' in doc:
            self._annotation(gene_id, DCTERMS.modified,
                             self._date(doc['date_modified']))
        if 'vega_id' in doc:
            self._dbxref(gene_id, [doc['vega_id']], "VEGA gene ID")
        if 'rgd_id' in doc:
            self._dbxref(gene_id, doc['rgd_id'], "Rat genome database gene ID")
        if 'mgd_id' in doc:
            self._dbxref(gene_id, doc['mgd_id'], "Mouse genome database gene ID")
        if 'ensembl_gene_id' in doc:
            self._dbxref(gene_id, [doc['ensembl_gene_id']], "Ensembl gene ID")
        if 'entrez_id' in doc:
            self._dbxref(gene_id, [doc['entrez_id']], "Entrez gene ID")
        if 'omim_id' in doc:
            self._dbxref(gene_id, doc['omim_id'], "OMIM ID")
        if 'uniprot_ids' in doc:
            self._dbxref(gene_id, doc['uniprot_ids'], "UniProt ID")
        if 'ccds_id' in doc:
            self._dbxref(gene_id, doc['ccds_id'], "CCDS ID")
        if 'enzyme_id' in doc:
            self._dbxref(gene_id, doc['enzyme_id'], "ENZYME EC accession number")

    def _add_withdrawn_symbol(self, doc):
        withdrawn_group_id = self._iri(HGNC._NS + "withdrawn")
        withdrawn_group = Class(withdrawn_group_id,
                                subClassOf=[Class(HGNC.gene)],
                                graph=self.graph)

        gene_id = self._get_gene_id(doc)
        Class(gene_id, subClassOf=[withdrawn_group], graph=self.graph)

        self._annotation(gene_id, RDFS.label,
                         self._string(doc['symbol']))
        self._annotation(gene_id, HGNC.symbol,
                         self._string(doc['symbol']))
        self._annotation(gene_id, HGNC.status,
                         self._string(doc['status']))
        self._annotation(gene_id, OWL.deprecated,
                         self._boolean("true"))

        if "merged_into_reports" in doc:
            for replaced_symbol in doc['merged_into_reports']:
                replacement_gene_id = self._get_gene_id(replaced_symbol)
                self._annotation(gene_id, OBO.IAO_0100001, replacement_gene_id)

    def _get_gene_id(self, obj):
        hgnc_id = obj['hgnc_id']
        hgnc_numerical_id = hgnc_id.split(":")[1]
        return self._iri("http://identifiers.org/hgnc/" + hgnc_numerical_id)

    def _dbxref(self, subject, values, comment):
        for value in values:
            self._annotation(subject, OBOINOWL.hasDbXref,
                             self._string(value),
                             self._string(comment))

    def _gene_group(self, subject, values):
        for value in values:
            self._annotation(subject, HGNC.gene_group, self._string(value))

    def _gene_group_id(self, subject, values):
        for value in values:
            self._annotation(subject, HGNC.gene_group_id, self._string(value))

    def _synonym(self, subject, values):
        for value in values:
            self._annotation(subject, SKOS.altLabel, self._string(value))

    def _prev_symbol(self, subject, values):
        for value in values:
            self._annotation(subject, HGNC.prev_symbol, self._string(value))

    def _references(self, subject, values):
        for value in values:
            source = "PMID:" + str(value)
            self._annotation(subject, DCTERMS.references, self._string(source))

    def _source(self, subject, hgnc_id):
        hgnc_numerical_id = hgnc_id.split(":")[1]
        url = "https://www.genenames.org/data/gene-symbol-report/#!/" +\
              "hgnc_id/" + str(hgnc_numerical_id)
        self._annotation(subject, DCTERMS.source, self._string(url))

    def _annotation(self, subject, property, value, comment=None):
        self.graph.add((subject, property, value))
        if comment is not None:
            # Add annotation of annotation
            bn = BNode()
            self.graph.add((bn, RDF.type, OWL.Axiom))
            self.graph.add((bn, OWL.annotatedSource, subject))
            self.graph.add((bn, OWL.annotatedProperty, property))
            self.graph.add((bn, OWL.annotatedTarget, value))
            self.graph.add((bn, RDFS.comment, comment))

    def _iri(self, str):
        return URIRef(str)

    def _string(self, str):
        return Literal(str, datatype=XSD.string)

    def _date(self, str):
        return Literal(str, datatype=XSD.date)

    def _boolean(self, str):
        return Literal(str, datatype=XSD.boolean)

    def serialize(self, destination):
        """
        """
        self.graph.serialize(format='ttl', destination=destination)
