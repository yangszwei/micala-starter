#!/usr/bin/env python3

from zipfile import ZipFile
import csv
import json
import os
import requests


def send_request(path, host="http://localhost:9200", method="GET", headers=None, data=None, silent=False):
    """
    Send HTTP request to elasticsearch server
    """
    url = f"{host}{path}"
    if data is not None:
        headers = {'Content-Type': 'application/json'}
    response = requests.request(method, url, headers=headers, data=data)
    if not silent and response.status_code >= 400:
        print(url, method, response.text)
    return response.json()


def create_index(index, host="http://localhost:9200", force=False):
    """
    Create index with pipeline
    """
    if not force and get_index(index) is not None:
        print(f"Index {index} already exists, skipping...")
        return
    print(f"Creating index {index}...")
    headers = {'Content-Type': 'application/json'}
    with open(f"../configs/elasticsearch/indices/{index}.json", 'r', encoding='utf-8-sig') as f:
        send_request(f"/{index}", host, "PUT", headers, f.read())
    with open(f"../configs/elasticsearch/indices/{index}-pipeline.json", 'r', encoding='utf-8-sig') as f:
        send_request(f"/_ingest/pipeline/{index}-pipeline", host, "PUT", headers, f.read())


def get_index(index, host="http://localhost:9200"):
    """
    Get all indices
    """
    response = send_request(f"/{index}", host=host, silent=True)
    if "error" in response:
        if response["error"]["type"] == "index_not_found_exception":
            return None
        raise Exception(response["error"]["reason"])
    return response


def upload_docs(index, filepath, host="http://localhost:9200", force=False):
    """
    Upload documents to elasticsearch server
    """
    if not force:
        response = send_request(f"/{index}/_count", host=host, silent=True)
        if "count" in response and response["count"] > 0:
            print(f"Index {index} is not empty, skipping...")
            return
    print(f"Uploading documents to index {index}...")

    path = f"/{index}/_bulk?pipeline={index}-pipeline"
    headers={'Content-Type': 'application/x-ndjson'}
    data = ""
    with open(filepath, 'r', encoding='utf-8-sig') as file:
        for row in file:
            data += json.dumps({"index": {}}) + "\n"
            data += json.dumps({"message": row.strip()}) + "\n"
    send_request(path, host=host, method="POST", headers=headers, data=data)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with ZipFile("../configs/elasticsearch/terms.zip", 'r') as zipObj:
        zipObj.extractall("../configs/elasticsearch")
    create_index("my-terms", force=False)
    upload_docs("my-terms", "../configs/elasticsearch/allterms.csv", force=False)
    create_index("radlexterm", force=False)
    upload_docs("radlexterm", "../configs/elasticsearch/radlexStem.csv", force=False)
