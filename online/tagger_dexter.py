import urllib2
import urllib
import numpy as np
import json

def send_request(text, n=50, wn="false", debug="false", format="text", min_conf="0.5"):
    url = "http://localhost:8080/dexter-webapp/api/rest/annotate?"

    dict = {}
    dict["text"] = text
    dict["n"] = n
    dict["wn"] = wn
    dict["debug"] = debug
    dict["format"] = format
    dict["min-conf"] = min_conf

    # for text
    data = urllib.urlencode(dict)

    request = urllib2.Request(url, data)
    f = urllib2.urlopen(request)
    result = f.read()
    return result
def get_wiki_id(title):
    result = send_request(title)
    spots = json.loads(result)['spots']

    wiki_spots = []
    for spot in spots:
        if 'linkProbability' in spot.keys() and float(spot['linkProbability'])<0.5:
            wiki_spots.append(str(spot['entity']))
            # + '\t' + str(spot['linkProbability']))
    print(str(wiki_spots))
    return wiki_spots