from SPARQLWrapper import SPARQLWrapper, JSON

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

# def get_dbpedia_uri(wiki_id):
#     query="select ?uri where {?uri dbo:wikiPageID "+str(wiki_id)+" .} LIMIT 10"
#     results = sparql_query(query=query)
#     labels=['uri']
#     uri_col = get_rows_result(results,labels)
#     if len(uri_col)==0:
#         print("No DBPedia Entity : "+ str(wiki_id))
#         return ""
#     return uri_col[0][0]


def get_hop_entities(wiki1, wiki2, hop=-1):
    # uri1=pid_dbpUri[pid1]
    # uri2=pid_dbpUri[pid2]
    triplets=[]
    query=""
    if hop == 0 or hop==-1:
        # Predicate
        # [ product1 rel product2]
        query="PREFIX dbO: <http://dbpedia.org/ontology/> "\
               "PREFIX dbR: <http://dbpedia.org/resource/> "\
               "select distinct ?rel where{ " \
               "?uri1 dbo:wikiPageID " + wiki1 + " ." \
               "?uri2 dbo:wikiPageID "+wiki2+" ."\
               "<uri1> ?rel_uri <uri2> . "\
               "?rel_uri rdfs:label ?rel . "\
               "FILTER (lang(?rel) = 'en')}"
        labels=['rel']
        result = sparql_query(query)
        rel_rows=get_rows_result(result,labels)
        if len(rel_rows)>0:
            for rel in rel_rows:

                triplets.append(wiki1+'\t'+rel[0]+'\t'+wiki2)

    if hop==1 or hop==-1:
        #Every Row will be a predicate
        # [ product1 rel1 e]
        # [ product2 rel2 e]

        #                "PREFIX dbo: <http://dbpedia.org/ontology/> "\
                #"PREFIX dbR: <http://dbpedia.org/resource/> "\

        query="PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "\
                "select distinct ?e,?rel1, ?rel2 where{ "\
                "?uri1 dbo:wikiPageID "+wiki1+" ."\
                "?uri2 dbo:wikiPageID "+wiki2+" ."\
                "<uri1> ?rel_uri1 ?e_uri . "\
                "<uri2> ?rel_uri2 ?e_uri . "\
                "?e_uri rdfs:label ?e . "\
                "?rel_uri1 rdfs:label ?rel1 . " \
                "?rel_uri2 rdfs:label ?rel2 . " \
                "FILTER (lang(?rel1) = 'en') .  " \
                "FILTER (lang(?rel2) = 'en') . " \
                "FILTER (lang(?e) = 'en') . }"
        labels=['e','rel1','rel2']
        result=sparql_query(query)
        rows=get_rows_result(result,labels)
        if len(rows)>0:
            for row in rows:
                triplets.append(wiki1+'\t'+row[1]+'\t'+row[0])
                triplets.append(wiki2+'\t'+row[2]+'\t'+row[0])
    return triplets

def get_hop_entities_dbp(dbp1, dbp2, hop=-1):
    uri1=dbp1
    uri2=dbp2
    triplets=[]
    query=""
    if hop == 0 or hop==-1:
        # Predicate
        # [ product1 rel product2]
        query="PREFIX dbO: <http://dbpedia.org/ontology/> "\
               "PREFIX dbR: <http://dbpedia.org/resource/> "\
               "select distinct ?rel where{ "\
               "<"+uri1+"> ?rel_uri <"+uri2+"> . "\
               "?rel_uri rdfs:label ?rel . "\
               "FILTER (lang(?rel) = 'en')}"
        labels=['rel']
        result = sparql_query(query)
        rel_rows=get_rows_result(result,labels)
        if len(rel_rows)>0:
            for rel in rel_rows:

                triplets.append(pid1+'\t'+rel[0]+'\t'+pid2)

    if hop==1 or hop==-1:
        #Every Row will be a predicate
        # [ product1 rel1 e]
        # [ product2 rel2 e]

        #                "PREFIX dbo: <http://dbpedia.org/ontology/> "\
                #"PREFIX dbR: <http://dbpedia.org/resource/> "\

        query="PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "\
                "select distinct ?e,?rel1, ?rel2 where{ "\
                "<"+uri1+"> ?rel_uri1 ?e_uri . "\
                "<"+uri2+"> ?rel_uri2 ?e_uri . "\
                "?e_uri rdfs:label ?e . "\
                "?rel_uri1 rdfs:label ?rel1 . " \
                "?rel_uri2 rdfs:label ?rel2 . " \
                "FILTER (lang(?rel1) = 'en') .  " \
                "FILTER (lang(?rel2) = 'en') . " \
                "FILTER (lang(?e) = 'en') . }"
        labels=['e','rel1','rel2']
        result=sparql_query(query)
        rows=get_rows_result(result,labels)
        if len(rows)>0:
            for row in rows:
                triplets.append(pid1+'\t'+row[1]+'\t'+row[0])
                triplets.append(pid2+'\t'+row[2]+'\t'+row[0])
    return triplets


'''
@ WORKING pair query 0-hop
select ?rel, ?uri1, ?uri2 where{
    ?uri1 dbo:wikiPageID 25970423 .
    ?uri2 dbo:wikiPageID 8841749 .
    ?uri1 ?rel_uri ?uri2 .
    ?rel_uri rdfs:label ?rel .     
}

@WORKING 1-hop query
select ?e,?rel1, ?rel2, ?p1, ?p2 where{
    ?uri1 dbo:wikiPageID 44501 .
    ?uri2 dbo:wikiPageID 676909 .
    ?uri1 ?rel_uri1 ?e_uri .
    ?uri2 ?rel_uri2 ?e_uri .

    ?e_uri rdfs:label ?e .
    ?rel_uri1 rdfs:label ?rel1 .
    ?rel_uri2 rdfs:label ?rel2 .
    ?uri1 rdfs:label ?p1 .
    ?uri2 rdfs:label ?p2 .

    FILTER (lang(?rel1) = 'en')
    FILTER (lang(?rel2) = 'en')
    FILTER (lang(?e) = 'en')
    FILTER (lang(?p1) = 'en')    
    FILTER (lang(?p2) = 'en')
}
'''