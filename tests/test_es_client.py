#!/usr/bin/env python
"""
最简单的ES连接测试
"""

import socket
import requests
from elasticsearch import Elasticsearch

def test_socket():
    """测试socket连接"""
    print("1. 测试Socket连接:")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex(('localhost', 9202))
    if result == 0:
        print("   ✅ Socket连接成功")
    else:
        print(f"   ❌ Socket连接失败 (错误码: {result})")
    sock.close()

def test_requests():
    """测试requests连接"""
    print("\n2. 测试Requests连接:")
    try:
        r = requests.get('http://localhost:9202', timeout=3)
        print(f"   ✅ 状态码: {r.status_code}")
        print(f"   响应内容: {r.json()['cluster_name']}")
        return True
    except Exception as e:
        print(f"   ❌ 失败: {type(e).__name__}: {e}")
        return False

def test_elasticsearch():
    """测试elasticsearch客户端"""
    print("\n3. 测试Elasticsearch客户端:")
    
    try:
        es = Elasticsearch('http://localhost:9202',)
        if es.ping():
            print("   ✅ Elasticsearch连接成功")
        else:
            print("   ❌ Elasticsearch连接失败")

    except Exception as e:
        print(f"   ❌ [方式A] 错误: {e}")


if __name__ == "__main__":
    print("="*50)
    print("ES连接终极测试")
    print("="*50)
    
    test_socket()
    test_requests()
    test_elasticsearch()