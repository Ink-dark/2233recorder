import os
import subprocess
from typing import Dict, Any
from src.recorder.core import Recorder


class RecordTrigger:
    """
    录制触发类
    """
    
    def __init__(self):
        """
        初始化录制触发器
        """
        self.recorders = {}
        self.recorder = Recorder()
    
    def on_room_status_changed(self, room: Dict[str, Any], live_status: bool, title: str, anchor_name: str):
        """
        房间状态变化时的处理函数
        
        Args:
            room: 房间配置
            live_status: 是否直播中
            title: 直播间标题
            anchor_name: 主播名称
        """
        room_id = room.get("room_id")
        platform = room.get("platform", "bilibili")
        room_key = f"{platform}_{room_id}"
        
        if live_status:
            # 直播间开播，开始录制
            if room_key not in self.recorders or not self.recorders[room_key]:
                self._start_recording(room, title, anchor_name)
        else:
            # 直播间下播，停止录制
            if room_key in self.recorders and self.recorders[room_key]:
                self._stop_recording(room)
    
    def _start_recording(self, room: Dict[str, Any], title: str, anchor_name: str):
        """
        开始录制
        
        Args:
            room: 房间配置
            title: 直播间标题
            anchor_name: 主播名称
        """
        room_id = room.get("room_id")
        platform = room.get("platform", "bilibili")
        room_name = room.get("name", f"房间{room_id}")
        room_key = f"{platform}_{room_id}"
        
        print(f"准备开始录制 {platform} 房间 {room_name} ({room_id})")
        
        try:
            # 调用录制核心模块开始录制
            recorder_process = self.recorder.start_recording(room, title, anchor_name)
            
            if recorder_process:
                self.recorders[room_key] = recorder_process
                print(f"✅ 成功开始录制 {platform} 房间 {room_name} ({room_id})")
            else:
                print(f"❌ 开始录制 {platform} 房间 {room_name} ({room_id}) 失败")
        
        except Exception as e:
            print(f"❌ 开始录制 {platform} 房间 {room_name} ({room_id}) 时发生错误: {e}")
    
    def _stop_recording(self, room: Dict[str, Any]):
        """
        停止录制
        
        Args:
            room: 房间配置
        """
        room_id = room.get("room_id")
        platform = room.get("platform", "bilibili")
        room_name = room.get("name", f"房间{room_id}")
        room_key = f"{platform}_{room_id}"
        
        print(f"准备停止录制 {platform} 房间 {room_name} ({room_id})")
        
        try:
            # 调用录制核心模块停止录制
            success = self.recorder.stop_recording(room)
            
            if success:
                self.recorders.pop(room_key, None)
                print(f"✅ 成功停止录制 {platform} 房间 {room_name} ({room_id})")
            else:
                print(f"❌ 停止录制 {platform} 房间 {room_name} ({room_id}) 失败")
        
        except Exception as e:
            print(f"❌ 停止录制 {platform} 房间 {room_name} ({room_id}) 时发生错误: {e}")
            self.recorders.pop(room_key, None)
    
    def stop_all_recordings(self):
        """
        停止所有录制
        """
        print("准备停止所有录制")
        
        for room_key in list(self.recorders.keys()):
            try:
                # 解析房间信息
                platform, room_id = room_key.split("_")
                # 查找房间配置
                from src.config.config import config_manager
                room = None
                for r in config_manager.get_rooms():
                    if r.get("platform") == platform and r.get("room_id") == room_id:
                        room = r
                        break
                
                if room:
                    self._stop_recording(room)
            
            except Exception as e:
                print(f"停止录制 {room_key} 时发生错误: {e}")
                self.recorders.pop(room_key, None)
        
        print("所有录制已停止")