from flask import Flask, render_template, request, url_for, jsonify
from tagger_dexter import get_wiki_id
from tagger_dbpedia import get_dbp_id

from sparql import get_hop_entities, get_hop_entities_dbp


app = Flask(__name__)

@app.route('/wiki/endpoint', methods=['POST'])
def wiki_endpoint():
    input_json = request.get_json(force=True)
    # force=True, above, is necessary if another developer
    # forgot to set the MIME type to 'application/json'
    print('data from client:', input_json)

    wikiId1 =  get_wiki_id(input_json['entity1'])
    wikiId2 = get_wiki_id(input_json['entity2'])
    triples = "Error"
    if len(wikiId1) == 0:
        triples = "Entity1 : No Grounding found in Dexter"
    elif len(wikiId2) == 0:
        triples = "Entity2 : No Grounding found in Dexter"
    else:
        triples = get_hop_entities(wiki1= wikiId1[0], wiki2=wikiId2[0], hop= input_json['hop'])

    dictToReturn = {'answer':triples}
    return jsonify(dictToReturn)


@app.route('/dbpedia/endpoint', methods=['POST'])
def dbpedia_endpoint():
    input_json = request.get_json(force=True)
    # force=True, above, is necessary if another developer
    # forgot to set the MIME type to 'application/json'
    print('data from client:', input_json)

    dbpUri1 =  get_dbp_id(input_json['entity1'])
    dbpUri2 = get_dbp_id(input_json['entity2'])
    triples = "Error"
    if len(dbpUri1) == 0:
        triples = "Entity1 : No Grounding found in Dexter"
    elif len(dbpUri2) == 0:
        triples = "Entity2 : No Grounding found in Dexter"
    else:
        triples = get_hop_entities_dbp(dbp1= dbpUri1[0], dbp2=dbpUri2[0], hop= input_json['hop'])

    dictToReturn = {'answer':triples}
    return jsonify(dictToReturn)


if __name__ == '__main__':
    app.run(debug=True)