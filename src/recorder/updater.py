import os
import sys
import requests
import zipfile
import shutil
from typing import Optional
import logging


class RecorderUpdater:
    """
    录播姬更新类
    """
    
    def __init__(self, base_dir: str = "/opt/2233recorder/recorders"):
        """
        初始化录播姬更新器
        
        Args:
            base_dir: 录播姬安装基础目录
        """
        self.base_dir = base_dir
        self.logger = logging.getLogger("RecorderUpdater")
        
        # 录播姬下载配置
        self.recorder_configs = {
            "bililive_recorder": {
                "name": "BililiveRecorder",
                "github_repo": "BililiveRecorder/BililiveRecorder",
                "download_url_template": "https://github.com/{repo}/releases/download/{version}/{filename}",
                "filename_template": "BililiveRecorder-CLI-linux-x64.zip",
                "executable": "BililiveRecorder.Cli",
                "work_dir": os.path.join(base_dir, "bilibili")
            }
        }
    
    def get_latest_version(self, recorder_type: str = "bililive_recorder") -> Optional[str]:
        """
        获取录播姬最新版本
        
        Args:
            recorder_type: 录播姬类型
            
        Returns:
            Optional[str]: 最新版本号，失败返回None
        """
        if recorder_type not in self.recorder_configs:
            self.logger.error(f"不支持的录播姬类型: {recorder_type}")
            return None
        
        config = self.recorder_configs[recorder_type]
        
        try:
            # 从GitHub API获取最新版本
            api_url = f"https://api.github.com/repos/{config['github_repo']}/releases/latest"
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            latest_version = data.get("tag_name")
            if latest_version:
                self.logger.info(f"获取到 {config['name']} 最新版本: {latest_version}")
                return latest_version
            else:
                self.logger.error(f"无法获取 {config['name']} 最新版本")
                return None
        
        except Exception as e:
            self.logger.error(f"获取最新版本失败: {e}")
            return None
    
    def download_recorder(self, recorder_type: str = "bililive_recorder", version: str = None) -> bool:
        """
        下载并安装录播姬
        
        Args:
            recorder_type: 录播姬类型
            version: 版本号，None表示下载最新版本
            
        Returns:
            bool: 下载安装成功返回True，失败返回False
        """
        if recorder_type not in self.recorder_configs:
            self.logger.error(f"不支持的录播姬类型: {recorder_type}")
            return False
        
        config = self.recorder_configs[recorder_type]
        
        # 获取版本号
        if not version:
            version = self.get_latest_version(recorder_type)
            if not version:
                return False
        
        # 创建工作目录
        work_dir = config["work_dir"]
        os.makedirs(work_dir, exist_ok=True)
        
        # 下载文件
        filename = config["filename_template"]
        download_url = config["download_url_template"].format(
            repo=config["github_repo"],
            version=version,
            filename=filename
        )
        
        download_path = os.path.join(work_dir, filename)
        
        self.logger.info(f"开始下载 {config['name']} {version}")
        self.logger.info(f"下载地址: {download_url}")
        
        try:
            # 下载文件
            response = requests.get(download_url, stream=True, timeout=30)
            response.raise_for_status()
            
            # 保存文件
            with open(download_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            self.logger.info(f"下载完成: {download_path}")
            
            # 解压文件
            extract_dir = os.path.join(work_dir, "temp")
            if os.path.exists(extract_dir):
                shutil.rmtree(extract_dir)
            os.makedirs(extract_dir)
            
            with zipfile.ZipFile(download_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)
            
            self.logger.info(f"解压完成: {extract_dir}")
            
            # 移动可执行文件到工作目录
            executable_path = os.path.join(work_dir, config["executable"])
            
            # 查找解压后的可执行文件
            for root, dirs, files in os.walk(extract_dir):
                if config["executable"] in files:
                    src_path = os.path.join(root, config["executable"])
                    # 先删除旧文件
                    if os.path.exists(executable_path):
                        os.remove(executable_path)
                    # 移动新文件
                    shutil.move(src_path, work_dir)
                    # 设置执行权限
                    os.chmod(executable_path, 0o755)
                    self.logger.info(f"已安装 {config['name']} 到: {executable_path}")
                    
                    # 清理临时文件
                    shutil.rmtree(extract_dir)
                    os.remove(download_path)
                    
                    return True
            
            self.logger.error(f"在解压目录中找不到可执行文件: {config['executable']}")
            # 清理临时文件
            shutil.rmtree(extract_dir)
            os.remove(download_path)
            
            return False
        
        except Exception as e:
            self.logger.error(f"下载或安装录播姬失败: {e}")
            # 清理临时文件
            if os.path.exists(extract_dir):
                shutil.rmtree(extract_dir)
            if os.path.exists(download_path):
                os.remove(download_path)
            return False
    
    def check_and_update(self, recorder_type: str = "bililive_recorder") -> bool:
        """
        检查并更新录播姬
        
        Args:
            recorder_type: 录播姬类型
            
        Returns:
            bool: 更新成功或已是最新版本返回True，失败返回False
        """
        if recorder_type not in self.recorder_configs:
            self.logger.error(f"不支持的录播姬类型: {recorder_type}")
            return False
        
        config = self.recorder_configs[recorder_type]
        executable_path = os.path.join(config["work_dir"], config["executable"])
        
        # 检查录播姬是否已安装
        if not os.path.exists(executable_path):
            self.logger.info(f"{config['name']} 未安装，开始安装")
            return self.download_recorder(recorder_type)
        
        # 检查是否需要更新
        self.logger.info(f"{config['name']} 已安装，检查更新")
        return self.download_recorder(recorder_type)
    
    def get_executable_path(self, recorder_type: str = "bililive_recorder") -> Optional[str]:
        """
        获取录播姬可执行文件路径
        
        Args:
            recorder_type: 录播姬类型
            
        Returns:
            Optional[str]: 可执行文件路径，失败返回None
        """
        if recorder_type not in self.recorder_configs:
            self.logger.error(f"不支持的录播姬类型: {recorder_type}")
            return None
        
        config = self.recorder_configs[recorder_type]
        executable_path = os.path.join(config["work_dir"], config["executable"])
        
        if os.path.exists(executable_path):
            return executable_path
        else:
            self.logger.error(f"{config['name']} 可执行文件不存在: {executable_path}")
            return None