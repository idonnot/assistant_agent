import pandas as pd
from elasticsearch import helpers
from es_loader.es_utils import get_es_client, create_index
from config.settings import ES_INDEX, ADCODE_EXCEL_PATH

MAPPING = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "ik_smart_analyzer": {
                        "type": "custom",
                        "tokenizer": "ik_smart"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                # BASE FIELDS
                "name": {
                    "type": "text",
                    "analyzer": "ik_smart_analyzer",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "adcode": {
                    "type": "keyword"
                },
                "level": {
                    "type": "keyword"
                },
                "level_rank":{
                    "type": "integer"
                },
                "citycode": {
                    "type": "keyword"
                },
                
                # level-specific fields for better search and filtering
                "province_name": {"type": "keyword"},
                "province_adcode": {"type": "keyword"},
                "city_name": {"type": "keyword"},
                "city_adcode": {"type": "keyword"},
                "district_name": {"type": "keyword"},
                "district_adcode": {"type": "keyword"},
                
                # full name field for better search relevance, analyzed with IK for flexible matching
                "full_name": {
                    "type": "text",
                    "analyzer": "ik_smart_analyzer",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                
                # parent-child relationships for hierarchical queries (e.g., find all districts under a city)
                "children_adcodes": {
                    "type": "keyword"
                }
            }
        }
    }


def load_excel_to_es(excel_path=None):
    """load city data from Excel and import to Elasticsearch"""
    if excel_path is None:
        excel_path = ADCODE_EXCEL_PATH
    
    # read Excel file
    df = pd.read_excel(excel_path, dtype={'中文名': str, 'adcode': str, 'citycode': str})
    print(f"Read {len(df)} rows from Excel file")
    
    # preprocess data
    df = preprocess_data(df)
    
    # connect to ES and import data
    es = get_es_client()
    if not es.ping():
        print("[Error] Cannot connect to Elasticsearch")
        return
    create_index(es, ES_INDEX, MAPPING)  # create index with mapping
    
    # import data to ES with progress logging
    docs = generate_documents(df)  # generate documents and build parent-child relationships
    
    bulk_insert(es, docs, ES_INDEX)  # bulk insert documents into ES
    

def preprocess_data(df):
    """Process the DataFrame to ensure it has the necessary structure and fields for ES indexing"""
    # rename columns to standard names
    df.columns = ['name', 'adcode', 'citycode']
    
    # make sure adcode is string and zero-padded to 6 digits
    df['adcode'] = df['adcode'].astype(str).str.zfill(6)
    
    # deal with missing citycode values
    df['citycode'] = df['citycode'].replace(['null', 'None', 'nan'], '').fillna('')
    
    # add level field based on adcode patterns
    df['level'] = df['adcode'].apply(determine_level)
    
    # Add province and city information based on adcode patterns
    df = extract_hierarchy(df)
    
    return df

def determine_level(adcode):
    """Determine the administrative level based on adcode patterns:"""
    if adcode.endswith('0000'):
        return 'province'
    elif adcode.endswith('00'):
        return 'city'
    else:
        return 'district'
    

