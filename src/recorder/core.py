import os
import subprocess
import time
import json
from typing import Dict, Any, Optional
from src.recorder.updater import RecorderUpdater


class Recorder:
    """
    录制核心类
    """
    
    def __init__(self):
        """
        初始化录制核心
        """
        self.updater = RecorderUpdater()
        self.record_processes = {}  # 存储正在运行的录制进程
    
    def start_recording(self, room: Dict[str, Any], title: str, anchor_name: str) -> Optional[subprocess.Popen]:
        """
        开始录制
        
        Args:
            room: 房间配置
            title: 直播间标题
            anchor_name: 主播名称
            
        Returns:
            Optional[subprocess.Popen]: 录制进程实例，失败返回None
        """
        room_id = room.get("room_id")
        platform = room.get("platform", "bilibili")
        room_key = f"{platform}_{room_id}"
        
        # 检查录播姬是否已安装，如未安装则自动下载
        if not self._check_recorder(platform):
            print(f"录播姬未安装或无法更新，无法录制 {platform} 房间 {room_id}")
            return None
        
        # 创建录制配置
        record_config = self._create_record_config(room, title, anchor_name)
        if not record_config:
            return None
        
        # 获取录播姬可执行文件路径
        recorder_path = self.updater.get_executable_path("bililive_recorder")
        if not recorder_path:
            return None
        
        try:
            # 启动录制进程
            process = subprocess.Popen(
                [recorder_path, "run", record_config["work_dir"]],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(recorder_path)
            )
            
            # 保存进程信息
            self.record_processes[room_key] = {
                "process": process,
                "config": record_config,
                "start_time": time.time()
            }
            
            print(f"已启动录制进程，PID: {process.pid}")
            return process
        
        except Exception as e:
            print(f"启动录制进程失败: {e}")
            return None
    
    def stop_recording(self, room: Dict[str, Any]) -> bool:
        """
        停止录制
        
        Args:
            room: 房间配置
            
        Returns:
            bool: 停止成功返回True，失败返回False
        """
        room_id = room.get("room_id")
        platform = room.get("platform", "bilibili")
        room_key = f"{platform}_{room_id}"
        
        if room_key not in self.record_processes:
            print(f"没有找到 {platform} 房间 {room_id} 的录制进程")
            return False
        
        try:
            process_info = self.record_processes[room_key]
            process = process_info["process"]
            
            # 终止进程
            process.terminate()
            
            # 等待进程结束
            process.wait(timeout=10)
            
            # 清理资源
            del self.record_processes[room_key]
            
            print(f"已停止录制进程，PID: {process.pid}")
            return True
        
        except subprocess.TimeoutExpired:
            # 超时未结束，强制终止
            process.kill()
            process.wait(timeout=5)
            del self.record_processes[room_key]
            print(f"已强制终止录制进程，PID: {process.pid}")
            return True
        
        except Exception as e:
            print(f"停止录制进程失败: {e}")
            return False
    
    def _check_recorder(self, platform: str) -> bool:
        """
        检查录播姬是否已安装，如未安装则自动下载
        
        Args:
            platform: 平台类型
            
        Returns:
            bool: 录播姬可用返回True，否则返回False
        """
        # 目前仅支持B站录播姬
        if platform == "bilibili":
            return self.updater.check_and_update("bililive_recorder")
        else:
            print(f"暂不支持 {platform} 平台的自动安装录播姬")
            return False
    
    def _create_record_config(self, room: Dict[str, Any], title: str, anchor_name: str) -> Optional[Dict[str, Any]]:
        """
        创建录制配置
        
        Args:
            room: 房间配置
            title: 直播间标题
            anchor_name: 主播名称
            
        Returns:
            Optional[Dict[str, Any]]: 录制配置字典，失败返回None
        """
        room_id = room.get("room_id")
        platform = room.get("platform", "bilibili")
        room_name = room.get("name", f"房间{room_id}")
        
        # 录制输出目录
        output_dir = room.get("output_dir")
        if not output_dir:
            output_dir = os.path.join("/opt/2233recorder/recordings", platform, room_id)
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 录播姬工作目录
        work_dir = self.updater.recorder_configs["bililive_recorder"]["work_dir"]
        room_work_dir = os.path.join(work_dir, f"room_{room_id}")
        os.makedirs(room_work_dir, exist_ok=True)
        
        # 创建录播姬配置文件
        config_path = os.path.join(room_work_dir, "config.json")
        
        # 构建配置
        config = {
            "Global": {
                "EnableMonitor": True,
                "Timer": 30,
                "Cookie": "",
                "Output": output_dir
            },
            "Rooms": [
                {
                    "Url": f"https://live.bilibili.com/{room_id}",
                    "AutoRecord": True,
                    "Cookie": "",
                    "Output": output_dir
                }
            ]
        }
        
        try:
            # 写入配置文件
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            return {
                "work_dir": room_work_dir,
                "output_dir": output_dir,
                "config_path": config_path
            }
        
        except Exception as e:
            print(f"创建录制配置失败: {e}")
            return None
    
    def get_recording_status(self, room: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取录制状态
        
        Args:
            room: 房间配置
            
        Returns:
            Dict[str, Any]: 录制状态信息
        """
        room_id = room.get("room_id")
        platform = room.get("platform", "bilibili")
        room_key = f"{platform}_{room_id}"
        
        if room_key not in self.record_processes:
            return {
                "is_recording": False,
                "status": "未录制"
            }
        
        process_info = self.record_processes[room_key]
        process = process_info["process"]
        
        # 检查进程是否还在运行
        return_code = process.poll()
        if return_code is not None:
            # 进程已结束，清理资源
            del self.record_processes[room_key]
            return {
                "is_recording": False,
                "status": f"已结束，返回码: {return_code}"
            }
        
        # 进程仍在运行
        return {
            "is_recording": True,
            "status": "录制中",
            "pid": process.pid,
            "start_time": process_info["start_time"],
            "duration": time.time() - process_info["start_time"]
        }