# 2233recorder

一个基于Linux的直播录播软件，支持多平台、多房间同时录制，提供可视化Web管理界面。

## 🌟 功能特性

### 核心功能
- ✅ **多平台支持**：支持B站、斗鱼、虎牙等主流直播平台
- ✅ **自动监控**：定时检查直播间状态，开播自动录制，下播自动停止
- ✅ **多房间录制**：支持同时录制多个直播间
- ✅ **视频处理**：自动将FLV转换为MP4格式，支持添加自定义水印
- ✅ **Web管理界面**：提供简单直观的Web管理界面，支持查看状态和控制录制
- ✅ **自动更新**：自动下载并更新录播姬

### 技术亮点
- 📱 **响应式设计**：Web界面支持移动端访问
- 📊 **实时监控**：实时显示监控状态和录制进度
- 🔧 **高度可配置**：通过配置文件灵活调整所有参数
- 📦 **模块化设计**：各功能模块独立，便于维护和扩展
- 📚 **完善的API文档**：提供Swagger和ReDoc文档

## 📋 系统要求

- Linux系统（Ubuntu 24.04/Debian 12及以上）
- Python 3.8+
- FFmpeg
- Git

## 🚀 安装步骤

### 1. 安装依赖

#### 安装FFmpeg

Ubuntu/Debian系统：
```bash
sudo apt update
sudo apt install -y ffmpeg
```

CentOS/RHEL系统：
```bash
sudo yum install -y epel-release
sudo yum install -y ffmpeg ffmpeg-devel
```

Arch Linux系统：
```bash
sudo pacman -Syu ffmpeg
```

#### 安装Git

```bash
sudo apt install -y git
```

### 2. 克隆仓库

```bash
git clone https://github.com/Ink-dark/2233recorder.git /opt/2233recorder
cd /opt/2233recorder
```

### 3. 创建虚拟环境并安装依赖

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. 初始化配置文件

```bash
cp config/config.example.yaml config/config.yaml
cp config/rooms.example.yaml config/rooms.yaml
```

### 5. 编辑配置文件

根据需要编辑配置文件：

```bash
# 编辑主配置文件
vim config/config.yaml

# 编辑房间配置文件
vim config/rooms.yaml
```

### 6. 启动服务

```bash
# 直接运行
python -m src.web.app

# 或使用uvicorn
uvicorn src.web.app:app --host 0.0.0.0 --port 8080 --reload
```

## 🎯 使用说明

### 访问Web界面

启动服务后，在浏览器中访问：
```
http://your_server_ip:8080
```

### API文档

- Swagger文档：http://your_server_ip:8080/docs
- ReDoc文档：http://your_server_ip:8080/redoc

### 手动控制

#### 启动监控
```bash
curl http://your_server_ip:8080/api/start_monitor
```

#### 停止监控
```bash
curl http://your_server_ip:8080/api/stop_monitor
```

#### 开始录制指定房间
```bash
curl http://your_server_ip:8080/api/start_recording/bilibili/123456
```

#### 停止录制指定房间
```bash
curl http://your_server_ip:8080/api/stop_recording/bilibili/123456
```

#### 获取系统状态
```bash
curl http://your_server_ip:8080/api/status
```

## 📁 项目结构

```
2233recorder/
├── src/
│   ├── api/          # 平台API封装
│   ├── config/       # 配置管理
│   ├── monitor/      # 监控模块
│   ├── recorder/     # 录制模块
│   ├── processor/    # 视频处理模块
│   ├── web/          # Web管理模块
│   └── utils/        # 工具函数
├── config/           # 配置文件目录
├── logs/             # 日志目录
├── recordings/       # 录制文件目录
├── tests/            # 测试代码
├── README.md         # 项目说明文档
├── CONTRIBUTING.md   # 贡献指南
├── requirements.txt  # 依赖管理文件
└── pyproject.toml    # Python项目配置
```

## 🤝 贡献指南

欢迎各位开发者贡献代码！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献流程和规范。

## 📄 许可证

本项目采用 MIT 许可证，详情请见 [LICENSE](LICENSE) 文件。

## 📞 联系方式

- GitHub Issues: https://github.com/Ink-dark/2233recorder/issues
- 电子邮件: moranqidarkseven@hallochat.cn

## 📊 开发进度

### MVP版本已完成
- [x] 项目初始化
- [x] 配置文件系统
- [x] B站API封装
- [x] 监控核心逻辑
- [x] 录制核心功能
- [x] 视频处理功能
- [x] Web管理界面
- [x] 集成测试

### 后续计划
- [ ] Docker容器部署
- [ ] 多用户权限管理
- [ ] 开放API接口
- [ ] AI辅助剪辑功能
- [ ] 云存储集成

## 📦 录播姬使用说明

2233recorder 使用 [BililiveRecorder](https://github.com/BililiveRecorder/BililiveRecorder) 作为录制核心，具体使用方式如下：

1. **自动下载机制**：系统会从 GitHub 自动下载最新版本的 BililiveRecorder-CLI 可执行文件
2. **独立进程运行**：BililiveRecorder 作为外部独立进程运行，通过命令行调用
3. **无代码集成**：2233recorder 不直接包含或修改 BililiveRecorder 的源代码
4. **配置分离**：每个直播间拥有独立的配置文件，与主程序代码完全分离

这种设计确保了 2233recorder 与 BililiveRecorder 之间的清晰边界，避免了许可证使用纠纷。

## 🙏 致谢

- 感谢 [BililiveRecorder](https://github.com/BililiveRecorder/BililiveRecorder) 提供的录播核心
- 感谢所有为项目做出贡献的开发者