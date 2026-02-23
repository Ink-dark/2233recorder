import time
import threading
from typing import List, Dict, Any
from src.api.bilibili_api import BilibiliAPI
from src.config.config import config_manager
from src.monitor.trigger import RecordTrigger


class Monitor:
    """
    直播间监控类
    """
    
    def __init__(self):
        """
        初始化监控器
        """
        self.bilibili_api = BilibiliAPI()
        self.monitor_threads = []
        self.is_running = False
        self.interval = config_manager.get("monitor.interval", 300)
        self.rooms = config_manager.get_rooms()
        self.trigger = RecordTrigger()
        
    def start(self):
        """
        启动监控
        """
        if self.is_running:
            print("监控已在运行中")
            return
        
        print("启动直播间监控")
        self.is_running = True
        
        # 为每个房间创建一个监控线程
        for room in self.rooms:
            thread = threading.Thread(
                target=self._monitor_room,
                args=(room,),
                daemon=True
            )
            self.monitor_threads.append(thread)
            thread.start()
            time.sleep(1)  # 避免同时请求API
        
        print(f"已启动 {len(self.monitor_threads)} 个监控线程")
    
    def stop(self):
        """
        停止监控
        """
        if not self.is_running:
            print("监控未在运行")
            return
        
        print("停止直播间监控")
        self.is_running = False
        
        # 等待所有监控线程结束
        for thread in self.monitor_threads:
            if thread.is_alive():
                thread.join(timeout=5)
        
        self.monitor_threads.clear()
        
        # 停止所有录制
        self.trigger.stop_all_recordings()
        
        print("所有监控线程已停止")
    
    def _monitor_room(self, room: Dict[str, Any]):
        """
        监控单个房间
        
        Args:
            room: 房间配置
        """
        room_id = room.get("room_id")
        platform = room.get("platform", "bilibili")
        room_name = room.get("name", f"房间{room_id}")
        
        print(f"开始监控 {platform} 房间 {room_name} ({room_id})")
        
        while self.is_running:
            try:
                # 根据平台选择不同的API客户端
                if platform == "bilibili":
                    live_status, title, anchor_name = self.bilibili_api.get_live_status(room_id)
                else:
                    # 其他平台暂未实现
                    live_status, title, anchor_name = False, "", ""
                
                # 调用录制触发逻辑
                self._on_room_status_changed(room, live_status, title, anchor_name)
                
            except Exception as e:
                print(f"监控房间 {room_id} 时发生错误: {e}")
            
            # 等待下一次监控
            for _ in range(self.interval):
                if not self.is_running:
                    break
                time.sleep(1)
        
        print(f"停止监控 {platform} 房间 {room_name} ({room_id})")
    
    def _on_room_status_changed(self, room: Dict[str, Any], live_status: bool, title: str, anchor_name: str):
        """
        房间状态变化时的回调函数
        
        Args:
            room: 房间配置
            live_status: 是否直播中
            title: 直播间标题
            anchor_name: 主播名称
        """
        room_id = room.get("room_id")
        room_name = room.get("name", f"房间{room_id}")
        
        status_text = "直播中" if live_status else "未开播"
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {room_name} ({room_id}): {status_text}")
        
        # 调用录制触发逻辑
        self.trigger.on_room_status_changed(room, live_status, title, anchor_name)
    
    def get_monitor_status(self):
        """
        获取监控状态
        
        Returns:
            Dict[str, Any]: 监控状态信息
        """
        return {
            "is_running": self.is_running,
            "monitor_threads_count": len(self.monitor_threads),
            "interval": self.interval,
            "rooms_count": len(self.rooms)
        }


# 全局监控器实例
monitor = Monitor()