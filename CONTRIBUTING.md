# 贡献指南

感谢您考虑为2233recorder项目做出贡献！本指南将帮助您了解如何参与项目开发。

## 📝 如何提交问题

### Bug报告

如果您发现了Bug，请按照以下格式提交Issue：

**标题**：简明扼要地描述问题

**内容**：
- 环境信息（操作系统版本、Python版本、FFmpeg版本）
- 详细的问题描述
- 重现步骤
- 预期行为
- 实际行为
- 错误日志（如果有）
- 截图（如果有）

### 功能请求

如果您有新功能建议，请按照以下格式提交Issue：

**标题**：简明扼要地描述功能

**内容**：
- 功能描述
- 功能价值（解决了什么问题）
- 实现思路（可选）
- 参考链接（如果有）

## 🛠️ 如何贡献代码

### 1. Fork仓库

首先，您需要Fork本仓库到您的GitHub账号下：

1. 访问项目主页：https://github.com/Ink-dark/2233recorder
2. 点击右上角的"Fork"按钮

### 2. 克隆Fork后的仓库

```bash
git clone https://github.com/your_username/2233recorder.git
cd 2233recorder
```

### 3. 创建分支

根据您要解决的问题或实现的功能，创建一个新的分支：

```bash
# 修复Bug
 git checkout -b bugfix/issue-number

# 实现新功能
 git checkout -b feature/feature-name

# 文档更新
 git checkout -b docs/document-name
```

### 4. 安装开发依赖

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .[dev]
```

### 5. 开发和测试

- 编写代码，遵循项目的代码规范
- 运行测试，确保代码通过所有测试
- 编写新的测试用例（如果添加了新功能）

### 6. 提交代码

提交代码前，请确保：
- 代码遵循PEP 8规范
- 所有测试通过
- 代码有适当的注释
- 提交信息清晰明了

提交信息格式：

```
type(scope): description

optional body

optional footer
```

**type**：
- feat: 新功能
- fix: Bug修复
- docs: 文档更新
- style: 代码格式调整（不影响功能）
- refactor: 代码重构（不影响功能）
- test: 测试代码
- chore: 构建过程或辅助工具的变动

**scope**：
- api: API相关
- config: 配置相关
- monitor: 监控模块
- recorder: 录制模块
- processor: 视频处理模块
- web: Web管理模块
- utils: 工具函数

**示例**：

```
feat(web): 添加直播间状态实时更新功能

- 实现WebSocket连接
- 添加状态更新API
- 优化前端显示

closes #123
```

### 7. 推送分支

```bash
git push origin your-branch-name
```

### 8. 创建Pull Request

1. 访问您Fork的仓库
2. 点击"Pull Request"按钮
3. 填写Pull Request标题和描述
4. 关联相关Issue
5. 提交Pull Request

### 9. 代码审查

- 项目维护者会对您的代码进行审查
- 您可能需要根据审查意见进行修改
- 修改后再次提交，系统会自动更新Pull Request

### 10. 合并代码

代码审查通过后，项目维护者会将您的代码合并到主分支。

## 🔧 代码规范

### Python代码规范

- 遵循PEP 8规范
- 变量名使用小写字母+下划线（snake_case）
- 函数名使用小写字母+下划线（snake_case）
- 类名使用首字母大写（CamelCase）
- 常量名使用全部大写+下划线（UPPER_CASE）
- 每行代码不超过100个字符
- 使用4个空格进行缩进
- 函数和类都要有文档字符串
- 关键操作要有日志记录

### JavaScript代码规范

- 遵循ESLint推荐规范
- 变量名使用驼峰命名法（camelCase）
- 函数名使用驼峰命名法（camelCase）
- 类名使用首字母大写（CamelCase）
- 常量名使用全部大写+下划线（UPPER_CASE）
- 每行代码不超过100个字符
- 使用2个空格进行缩进

### 文档规范

- 文档使用Markdown格式
- 文档结构清晰，有适当的标题和章节
- 代码示例要完整可运行
- API文档要包含参数说明、返回值说明和示例

## 🧪 测试要求

### 单元测试

- 所有新功能都必须添加对应的单元测试
- 单元测试覆盖率目标：80%以上
- 测试文件放在`tests`目录下
- 测试文件名格式：`test_*.py`
- 测试函数名格式：`test_*`
- 测试类名格式：`Test*`

### 集成测试

- 新功能必须通过集成测试
- 集成测试脚本：`tests/test_integration.py`

### 运行测试

```bash
# 运行所有测试
pytest

# 运行指定测试文件
pytest tests/test_bilibili_api.py

# 运行指定测试函数
pytest tests/test_bilibili_api.py::test_bilibili_api

# 查看覆盖率
pytest --cov=src
```

## 🌿 分支管理策略

- **main**：主分支，用于发布稳定版本
- **develop**：开发分支，整合各个功能分支
- **feature/***：功能分支，用于开发新功能
- **bugfix/***：Bug修复分支，用于修复Bug
- **release/***：发布分支，用于准备发布

## 📚 文档贡献

### API文档

- API文档使用FastAPI自动生成
- 所有API端点都必须有文档字符串
- 文档字符串要包含功能描述、参数说明、返回值说明和示例

### 示例代码

- 示例代码要完整可运行
- 示例代码要包含详细的注释
- 示例代码要放在`examples`目录下

## 🎯 开发流程

1. **规划**：在Issue中讨论功能或Bug修复
2. **开发**：按照分支管理策略创建分支，编写代码
3. **测试**：运行测试，确保代码通过所有测试
4. **提交**：按照提交信息规范提交代码
5. **审查**：创建Pull Request，等待代码审查
6. **合并**：代码审查通过后，合并到主分支
7. **发布**：定期从main分支发布新版本

## 💡 开发建议

1. 从小功能开始，逐步熟悉项目结构
2. 查看现有代码，了解项目的代码风格和架构
3. 参与Issue讨论，了解项目的发展方向
4. 关注项目的Pull Request，学习其他开发者的代码
5. 定期更新您的Fork，保持与主仓库同步

## 📞 联系方式

- GitHub Issues：https://github.com/Ink-dark/2233recorder/issues
- 电子邮件：moranqidarkseven@hallochat.cn

## 📄 许可证

通过贡献代码，您同意您的贡献将按照项目的MIT许可证发布。

再次感谢您的贡献！🎉