from elasticsearch import Elasticsearch
from config.settings import ES_HOST, ES_PORT, ES_SCHEME

def get_es_client():
    """Create and return an Elasticsearch client instance."""
    es = Elasticsearch(
        [{"host": ES_HOST, "port": ES_PORT, "scheme": ES_SCHEME}]
    )
    return es


def create_index(es: Elasticsearch, index_name: str, mapping: dict) -> Elasticsearch:
    """Create ES index with mapping"""
    # delete index if exists
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
    
    # create index with mapping
    es.indices.create(index=index_name, mappings=mapping['mappings'], settings=mapping['settings'])
    print(f"Index {index_name} created with mapping")
    
    return es

def delete_index(es: Elasticsearch, index_name: str):
    """Delete ES index if exists"""
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        print(f"Index {index_name} has been deleted")


if __name__ == "__main__":
    """Test ES connection and index management"""
    es = get_es_client()
    print("Connected to ES:", es.ping())