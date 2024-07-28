from fastapi import FastAPI, HTTPException
from elasticsearch import Elasticsearch
from typing import List

app = FastAPI()

es = Elasticsearch([{"host": "localhost", "port": 9200}])


@app.get("/search/discussion")
def search_discussions(query: str):
    try:
        result = es.search(
            index="discussions",
            body={
                "query": {
                    "multi_match": {"query": query, "fields": ["text", "hashtags"]}
                }
            },
        )
        return result["hits"]["hits"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search/user")
def search_discussions(query: str):
    try:
        result = es.search(
            index="users",
            body={
                "query": {
                    "multi_match": {"query": query, "fields": ["name", "email"]}
                }
            },
        )
        return result["hits"]["hits"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def _health_check():
    return {"message": "Search Service is running"}