def extract_hierarchy(df):
    """Extract province and city information based on adcode patterns and create new fields for ES indexing"""
    # create mapping of adcode to province and city names for easy lookup
    province_map = {}  # adcode : province_name
    city_map = {}      # adcode : city_name
    
    # Find all provinces and cities first to build the mapping
    for _, row in df.iterrows():
        adcode = row['adcode']
        name = row['name']
        
        if row['level'] == 'province':
            province_map[adcode] = name
        elif row['level'] == 'city':
            city_map[adcode] = name
    
    # add new fields for province and city information
    df['province_name'] = ''
    df['province_adcode'] = ''
    df['city_name'] = ''
    df['city_adcode'] = ''
    df['full_name'] = ''
   
    
    for idx, row in df.iterrows():
        adcode = row['adcode']
        level = row['level']
        
        if level == 'province':
            # level is province, just fill in province fields
            df.at[idx, 'province_name'] = row['name']
            df.at[idx, 'province_adcode'] = adcode
            df.at[idx, 'full_name'] = row['name']
            
        elif level == 'city':
            # level is city, find the corresponding province
            province_adcode = adcode[:2] + '0000'
            df.at[idx, 'province_name'] = province_map.get(province_adcode, '')
            df.at[idx, 'province_adcode'] = province_adcode
            df.at[idx, 'city_name'] = row['name']
            df.at[idx, 'city_adcode'] = adcode
            df.at[idx, 'full_name'] = f"{province_map.get(province_adcode, '')}{row['name']}"
            
        else:  
            # district level, find corresponding province and city
            province_adcode = adcode[:2] + '0000'
            city_adcode = adcode[:4] + '00'
            
            df.at[idx, 'province_name'] = province_map.get(province_adcode, '')
            df.at[idx, 'province_adcode'] = province_adcode
            df.at[idx, 'city_name'] = city_map.get(city_adcode, '')
            df.at[idx, 'city_adcode'] = city_adcode
            df.at[idx, 'full_name'] = f"{province_map.get(province_adcode, '')}{city_map.get(city_adcode, '')}{row['name']}"
    
    return df


def generate_documents(df) -> dict:
    """
    Generate ES documents from the DataFrame, ensuring proper structure and parent-child relationships for administrative divisions
    
    Returns:
        {adcode: document} dictionary where key is adcode and value is the corresponding ES document ready for indexing
    """
    documents = {}
    
    for _, row in df.iterrows():
        adcode = row['adcode']
        level = row['level']
        level_map = {
            "province": 1,
            "city": 2,
            "district": 3
        }
        level_rank = level_map.get(level, 0)    
        name = row['name']
        citycode = row['citycode']
        
        doc = {
            "name": name,
            "adcode": adcode,
            "level": level,
            "level_rank": level_rank,
            "citycode": citycode,
            "province_name": row['province_name'],
            "province_adcode": row['province_adcode'],
            "city_name": row['city_name'],
            "city_adcode": row['city_adcode'],
            "full_name": row['full_name']
        }
        
        documents[adcode] = doc
    
    # build parent-child relationships based on adcode patterns
    for adcode, doc in documents.items():
        if doc['level'] == 'city':
            # city-level document: find its province
            parent_adcode = doc['province_adcode']
            if parent_adcode in documents:
                if 'children_adcodes' not in documents[parent_adcode]:
                    documents[parent_adcode]['children_adcodes'] = []
                documents[parent_adcode]['children_adcodes'].append(adcode)
        
        elif doc['level'] == 'district':
            # district-level document: find its city
            parent_adcode = doc['city_adcode']
            if parent_adcode in documents:
                if 'children_adcodes' not in documents[parent_adcode]:
                    documents[parent_adcode]['children_adcodes'] = []
                documents[parent_adcode]['children_adcodes'].append(adcode)
    
    return documents


def bulk_insert(es, docs, index_name, chunk_size=500):
    """
    Bulk insert documents into Elasticsearch
    
    :param es: Elasticsearch client
    :param docs: dict {doc_id: document}
    :param index_name: index name
    :param chunk_size: batch size
    """

    success_count = 0

    actions = []

    for doc_id, doc in docs.items():
        action = {
            "_index": index_name,
            "_id": doc_id,
            "_source": doc
        }
        actions.append(action)

    try:
        # helpers.bulk returns a tuple of (success_count, failed_items)
        success, failed = helpers.bulk(
            es,
            actions,
            chunk_size=chunk_size,
            request_timeout=60
        )

        success_count = success
        print(f"[✓] Successfully inserted {success_count} documents")

        if failed:
            print(f"[!] Failed documents: {failed}")

    except Exception as e:
        print(f"[Error] Bulk insert failed: {e}")

    return success_count