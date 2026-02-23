#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
B站API测试脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.bilibili_api import BilibiliAPI

def test_bilibili_api():
    """
    测试B站API功能
    """
    print("=== 测试B站API功能 ===")
    
    # 创建API客户端实例
    api = BilibiliAPI()
    
    # 测试房间ID（可以替换为实际直播的房间ID）
    test_room_id = "2233"
    
    print(f"\n1. 测试获取直播间信息（房间ID: {test_room_id}）")
    room_info = api.get_room_info(test_room_id)
    if room_info:
        print(f"   成功获取直播间信息：")
        print(f"   房间标题: {room_info.get('title')}")
        print(f"   主播名称: {room_info.get('uname')}")
        print(f"   直播状态: {'直播中' if room_info.get('live_status') == 1 else '未开播'}")
        print(f"   人气值: {room_info.get('online')}")
    else:
        print(f"   获取直播间信息失败")
    
    print(f"\n2. 测试获取直播状态（房间ID: {test_room_id}）")
    live_status, title, anchor_name = api.get_live_status(test_room_id)
    print(f"   直播状态: {'直播中' if live_status else '未开播'}")
    print(f"   房间标题: {title}")
    print(f"   主播名称: {anchor_name}")
    
    print(f"\n3. 测试是否在直播（房间ID: {test_room_id}）")
    is_living = api.is_living(test_room_id)
    print(f"   是否在直播: {'是' if is_living else '否'}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_bilibili_api()