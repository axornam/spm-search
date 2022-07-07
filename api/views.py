import json
from json import encoder
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from txtai.embeddings import Embeddings
import requests

embeddings = Embeddings(
    config={'path': 'sentence-transformers/all-MiniLM-L12-v2'})


def index(request):
    # make request to data endpoint and get data
    r = requests.request(
        "GET", "https://full-spm-api.herokuapp.com/api/v1/projects")
    content = r.content.decode('utf-8')
    # print(r.status_code, r.elapsed, r.content.decode('utf-8'))

    decoder = json.decoder.JSONDecoder()
    jdata = decoder.decode(content)

    # store json file
    with open('data_1.json', 'w') as f:
        json.dump(jdata, f)

    # convert json file to csv
    sentences = [s['abstract'] for s in jdata]
    # for data in jdata:
    # sentences.append(data['abstract'])

    print([len(w.split(' ')) for w in (s for s in sentences)])
    # store the embeddings
    embeddings.index([(uuid, text, None)
                      for uuid, text in enumerate(sentences)])
    embeddings.save('indicies/index1.idx')

    return HttpResponse(encoder.JSONEncoder().encode(sentences))


def add(request):
    return HttpResponse('document added')


def update(request):
    return HttpResponse('document updated')


def remove(request):
    return HttpResponse('document removed')


def query(request, query_string):
    # load sentences from json file
    embeddings.load('indicies/index1.idx')

    sentences = []
    with open("data_1.json", 'r') as f:
        jdata = json.load(f)
        sentences = [s['abstract'] for s in jdata]

    # make query against the embeddings
    result = embeddings.search(query_string)
    # print(sentences)
    print(result)

    # return appropriate search result
    if not sentences:
        return HttpResponse("No Data Matched the Query")

    data = [jdata[r[0]] for r in result]
    data_as_json = dict()

    for k, v in enumerate(data):
        data_as_json[k] = v

    with open('results.json', 'w') as f:
        json.dump(data_as_json, f)

    return JsonResponse((data_as_json))
