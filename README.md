# 🔮 AI算命大师 (AI Fortune Teller)

基于大语言模型的AI算命产品，融合八字计算与心理共鸣对话，提升用户娱乐体验。

## 📊 项目成果

- ✅ **100+** 用户体验
- ✅ **62%** 用户停留时长提升（相比传统算命应用）
- ✅ **4.7/5** 满意度评分
- ✅ 三种人格化AI对话体验
- ✅ 即时生成命理与心理双维报告

## ✨ 核心特性

### 1. 智能八字计算
- 基于传统命理学的八字计算系统
- 自动分析五行分布和强弱
- 生成性格特征和运势预测

### 2. 三种AI人格
构建人格化Prompt体系，提供不同风格的对话体验：

- **🧠 理性大师**：客观理性，注重逻辑分析和科学解读
- **💕 温柔大师**：温暖体贴，善于情感共鸣和心理安慰
- **⚡ 毒舌大师**：直言不讳，犀利幽默，以独特方式点醒用户

### 3. 情感分析引擎
- 采用情感词典和规则引擎
- 实时识别用户情绪状态
- 智能调整对话风格和回应策略
- 确保对话流畅自然

### 4. 双维度报告生成
- **命理报告**：全面分析事业、感情、财运、健康等维度
- **心理报告**：基于对话内容的深度心理分析

### 5. 优化的用户体验
- Streamlit前端界面，简洁美观
- 优化的用户输入流程
- 即时反馈和互动
- 会话数据追踪和分析

## 🚀 快速开始

### 环境要求

- Python 3.8+
- OpenAI API Key

### 本地运行

1. **克隆仓库**
```bash
git clone https://github.com/Neilouo/AI-Fortune-Teller.git
cd AI-Fortune-Teller
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
cp .env.example .env
# 编辑.env文件，填入您的OpenAI API Key
```

4. **运行应用**
```bash
streamlit run app.py
```

5. **访问应用**
打开浏览器访问 `http://localhost:8501`

### 部署到 Streamlit Cloud

1. **Fork 本仓库**到您的 GitHub 账号

2. **在 Streamlit Cloud 创建应用**
   - 访问 [share.streamlit.io](https://share.streamlit.io)
   - 选择您 fork 的仓库
   - 主文件路径：`app.py`

3. **配置 Secrets**
   - 点击应用的 "Settings" → "Secrets"
   - 添加以下内容：
   ```toml
   OPENAI_API_KEY = "your_openai_api_key_here"
   OPENAI_MODEL = "gpt-3.5-turbo"
   ```

4. **部署完成**
   - Streamlit Cloud 会自动安装依赖并启动应用
   - 您的应用将获得一个公开访问链接

## 📖 使用指南

### 第一步：选择AI人格
根据您的偏好选择三种大师风格之一：
- 理性大师：适合需要客观分析的用户
- 温柔大师：适合需要情感支持的用户
- 毒舌大师：适合需要直接建议的用户

### 第二步：输入生辰信息
- 选择出生日期
- 选择出生时辰（0-23时）
- 系统自动计算八字和五行

### 第三步：开始对话
- 可以询问事业、感情、财运等任何问题
- AI会根据您的八字和对话情感智能回应
- 支持连续对话，建立深入交流

### 第四步：生成报告
- 生成命理分析报告：全面的命理解读
- 生成心理分析报告：基于对话的心理洞察

### 第五步：评分反馈
为您的体验评分，帮助我们持续改进

## 🏗️ 技术架构

### 核心模块

```
AI-Fortune-Teller/
├── app.py                      # Streamlit主应用
├── ai_fortune_teller.py        # AI算命核心模块
├── bazi_calculator.py          # 八字计算模块
├── personality_prompts.py      # 人格提示词模板库
├── emotion_engine.py           # 情感分析引擎
├── analytics.py                # 用户分析模块
├── requirements.txt            # 依赖包列表
└── README.md                   # 项目文档
```

### 技术栈

- **前端框架**：Streamlit
- **AI模型**：OpenAI GPT (支持自定义模型)
- **命理计算**：lunar-python (农历和干支计算)
- **情感分析**：jieba (中文分词) + 自定义情感词典
- **数据分析**：pandas, numpy

### 设计模式

- **情感识别**：基于词典匹配和规则引擎
- **对话管理**：上下文管理和历史记录
- **人格系统**：模板化Prompt设计
- **报告生成**：结构化提示词工程

## 📊 数据统计与分析

系统自动记录以下数据：
- 用户会话数量
- 平均停留时长
- 交互次数统计
- 满意度评分
- 人格选择分布
- 话题关注度

数据存储在 `user_analytics.json` 中，用于产品优化。

## 🎨 人格模板示例

### 理性大师示例
```
用户：我最近工作压力很大，怎么办？
理性大师：从命理角度来看，您的八字显示...综合分析，建议您...
```

### 温柔大师示例
```
用户：我最近工作压力很大，怎么办？
温柔大师：亲爱的，我理解你现在的压力💕。从你的八字来看...相信会越来越好的✨
```

### 毒舌大师示例
```
用户：我最近工作压力很大，怎么办？
毒舌大师：说实话吧，压力大是因为...听我一句劝，你得...别再自己为难自己了。
```

## 📄 PRD与模板文档

### 产品需求文档 (PRD)
详细的产品需求文档请参考 [PRD.md](./docs/PRD.md)，包含：
- 产品定位与目标
- 用户画像分析
- 功能需求详述
- 技术实现方案
- 数据指标定义
- 迭代规划路线

### AI人格模板库
完整的人格模板库请参考 [PERSONALITY_TEMPLATES.md](./docs/PERSONALITY_TEMPLATES.md)，包含：
- 三种基础人格详细设定
- 对话示例库
- 场景化应对策略
- 扩展人格设计指南

## 🔒 隐私与安全

- 所有用户数据仅用于改进产品体验
- 不会分享或出售用户信息
- 支持本地部署，完全控制数据
- 建议妥善保管OpenAI API Key

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 📮 联系方式

- 项目维护者：[@Neilouo](https://github.com/Neilouo)
- 问题反馈：[GitHub Issues](https://github.com/Neilouo/AI-Fortune-Teller/issues)

## 🙏 致谢

感谢所有参与测试和反馈的用户！

---

**免责声明**：本项目仅供娱乐和学习使用，算命结果仅供参考，请理性看待。重要决策请结合实际情况慎重考虑。