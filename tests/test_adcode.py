import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from es_loader.adcode_data_loader import load_excel_to_es
from es_loader.searcher import get_searcher

def test_all():
    """完整测试"""
    print("=" * 50)
    print("开始测试三列数据结构的ES加载和搜索")
    print("=" * 50)
    
    # 1. 加载数据
    print("\n📦 步骤1: 加载Excel数据到ES")
    load_excel_to_es()
    
    # 2. 获取搜索器
    searcher = get_searcher()
    
    # 3. 测试搜索
    print("\n🔍 步骤2: 测试搜索功能")
    test_cases = [
        "浙江省",
        "杭州市", 
        "上城区",
        "杭州",  
        "330102",  
        "西湖",
    ]
    
    for query in test_cases:
        print(f"\n📌 搜索: '{query}'")
        results = searcher.search(query, top_k=3)
        
        if results:
            for r in results:
                print(f"  - {r['full_name']} [{r['level']}] (adcode: {r['adcode']})")
            
            # 测试获取adcode
            adcode = searcher.get_adcode(query)
            weather_loc = searcher.get_weather_location(query)
            print(f"  ✅ 天气查询用: {weather_loc['full_name']} (adcode: {adcode})")
        else:
            print("  ❌ 未找到匹配")
    
    # 4. 测试层级关系
    print("\n🏢 步骤3: 测试层级关系")
    
    # 浙江省
    zhejiang = searcher.get_by_adcode('330000')
    if zhejiang:
        print(f"\n浙江省: {zhejiang['full_name']}")
        cities = searcher.get_children('330000')
        print(f"下辖市数量: {len(cities)}")
        if cities:
            print(f"前5个市: {[c['full_name'] for c in cities[:5]]}")
    
    # 杭州市
    hangzhou = searcher.get_by_adcode('330100')
    if hangzhou:
        print(f"\n杭州市: {hangzhou['full_name']}")
        districts = searcher.get_children('330100')
        print(f"下辖区/县数量: {len(districts)}")
        if districts:
            print(f"前5个区/县: {[d['full_name'] for d in districts[:5]]}")

if __name__ == "__main__":
    # test_all()
    print(get_searcher().get_adcode("西安长安"))