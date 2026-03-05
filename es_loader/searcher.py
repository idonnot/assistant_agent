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
            # 层1：adcode精确匹配（最高权重）
            {
                "term": {
                    "adcode": {
                        "value": query,
                        "boost": 6
                    }
                }
            },
            
            # # 层2：cross_fields匹配（关键改进）
            # {
            #     "multi_match": {
            #         "query": query,
            #         "fields": ["full_name^3", "name^2"],
            #         "type": "cross_fields",
            #         "operator": "and",  
            #         "boost": 5
            #     }
            # },
            
            # 层3：full_name AND匹配（要求所有词都出现）
            {
                "match": {
                    "full_name": {
                        "query": query,
                        "analyzer": "ik_smart",  # 使用ik_smart减少重复分词导致的高分
                        "operator": "and",
                        "boost": 4
                    }
                }
            },
            
            # 层4：name动词or匹配（单字段容错）
            {
                "match": {
                    "name": {
                        "query": query,
                        "analyzer": "ik_smart",
                        "operator": "or",
                        "boost": 3
                    }
                }
            },
            
            # # 层5：前缀匹配
            # {
            #     "prefix": {
            #         "name": {
            #             "value": query,
            #             "analyzer": "ik_smart",
            #             "boost": 2
            #         }
            #     }
            # },
            
            # 层6：模糊匹配（容错）
            {
                "match": {
                    "full_name": {
                        "query": query,
                        "analyzer": "ik_smart",
                        "fuzziness": "AUTO",
                        "boost": 1
                    }
                }
            }
        ]
        
        search_body = {
            "query": {
                "bool": {
                    "should": should_conditions,
                    "minimum_should_match": 1
                }
            },
            "sort": [
                {"_score": "desc"}
            ],
            "size": top_k
        }
        
        result = self.es.search(index=ES_INDEX, body=search_body)
        return self._format_results(result)
    
    def get_adcode(self, location_text):
        """
        Get the adcode for a given location text.
        Returns a structured dict with 'status', 'adcode', and optional 'error' or 'candidates'.
        """
        results = self.search(location_text, top_k=5)
        
        if not results:
            return {"status": "not_found", "error": f"未找到位置 '{location_text}'"}
        print(results)
        
        duplicate_results = self.check_duplicate_city(results)
        
        if duplicate_results['status'] == 'ambiguous':
            return {
                "status": "ambiguous",
                "error": f"位置 '{location_text}' 存在歧义，可能指以下位置中的一个：{', '.join(duplicate_results['candidates'])}。请提供更具体的位置信息（例如添加上级行政区）以获取准确的天气信息。",
                "candidates": duplicate_results['candidates']
            }
        
        return {
            "status": "ok",
            "adcode": results[0]['adcode'],
            "location": results[0]['full_name'],
            "level": results[0]['level']
        }
    

    def get_weather_location(self, location_text):
        """
        Get the most relevant location info for weather queries, prioritizing district > city > province
        """
        results = self.search(location_text, top_k=5)
        
        if not results:
            return None
        
        # Province
        return {
            'adcode': results[0]['adcode'],
            'full_name': results[0]['full_name'],
            'citycode': '',
            'level': 'province'
        }
    
    def check_duplicate_city(self, top_k_list):
        # get the highest score from the top_k results
        max_score = top_k_list[0]["score"]

        # get all results that have a score close to the max score (e.g., within 0.01)
        top_results = [
            r for r in top_k_list
            if abs(r["score"] - max_score) < 2
        ]

        # if there are multiple results with similar high scores, it may indicate ambiguity
        if len(top_results) > 1:
            return {
                "status": "ambiguous",
                "candidates": [
                    r["full_name"] for r in top_results
                ]
            }

        # only one clear winner
        return {
            "status": "ok",
            "adcode": top_k_list[0]["adcode"]
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