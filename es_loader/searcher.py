from elasticsearch import Elasticsearch
from es_loader.es_utils import get_es_client
from config.settings import ES_INDEX

class LocationSearcher:
    """Location searcher for administrative divisions"""
    
    def __init__(self):
        self.es = get_es_client()
    
    def search(self, query, level=None, top_k=10):
        """
        Search for locations by name or adcode, with optional level filtering
        
        Args:
            query: keyword to search (can be name or adcode)
            level: filter by administrative level (province/city/district)
            top_k: return top N results
        """
        
        should_conditions = [
            {
                "match": {
                    "full_name": {
                        "query": query,
                        "boost": 3
                    }
                }
            },
            {
                "match": {
                    "name": {
                        "query": query,
                        "boost": 2
                    }
                }
            },
            {
                "prefix": {
                    "name": {
                        "value": query,
                        "boost": 1.5
                    }
                }
            },
            {
                "term": {
                    "adcode": {
                        "value": query,
                        "boost": 5
                    }
                }
            }
        ]
        
        # filter by level if specified
        filters = []
        if level:
            filters.append({"term": {"level": level}})
        
        search_body = {
            "query": {
                "bool": {
                    "should": should_conditions,
                    "filter": filters,
                    "minimum_should_match": 1
                }
            },
            "sort": [
                {"_score": "desc"},
                {"level_rank": "desc"}
            ],
            "size": top_k
        }
        
        result = self.es.search(index=ES_INDEX, body=search_body)
        return self._format_results(result)
    
    def get_adcode(self, location_text):
        """
        Get the adcode for a given location text, prioritizing district > city > province for weather queries
        """
        results = self.search(location_text, top_k=5)
        
        if not results:
            return None
        
        # district > city > province
        for level in ['district', 'city', 'province']:
            for result in results:
                if result['level'] == level:
                    return result['adcode']
        
        return results[0]['adcode']
    

    def get_weather_location(self, location_text):
        """
        Get the most relevant location info for weather queries, prioritizing district > city > province
        """
        results = self.search(location_text, top_k=5)
        
        if not results:
            return None
        
        # Priority: district > city > province
        for result in results:
            if result['level'] == 'district':
                return {
                    'adcode': result['adcode'],
                    'full_name': result['full_name'],
                    'citycode': result.get('citycode', ''),
                    'level': 'district'
                }
        
        for result in results:
            if result['level'] == 'city':
                return {
                    'adcode': result['adcode'],
                    'full_name': result['full_name'],
                    'citycode': result.get('citycode', ''),
                    'level': 'city'
                }
        
        # Province
        return {
            'adcode': results[0]['adcode'],
            'full_name': results[0]['full_name'],
            'citycode': '',
            'level': 'province'
        }
    
    def get_by_adcode(self, adcode):
        """Get location info by adcode"""
        try:
            result = self.es.get(index=ES_INDEX, id=adcode)
            return result['_source']
        except:
            return None
        
    
    def get_children(self, adcode):
        """Get child locations by parent adcode (e.g., get all districts under a city)"""
        doc = self.get_by_adcode(adcode)
        if not doc or 'children_adcodes' not in doc:
            return []
        
        children = []
        for child_adcode in doc['children_adcodes']:
            child = self.get_by_adcode(child_adcode)
            if child:
                children.append(child)
        
        return children
    

    def _format_results(self, es_response):
        """Format ES search results into a more readable structure"""
        formatted = []
        for hit in es_response['hits']['hits']:
            source = hit['_source']
            formatted.append({
                'score': hit['_score'],
                'adcode': source['adcode'],
                'name': source['name'],
                'full_name': source.get('full_name', source['name']),
                'province': source.get('province_name', ''),
                'city': source.get('city_name', ''),
                'district': source.get('district_name', ''),
                'level': source['level'],
                'citycode': source.get('citycode', '')
            })
        return formatted


_location_searcher = None

def get_searcher():
    """Get a singleton instance of LocationSearcher"""
    global _location_searcher
    if _location_searcher is None:
        _location_searcher = LocationSearcher()
    return _location_searcher