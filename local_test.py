import requests
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 测试配置
BASE_URL = "http://localhost:8000"  # 本地测试URL
ABACUS_COOKIE = os.getenv("ABACUS_COOKIE", "")  # 从环境变量获取cookie

if not ABACUS_COOKIE:
    print("警告: 未设置ABACUS_COOKIE环境变量，请在.env文件中设置或直接在脚本中指定")
    ABACUS_COOKIE = input("请输入Abacus cookie: ")

def test_models_endpoint():
    """测试模型列表接口"""
    print("\n=== 测试模型列表接口 ===")
    
    url = f"{BASE_URL}/v1/models"
    headers = {
        "Cookie": ABACUS_COOKIE  # 标准Cookie头
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"可用模型数量: {len(data['data'])}")
            for model in data['data'][:5]:  # 只显示前5个模型
                print(f" - {model['id']}")
            if len(data['data']) > 5:
                print(f" - ... 等{len(data['data'])-5}个模型")
        else:
            print(f"错误: {response.text}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_chat_completion(stream=False):
    """测试聊天完成接口"""
    mode = "流式" if stream else "非流式"
    print(f"\n=== 测试{mode}聊天完成接口 ===")
    
    url = f"{BASE_URL}/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Cookie": ABACUS_COOKIE  # 标准Cookie头
    }
    data = {
        "messages": [
            {"role": "user", "content": "你好，请用一句话介绍自己"}
        ],
        "model": "gpt-4o-abacus",  # 带-abacus后缀的模型名
        "stream": stream
    }
    
    try:
        if not stream:
            # 非流式请求
            response = requests.post(url, headers=headers, json=data)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                print(f"回复内容: {content}")
            else:
                print(f"错误: {response.text}")
        else:
            # 流式请求
            response = requests.post(url, headers=headers, json=data, stream=True)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                print("回复内容: ", end="", flush=True)
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: ') and line != 'data: [DONE]':
                            try:
                                json_str = line[6:]
                                data = json.loads(json_str)
                                content = data['choices'][0]['delta'].get('content', '')
                                if content:
                                    print(content, end="", flush=True)
                            except Exception as e:
                                print(f"\n解析响应失败: {str(e)}")
                print()  # 换行
            else:
                print(f"错误: {response.text}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

if __name__ == "__main__":
    print("Abacus API本地测试工具")
    print("-----------------------")
    
    # 测试模型列表API
    test_models_endpoint()
    
    # 测试非流式聊天完成API
    test_chat_completion(stream=False)
    
    # 测试流式聊天完成API
    test_chat_completion(stream=True)
    
    print("\n测试完成!") 