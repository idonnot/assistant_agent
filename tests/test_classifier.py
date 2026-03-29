import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.tools.character_classifier.basic_character_classifier import BasicCharacterClassifier

def test_basic_character_classifier():
    classifier = BasicCharacterClassifier()
    
    test_queries = [
        "南宫婉是谁",
        "介绍一下韩老魔",
        "紫灵和韩立什么关系",
        "今天杭州天气",
        "凡人修仙传好看吗",
        "元瑶的来历"
    ]
    
    print("\n🔍 角色分类器测试")
    print("=" * 50)
    
    for query in test_queries:
        is_fanren, details = classifier.classify(query)
        character = classifier.get_character_from_query(query)
        
        print(f"\n📌 查询: {query}")
        print(f"  涉及角色: {'✅' if is_fanren else '❌'}")
        if character:
            print(f"  提取角色: {character}")
        if details:
            print(f"  详情: {details}")

if __name__ == "__main__":
    test_basic_character_classifier()