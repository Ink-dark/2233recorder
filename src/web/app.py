from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import os
from src.config.config import config_manager
from src.monitor.monitor import monitor
from src.recorder.core import Recorder
from src.processor.converter import VideoConverter
from src.processor.watermark import WatermarkAdder

# 初始化配置
config_manager.load_config()
config_manager.load_rooms()

# 创建FastAPI应用
app = FastAPI(
    title="2233recorder API",
    description="A Linux-based live streaming recorder with web management interface",
    version="0.1.0"
)

# 初始化核心组件
recorder = Recorder()
converter = VideoConverter()
watermark_adder = WatermarkAdder()

# 挂载静态文件目录
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 根路径返回HTML页面
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>2233recorder</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f0f0f0;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                .status {
                    margin: 20px 0;
                    padding: 10px;
                    border-radius: 4px;
                }
                .status.online {
                    background-color: #d4edda;
                    color: #155724;
                }
                .status.offline {
                    background-color: #f8d7da;
                    color: #721c24;
                }
                .btn {
                    display: inline-block;
                    padding: 10px 20px;
                    margin: 5px;
                    background-color: #007bff;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    border: none;
                    cursor: pointer;
                }
                .btn:hover {
                    background-color: #0056b3;
                }
                .btn-danger {
                    background-color: #dc3545;
                }
                .btn-danger:hover {
                    background-color: #c82333;
                }
                .rooms {
                    margin: 20px 0;
                }
                .room-item {
                    margin: 10px 0;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }
                .api-docs {
                    margin-top: 30px;
                    text-align: center;
                }
                .loading {
                    color: #666;
                    font-style: italic;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>2233recorder</h1>
                
                <div class="status" id="monitor-status">
                    <strong>监控状态:</strong> <span id="monitor-status-text" class="loading">加载中...</span>
                    <br>
                    <strong>监控线程数:</strong> <span id="monitor-threads">-</span>
                    <br>
                    <strong>监控间隔:</strong> <span id="monitor-interval">-</span>秒
                </div>
                
                <div>
                    <button onclick="startMonitor()" class="btn">启动监控</button>
                    <button onclick="stopMonitor()" class="btn btn-danger">停止监控</button>
                </div>
                
                <div class="rooms">
                    <h2>直播间列表</h2>
                    <div id="rooms-list" class="loading">加载中...</div>
                </div>
                
                <div class="api-docs">
                    <a href="/docs" class="btn">API文档</a>
                    <a href="/redoc" class="btn">ReDoc文档</a>
                </div>
            </div>
            
            <script>
                // 获取系统状态
                async function getStatus() {
                    try {
                        const response = await fetch('/api/status');
                        const data = await response.json();
                        return data;
                    } catch (error) {
                        console.error('获取状态失败:', error);
                        return null;
                    }
                }
                
                // 更新监控状态
                function updateMonitorStatus(data) {
                    const statusDiv = document.getElementById('monitor-status');
                    const statusText = document.getElementById('monitor-status-text');
                    const threadsSpan = document.getElementById('monitor-threads');
                    const intervalSpan = document.getElementById('monitor-interval');
                    
                    if (data.monitor.is_running) {
                        statusDiv.className = 'status online';
                        statusText.textContent = '运行中';
                    } else {
                        statusDiv.className = 'status offline';
                        statusText.textContent = '已停止';
                    }
                    
                    threadsSpan.textContent = data.monitor.monitor_threads_count;
                    intervalSpan.textContent = data.monitor.interval;
                }
                
                // 更新直播间列表
                function updateRoomsList(data) {
                    const roomsList = document.getElementById('rooms-list');
                    
                    if (data.rooms.length === 0) {
                        roomsList.innerHTML = '<p>没有配置的直播间</p>';
                        return;
                    }
                    
                    let html = '';
                    data.rooms.forEach(room => {
                        html += `
                        <div class="room-item">
                            <strong>${room.name || '未知主播'}</strong> (${room.platform} - ${room.room_id})
                            <br>
                            状态: ${room.status}
                            <br>
                            <button onclick="startRecording('${room.platform}', '${room.room_id}')" class="btn">开始录制</button>
                            <button onclick="stopRecording('${room.platform}', '${room.room_id}')" class="btn btn-danger">停止录制</button>
                        </div>
                        `;
                    });
                    
                    roomsList.innerHTML = html;
                }
                
                // 更新页面数据
                async function updateData() {
                    const data = await getStatus();
                    if (data) {
                        updateMonitorStatus(data);
                        updateRoomsList(data);
                    }
                }
                
                // 启动监控
                async function startMonitor() {
                    try {
                        await fetch('/api/start_monitor');
                        updateData();
                    } catch (error) {
                        console.error('启动监控失败:', error);
                        alert('启动监控失败');
                    }
                }
                
                // 停止监控
                async function stopMonitor() {
                    try {
                        await fetch('/api/stop_monitor');
                        updateData();
                    } catch (error) {
                        console.error('停止监控失败:', error);
                        alert('停止监控失败');
                    }
                }
                
                // 开始录制
                async function startRecording(platform, roomId) {
                    try {
                        await fetch(`/api/start_recording/${platform}/${roomId}`);
                        updateData();
                    } catch (error) {
                        console.error('开始录制失败:', error);
                        alert('开始录制失败');
                    }
                }
                
                // 停止录制
                async function stopRecording(platform, roomId) {
                    try {
                        await fetch(`/api/stop_recording/${platform}/${roomId}`);
                        updateData();
                    } catch (error) {
                        console.error('停止录制失败:', error);
                        alert('停止录制失败');
                    }
                }
                
                // 初始化页面
                updateData();
                
                // 每5秒自动更新数据
                setInterval(updateData, 5000);
            </script>
        </body>
    </html>
    """

# API端点

@app.get("/api/status")
async def get_status():
    """
    获取系统状态
    """
    monitor_status = monitor.get_monitor_status()
    rooms = config_manager.get_rooms()
    
    # 获取每个房间的录制状态
    for room in rooms:
        recording_status = recorder.get_recording_status(room)
        room["status"] = recording_status["status"]
    
    return {
        "system": {
            "name": config_manager.get("system.name"),
            "version": config_manager.get("system.version"),
            "log_level": config_manager.get("system.log_level")
        },
        "monitor": monitor_status,
        "rooms": rooms,
        "recorder": {
            "record_processes_count": len(recorder.record_processes)
        }
    }

@app.get("/api/start_monitor")
async def start_monitor():
    """
    启动监控
    """
    monitor.start()
    return {"message": "监控已启动"}

@app.get("/api/stop_monitor")
async def stop_monitor():
    """
    停止监控
    """
    monitor.stop()
    return {"message": "监控已停止"}

@app.get("/api/start_recording/{platform}/{room_id}")
async def start_recording(platform: str, room_id: str):
    """
    开始录制指定房间
    """
    room = None
    for r in config_manager.get_rooms():
        if r.get("platform") == platform and r.get("room_id") == room_id:
            room = r
            break
    
    if not room:
        raise HTTPException(status_code=404, detail="直播间未找到")
    
    # 调用录制核心开始录制
    result = recorder.start_recording(room, "", room.get("name"))
    if result:
        return {"message": f"已开始录制 {platform} 房间 {room_id}"}
    else:
        raise HTTPException(status_code=500, detail=f"录制 {platform} 房间 {room_id} 失败")

@app.get("/api/stop_recording/{platform}/{room_id}")
async def stop_recording(platform: str, room_id: str):
    """
    停止录制指定房间
    """
    room = None
    for r in config_manager.get_rooms():
        if r.get("platform") == platform and r.get("room_id") == room_id:
            room = r
            break
    
    if not room:
        raise HTTPException(status_code=404, detail="直播间未找到")
    
    # 调用录制核心停止录制
    result = recorder.stop_recording(room)
    if result:
        return {"message": f"已停止录制 {platform} 房间 {room_id}"}
    else:
        raise HTTPException(status_code=500, detail=f"停止录制 {platform} 房间 {room_id} 失败")

@app.get("/api/rooms")
async def get_rooms():
    """
    获取所有直播间配置
    """
    rooms = config_manager.get_rooms()
    
    # 获取每个房间的录制状态
    for room in rooms:
        recording_status = recorder.get_recording_status(room)
        room["status"] = recording_status["status"]
    
    return {"rooms": rooms}

@app.get("/api/room/{room_id}")
async def get_room(room_id: str):
    """
    获取指定直播间配置
    """
    room = config_manager.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="直播间未找到")
    
    # 获取录制状态
    recording_status = recorder.get_recording_status(room)
    room["status"] = recording_status["status"]
    
    return room

# 主函数
if __name__ == "__main__":
    host = config_manager.get("web.host", "0.0.0.0")
    port = config_manager.get("web.port", 8080)
    
    print(f"Starting 2233recorder API server on http://{host}:{port}")
    print(f"API documentation available at http://{host}:{port}/docs")
    print(f"Web interface available at http://{host}:{port}")
    
    uvicorn.run(
        "src.web.app:app",
        host=host,
        port=port,
        reload=True
    )