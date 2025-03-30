import uvicorn
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

if __name__ == "__main__":
    print("正在启动Abacus API中转服务器...")
    print(f"服务器将在http://localhost:8000运行")
    print("按Ctrl+C停止服务器")
    
    # 从环境变量获取配置，或使用默认值
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    # 启动服务器
    uvicorn.run(
        "abacus:app", 
        host=host, 
        port=port, 
        reload=True,  # 开发模式下启用热重载
        log_level="info"
    ) 