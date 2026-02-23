import requests
from typing import Dict, Any, Optional


class BilibiliAPI:
    """
    B站API封装类
    """
    
    def __init__(self):
        """
        初始化B站API客户端
        """
        self.base_url = "https://api.live.bilibili.com"
        self.space_base_url = "https://api.bilibili.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    
    def get_room_info(self, room_id: str) -> Optional[Dict[str, Any]]:
        """
        获取直播间信息
        
        Args:
            room_id: 房间ID
            
        Returns:
            Optional[Dict[str, Any]]: 直播间信息字典，失败返回None
        """
        url = f"{self.base_url}/room/v1/Room/get_info"
        params = {
            "room_id": room_id
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                return data.get("data", {})
            else:
                print(f"获取直播间信息失败: {data.get('message')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"请求直播间信息失败: {e}")
            return None
    
    def get_live_status(self, room_id: str) -> tuple:
        """
        获取直播间直播状态
        
        Args:
            room_id: 房间ID
            
        Returns:
            tuple: (是否直播中, 直播间标题, 主播名称)
        """
        room_info = self.get_room_info(room_id)
        
        if not room_info:
            return False, "", ""
        
        live_status = room_info.get("live_status", 0) == 1
        title = room_info.get("title", "")
        anchor_name = room_info.get("uname", "")
        
        # 如果主播名为空，尝试通过UID获取
        if not anchor_name and room_info.get("uid"):
            anchor_info = self.get_user_info(room_info.get("uid"))
            if anchor_info:
                anchor_name = anchor_info.get("name", "")
        
        return live_status, title, anchor_name
    
    def get_user_info(self, uid: int) -> Optional[Dict[str, Any]]:
        """
        获取用户信息
        
        Args:
            uid: 用户UID
            
        Returns:
            Optional[Dict[str, Any]]: 用户信息字典，失败返回None
        """
        url = f"{self.space_base_url}/x/space/acc/info"
        params = {
            "mid": uid
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                return data.get("data", {})
            else:
                print(f"获取用户信息失败: {data.get('message')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"请求用户信息失败: {e}")
            return None
    
    def is_living(self, room_id: str) -> bool:
        """
        检查直播间是否在直播
        
        Args:
            room_id: 房间ID
            
        Returns:
            bool: 直播中返回True，否则返回False
        """
        live_status, _, _ = self.get_live_status(room_id)
        return live_status