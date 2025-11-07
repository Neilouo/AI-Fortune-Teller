# 安装指南 (Installation Guide)

## 系统要求

- Python 3.8 或更高版本
- pip 包管理器
- OpenAI API Key

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/Neilouo/AI-Fortune-Teller.git
cd AI-Fortune-Teller
```

### 2. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. 安装依赖包

```bash
pip install -r requirements.txt
```

如果遇到网络问题，可以尝试：

```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或者单独安装
pip install streamlit openai python-dotenv pandas numpy lunar-python jieba
```

### 4. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入您的 OpenAI API Key
# Windows:
notepad .env
# Linux/Mac:
nano .env
```

在 `.env` 文件中设置：

```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

### 5. 获取 OpenAI API Key

如果还没有 OpenAI API Key：

1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 注册/登录账号
3. 进入 API Keys 页面
4. 创建新的 API Key
5. 复制 API Key 到 `.env` 文件

## 运行应用

### 启动 Streamlit 应用

```bash
streamlit run app.py
```

应用会自动在浏览器中打开，默认地址为：`http://localhost:8501`

### 命令行选项

```bash
# 指定端口
streamlit run app.py --server.port 8080

# 指定地址（允许外部访问）
streamlit run app.py --server.address 0.0.0.0
```

## 验证安装

运行测试脚本验证核心模块：

```bash
python test_modules.py
```

您应该看到：

```
Running module tests...

✓ PersonalityPrompts tests passed
✓ EmotionEngine tests passed
✓ BaziCalculator tests passed
✓ Analytics tests passed

✅ All available tests passed!
```

## 常见问题

### 1. 导入错误

**问题**：`ModuleNotFoundError: No module named 'xxx'`

**解决**：确保已激活虚拟环境并安装了所有依赖：

```bash
pip install -r requirements.txt
```

### 2. OpenAI API 错误

**问题**：`OpenAI API key not found`

**解决**：
- 检查 `.env` 文件是否存在
- 确认 API Key 正确无误
- 确保 `.env` 文件在项目根目录

### 3. 端口占用

**问题**：`Port 8501 is already in use`

**解决**：使用不同端口：

```bash
streamlit run app.py --server.port 8080
```

### 4. 网络连接问题

**问题**：无法安装依赖或访问 OpenAI API

**解决**：
- 检查网络连接
- 使用国内镜像源安装依赖
- 配置代理（如需要）

### 5. 编码错误

**问题**：中文显示乱码

**解决**：
- 确保终端支持 UTF-8 编码
- Windows 用户可以使用 Windows Terminal 或设置代码页：

```bash
chcp 65001
```

## 开发环境设置

如果您想参与开发：

```bash
# 安装开发依赖
pip install pytest black flake8

# 运行测试
pytest test_modules.py

# 格式化代码
black *.py

# 代码检查
flake8 *.py --max-line-length=120
```

## Docker 部署（可选）

创建 `Dockerfile`：

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

构建和运行：

```bash
# 构建镜像
docker build -t ai-fortune-teller .

# 运行容器
docker run -p 8501:8501 --env-file .env ai-fortune-teller
```

## 更新应用

```bash
# 拉取最新代码
git pull origin main

# 更新依赖（如有变化）
pip install -r requirements.txt --upgrade

# 重启应用
streamlit run app.py
```

## 技术支持

如遇到其他问题：

1. 查看 [GitHub Issues](https://github.com/Neilouo/AI-Fortune-Teller/issues)
2. 提交新的 Issue 描述您的问题
3. 包含错误信息和系统环境信息

---

祝您使用愉快！ 🔮
