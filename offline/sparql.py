from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Literal, Namespace, URIRef

def add_dbpedia_triplets(wiki_id):
    query="select ?s ?p ?o where {?s dbo:wikiPageID "+str(wiki_id)+" . ?s ?p ?o .} LIMIT 10"
    query_results = sparql_query(query=query)

    results = query_results["results"]["bindings"]
    for result in results:
        subj = result['s']['value']
        rel = result['p']['value']
        obj = result['o']['value']
        grph.add((URIRef(subj),URIRef(rel),URIRef(obj)))
        grph.add((URIRef(obj), URIRef(rel), URIRef(subj)))

    return True

def query_graph(URI1,URI2):

    # # qres = grph.query(
    #     """SELECT ?s ?p ?o
    #        WHERE {
    #           ?s ?p ?o .
    #        }""")
    qres = grph.query(
        """SELECT ?s ?p ?o
           WHERE {
              """+URI1+ """ ?p1 ?o1 ."""
                +"""?s2 ?p2 """+URI2+""" .
           }"""
    )
    for row in qres:
        print(row)

def sparql_query(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery(query)  # the previous query as a literal string

    return sparql.query().convert()

def get_rows_result(results, labels):
    rows=[]
    bad_set={'Link from a Wikipage to another Wikipage'}
    for result in results["results"]["bindings"]:
        temp=[]
        flag=False
        for label in labels:
            if result[label]["value"] in bad_set:
                flag=True
                break
            temp.append(result[label]["value"])
        if not flag:
            rows.append(temp)
    return rows



def get_facts_associated(wikiId):
    """

    :param wikiId:
    :return: returns all facts found in dbpedia as a list of tuples
    """

    # change query
    query = "PREFIX dbO: <http://dbpedia.org/ontology/> " \
            "PREFIX dbR: <http://dbpedia.org/resource/> " \
            "select distinct ?rel where{ " \
            "?uri1 dbo:wikiPageID " + wikiId + " ." \
                                              "?uri2 dbo:wikiPageID " + wiki2 + " ." \
                                                                                "<uri1> ?rel_uri <uri2> . " \
                                                                                "?rel_uri rdfs:label ?rel . " \
                                                                                "FILTER (lang(?rel) = 'en')}"

    triplets = []
    labels = ['rel']
    result = sparql_query(query)
    rel_rows = get_rows_result(result, labels)
    if len(rel_rows) > 0:
        for rel in rel_rows:
            triplets.append(wikiId + '\t' + rel[0] + '\t' + obj)

grph = Graph()
add_dbpedia_triplets(wiki_id=25970423)
