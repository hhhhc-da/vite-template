import os
import requests
import time
import yaml

API_BASE_URL = "http://localhost:83/v1"

BASE_CONFIG_PATH = "D:\\Code\\Python\\Oumi\\cfg"
CONFIG_PATH = os.path.join(BASE_CONFIG_PATH, "token.yaml")

VALID_API_KEY = ""

try:
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        TOKEN = yaml.safe_load(f.read())
        VALID_API_KEY = TOKEN['token']
except Exception as e:
    print(f"✗ 加载 YAML 配置失败：{str(e)}")
    raise

INVALID_API_KEY = "123456"
SUPPORTED_MODEL = "HuggingFaceTB/SmolLM2-135M-Instruct"

def get_headers(api_key: str = VALID_API_KEY):
    """生成带有 Authorization 头的请求头字典"""
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

def test_api_functionality():
    """
    一个综合性的测试函数，验证 API 的所有核心功能。
    包括：API Key 验证、模型列表、聊天补全（单轮、多轮、参数控制）。
    """
    headers = get_headers()
    all_passed = True

    print("\n--- 测试 1: API Key 验证 ---")
    try:
        response = requests.get(f"{API_BASE_URL}/models")
        assert response.status_code == 401
        assert "未提供 API Key" in response.json()["detail"]
        print("✓ 未提供 API Key -> 401")

        invalid_headers = get_headers(INVALID_API_KEY)
        response = requests.get(f"{API_BASE_URL}/models", headers=invalid_headers)
        assert response.status_code == 401
        assert "无效的 API Key" in response.json()["detail"]
        print("✓ 无效 API Key -> 401")
    except Exception as e:
        print(f"✗ API Key 验证失败: {e}")
        all_passed = False

    print("\n--- 测试 2: 模型列表 ---")
    try:
        response = requests.get(f"{API_BASE_URL}/models", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "data" in data and isinstance(data["data"], list)
        assert len(data["data"]) > 0
        model = data["data"][0]
        assert model["id"] == SUPPORTED_MODEL
        print(f"✓ 成功获取模型列表，支持的模型: {SUPPORTED_MODEL}")
    except Exception as e:
        print(f"✗ 模型列表测试失败: {e}")
        all_passed = False

    print("\n--- 测试 3: 基本聊天补全 ---")
    try:
        payload = {
            "model": SUPPORTED_MODEL,
            "messages": [{"role": "user", "content": "你好，请介绍一下自己。"}]
        }
        response = requests.post(f"{API_BASE_URL}/chat/completions", headers=headers, json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "choices" in data and len(data["choices"]) > 0
        content = data["choices"][0]["message"]["content"]
        assert isinstance(content, str) and len(content.strip()) > 0
        print(f"✓ 成功生成回复: {content[:50]}...")
    except Exception as e:
        print(f"✗ 基本聊天补全失败: {e}")
        all_passed = False

    print("\n--- 测试 4: 模型名验证 ---")
    try:
        payload = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "你好"}]
        }
        response = requests.post(f"{API_BASE_URL}/chat/completions", headers=headers, json=payload)
        assert response.status_code == 400
        assert "不支持的模型" in response.json()["detail"]
        print("✓ 不支持的模型 -> 400")
    except Exception as e:
        print(f"✗ 模型名验证失败: {e}")
        all_passed = False

    print("\n--- 测试 5: 多轮对话上下文 ---")
    try:
        payload1 = {"model": SUPPORTED_MODEL, "messages": [{"role": "user", "content": "我的名字叫小明。"}]}
        reply1 = requests.post(f"{API_BASE_URL}/chat/completions", headers=headers, json=payload1).json()["choices"][0]["message"]["content"]
        
        payload2 = {
            "model": SUPPORTED_MODEL,
            "messages": [
                {"role": "user", "content": "我的名字叫小明。"},
                {"role": "assistant", "content": reply1},
                {"role": "user", "content": "你知道我叫什么名字吗？"}
            ]
        }
        response2 = requests.post(f"{API_BASE_URL}/chat/completions", headers=headers, json=payload2)
        assert response2.status_code == 200
        reply2 = response2.json()["choices"][0]["message"]["content"].lower()
        print(f"✓ 多轮对话流程完成。模型回复: {reply2[:50]}...")
    except Exception as e:
        print(f"✗ 多轮对话测试失败: {e}")
        all_passed = False

    print("\n--- 测试 6: 生成参数控制 (max_tokens) ---")
    try:
        payload = {
            "model": SUPPORTED_MODEL,
            "messages": [{"role": "user", "content": "请写一个很长的故事。"}],
            "max_tokens": 10
        }
        response = requests.post(f"{API_BASE_URL}/chat/completions", headers=headers, json=payload)
        assert response.status_code == 200
        content = response.json()["choices"][0]["message"]["content"]
        assert len(content.split()) <= 20
        print(f"✓ max_tokens 参数生效。生成短回复: {content}")
    except Exception as e:
        print(f"✗ max_tokens 参数测试失败: {e}")
        all_passed = False

    # 最终断言
    assert all_passed, "部分测试用例失败，请查看详细输出。"
    print("\n✓✓✓ 所有测试用例均通过！")

if __name__ == "__main__":
    print("请确保 FastAPI 服务已在 http://localhost:83 启动！")
    time.sleep(2)
    
    test_api_functionality()