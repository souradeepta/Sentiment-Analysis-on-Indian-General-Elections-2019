from datetime import datetime
from elasticsearch import Elasticsearch
import json

es = Elasticsearch(['localhost:9200'])

def write_to_es(data):
    es.index(index="sentiments", body=data)

def backup_from_file():
    with open('../dump/data_es_3.json', 'r') as data_file:
        data_es = json.load(data_file)

        for data in data_es:
            res = es.index(index="sentiments", body=data)

        print('Completed.')


if __name__ == '__main__':
    backup_from_file()