import os
import subprocess
from typing import Optional
import logging


class VideoConverter:
    """
    视频格式转换类
    """
    
    def __init__(self, ffmpeg_path: str = "/usr/bin/ffmpeg"):
        """
        初始化视频转换器
        
        Args:
            ffmpeg_path: FFmpeg可执行文件路径
        """
        self.ffmpeg_path = ffmpeg_path
        self.logger = logging.getLogger("VideoConverter")
    
    def convert_flv_to_mp4(self, input_file: str, output_file: Optional[str] = None, delete_original: bool = False) -> bool:
        """
        将FLV文件转换为MP4格式
        
        Args:
            input_file: 输入FLV文件路径
            output_file: 输出MP4文件路径，默认与输入文件同名
            delete_original: 转换完成后是否删除原文件
            
        Returns:
            bool: 转换成功返回True，失败返回False
        """
        # 检查输入文件是否存在
        if not os.path.exists(input_file):
            self.logger.error(f"输入文件不存在: {input_file}")
            return False
        
        # 检查文件扩展名是否为FLV
        if not input_file.lower().endswith(".flv"):
            self.logger.error(f"输入文件不是FLV格式: {input_file}")
            return False
        
        # 设置输出文件路径
        if not output_file:
            output_file = os.path.splitext(input_file)[0] + ".mp4"
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        try:
            # 构建FFmpeg命令
            cmd = [
                self.ffmpeg_path,
                "-i", input_file,
                "-c:v", "copy",  # 复制视频流，不重新编码
                "-c:a", "copy",  # 复制音频流，不重新编码
                "-movflags", "+faststart",  # 优化MP4文件，适合Web播放
                "-y",  # 覆盖输出文件
                output_file
            ]
            
            self.logger.info(f"开始转换: {input_file} -> {output_file}")
            
            # 执行转换命令
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=3600  # 1小时超时
            )
            
            # 检查转换结果
            if result.returncode == 0:
                self.logger.info(f"转换成功: {input_file} -> {output_file}")
                
                # 删除原文件
                if delete_original:
                    try:
                        os.remove(input_file)
                        self.logger.info(f"已删除原文件: {input_file}")
                    except Exception as e:
                        self.logger.error(f"删除原文件失败: {e}")
                
                return True
            else:
                self.logger.error(f"转换失败，返回码: {result.returncode}")
                self.logger.error(f"错误输出: {result.stderr}")
                return False
        
        except subprocess.TimeoutExpired:
            self.logger.error(f"转换超时: {input_file}")
            return False
        
        except Exception as e:
            self.logger.error(f"转换过程中发生错误: {e}")
            return False
    
    def batch_convert(self, input_dir: str, output_dir: Optional[str] = None, delete_original: bool = False) -> int:
        """
        批量转换目录中的FLV文件
        
        Args:
            input_dir: 输入目录
            output_dir: 输出目录，默认与输入目录相同
            delete_original: 转换完成后是否删除原文件
            
        Returns:
            int: 成功转换的文件数量
        """
        if not os.path.exists(input_dir):
            self.logger.error(f"输入目录不存在: {input_dir}")
            return 0
        
        if not os.path.isdir(input_dir):
            self.logger.error(f"输入路径不是目录: {input_dir}")
            return 0
        
        # 设置输出目录
        if not output_dir:
            output_dir = input_dir
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        success_count = 0
        
        # 遍历目录中的所有FLV文件
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.lower().endswith(".flv"):
                    input_file = os.path.join(root, file)
                    
                    # 构建输出文件路径
                    if output_dir == input_dir:
                        output_file = os.path.splitext(input_file)[0] + ".mp4"
                    else:
                        # 保持相同的目录结构
                        relative_path = os.path.relpath(root, input_dir)
                        output_subdir = os.path.join(output_dir, relative_path)
                        os.makedirs(output_subdir, exist_ok=True)
                        output_file = os.path.join(output_subdir, os.path.splitext(file)[0] + ".mp4")
                    
                    # 执行转换
                    if self.convert_flv_to_mp4(input_file, output_file, delete_original):
                        success_count += 1
        
        self.logger.info(f"批量转换完成，成功转换 {success_count} 个文件")
        return success_count
    
    def check_ffmpeg(self) -> bool:
        """
        检查FFmpeg是否可用
        
        Returns:
            bool: FFmpeg可用返回True，否则返回False
        """
        try:
            result = subprocess.run(
                [self.ffmpeg_path, "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.logger.info(f"FFmpeg版本: {result.stdout.splitlines()[0]}")
                return True
            else:
                self.logger.error(f"FFmpeg检查失败: {result.stderr}")
                return False
        
        except FileNotFoundError:
            self.logger.error(f"FFmpeg未找到: {self.ffmpeg_path}")
            return False
        
        except Exception as e:
            self.logger.error(f"检查FFmpeg时发生错误: {e}")
            return False