# Abacus API 中转脚本部署指南 (Vercel)

本文档提供了如何将Abacus API中转脚本部署到Vercel平台的详细步骤。

## 前提条件

1. 一个[Vercel账户](https://vercel.com/signup)
2. 安装[Vercel CLI](https://vercel.com/docs/cli)（可选，用于本地开发和测试）
3. 一个[GitHub](https://github.com/)、[GitLab](https://gitlab.com/)或[BitBucket](https://bitbucket.org/)账户（用于代码托管）

## 步骤1：准备项目代码

### 确保文件结构如下

```
project/
├── abacus.py           # 主应用代码
├── index.py            # Vercel入口文件
├── requirements.txt    # 依赖项列表
├── vercel.json         # Vercel配置文件
└── .env                # 环境变量配置（本地开发用，不会上传到Vercel）
```

## 步骤2：配置环境变量

在Vercel部署时，需要在Vercel项目设置中配置以下环境变量：

- `BASE_URL`：Abacus API基础URL，默认为"https://apps.abacus.ai"
- `DEPLOYMENT_ID`：部署ID（必填）
- `EXTERNAL_APP_ID`：外部应用ID（必填）
- `MAX_CONCURRENT_REQUESTS`：最大并发请求数，建议设置为30
- `CONNECT_TIMEOUT`：连接超时时间（秒），建议设置为10.0
- `STREAM_TIMEOUT`：流式响应超时时间（秒），建议设置为120.0

## 步骤3：部署到Vercel

### 使用Vercel网页界面部署

1. 首先，将项目代码推送到一个Git仓库（GitHub、GitLab或BitBucket）

2. 登录[Vercel](https://vercel.com/)，点击"New Project"

3. 导入你的Git仓库，选择包含API中转脚本的仓库

4. 配置项目:
   - 框架预设选择"Other"
   - 构建命令留空
   - 输出目录留空
   - 安装命令保持默认`pip install -r requirements.txt`
   
5. 环境变量:
   - 点击"Environment Variables"
   - 添加上面"步骤2"中列出的所有必要环境变量
   
6. 点击"Deploy"开始部署

### 使用Vercel CLI部署

1. 安装Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. 登录到Vercel:
   ```bash
   vercel login
   ```

3. 在项目目录中初始化:
   ```bash
   vercel
   ```
   
4. 按照提示设置项目名称、团队等信息

5. 部署时添加环境变量:
   ```bash
   vercel --env BASE_URL=https://apps.abacus.ai --env DEPLOYMENT_ID=your_deployment_id --env EXTERNAL_APP_ID=your_app_id --env MAX_CONCURRENT_REQUESTS=30 --env CONNECT_TIMEOUT=10.0 --env STREAM_TIMEOUT=120.0
   ```

## 步骤4：测试部署

部署完成后，你会得到一个Vercel生成的URL（例如`https://your-project.vercel.app`）。

使用以下命令测试API是否正常工作:

```bash
curl -X GET https://your-project.vercel.app/v1/models
```

或发送一个简单的聊天请求:

```bash
curl -X POST https://your-project.vercel.app/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello, how are you?"}],
    "model": "gpt-4o-abacus",
    "cookie": "your_abacus_cookie_here"
  }'
```

## 注意事项

1. **环境变量安全**：
   - 确保敏感环境变量在Vercel项目设置中标记为"隐藏"
   - 不要将敏感信息存储在代码仓库中

2. **无服务器环境限制**：
   - Vercel无服务器函数有冷启动时间
   - 函数执行有时间限制（最长60秒）
   - 连接可能会因为无服务器函数的特性而中断

3. **监控**：
   - 使用Vercel提供的日志和监控工具检查应用性能
   - 定期检查函数执行情况和错误日志

4. **持久会话**：
   - 在无服务器环境中，会话状态不会持久保存
   - 每个函数调用可能使用新的实例，导致会话状态丢失
   - 考虑使用Vercel KV或外部数据库来存储会话信息

## 故障排除

如果遇到问题，请检查：

1. 环境变量是否正确配置
2. 依赖项是否正确安装（检查requirements.txt）
3. Vercel日志中是否有错误信息
4. 是否存在超时问题（调整CONNECT_TIMEOUT和STREAM_TIMEOUT）

更多帮助，请参考[Vercel文档](https://vercel.com/docs)或[FastAPI在Vercel上的部署指南](https://vercel.com/guides/deploying-fastapi-with-vercel) 