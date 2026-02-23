import os
import yaml
from typing import Dict, Any


class ConfigManager:
    """
    配置文件管理类
    """
    
    def __init__(self, config_dir: str = "config"):
        """
        初始化配置管理器
        
        Args:
            config_dir: 配置文件目录
        """
        self.config_dir = config_dir
        self.config: Dict[str, Any] = {}
        self.rooms: Dict[str, Any] = {}
        
    def load_config(self) -> bool:
        """
        加载主配置文件
        
        Returns:
            bool: 加载成功返回True，失败返回False
        """
        config_path = os.path.join(self.config_dir, "config.yaml")
        
        # 如果配置文件不存在，使用示例配置文件
        if not os.path.exists(config_path):
            example_path = os.path.join(self.config_dir, "config.example.yaml")
            if os.path.exists(example_path):
                with open(example_path, "r", encoding="utf-8") as f:
                    self.config = yaml.safe_load(f)
                return True
            else:
                return False
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f)
            return True
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return False
    
    def load_rooms(self) -> bool:
        """
        加载房间配置文件
        
        Returns:
            bool: 加载成功返回True，失败返回False
        """
        rooms_path = os.path.join(self.config_dir, "rooms.yaml")
        
        # 如果配置文件不存在，使用示例配置文件
        if not os.path.exists(rooms_path):
            example_path = os.path.join(self.config_dir, "rooms.example.yaml")
            if os.path.exists(example_path):
                with open(example_path, "r", encoding="utf-8") as f:
                    self.rooms = yaml.safe_load(f)
                return True
            else:
                return False
        
        try:
            with open(rooms_path, "r", encoding="utf-8") as f:
                self.rooms = yaml.safe_load(f)
            return True
        except Exception as e:
            print(f"加载房间配置文件失败: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键，支持点分隔符（如"system.log_level"）
            default: 默认值
            
        Returns:
            Any: 配置值或默认值
        """
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_rooms(self) -> list:
        """
        获取所有房间配置
        
        Returns:
            list: 房间配置列表
        """
        return self.rooms.get("rooms", [])
    
    def get_room(self, room_id: str) -> dict:
        """
        根据ID获取房间配置
        
        Args:
            room_id: 房间ID
            
        Returns:
            dict: 房间配置或空字典
        """
        for room in self.get_rooms():
            if room.get("id") == room_id:
                return room
        return {}


# 全局配置管理器实例
config_manager = ConfigManager()