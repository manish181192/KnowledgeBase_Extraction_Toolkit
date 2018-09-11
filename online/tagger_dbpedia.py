import spotlight

def get_dbp_id(text, confidence=0.4, support=20):

    annotations = spotlight.annotate('http://spotlight.dbpedia.org/rest/annotate', text, confidence=confidence, support=support)

    dbpUri_list = []
    for a in annotations:
        dbpUri_list.append(a['URI'])
    return dbpUri_list
