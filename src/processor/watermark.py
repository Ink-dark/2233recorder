import os
import subprocess
from typing import Optional, Dict, Any
import logging


class WatermarkAdder:
    """
    水印添加类
    """
    
    def __init__(self, ffmpeg_path: str = "/usr/bin/ffmpeg"):
        """
        初始化水印添加器
        
        Args:
            ffmpeg_path: FFmpeg可执行文件路径
        """
        self.ffmpeg_path = ffmpeg_path
        self.logger = logging.getLogger("WatermarkAdder")
    
    def add_text_watermark(self, 
                         input_file: str, 
                         output_file: Optional[str] = None, 
                         watermark_text: str = "2233recorder录制",
                         font: str = "wqy-microhei",
                         font_size: int = 24,
                         font_color: str = "white",
                         position: str = "bottom-right",
                         margin: int = 10,
                         opacity: float = 0.8,
                         box: bool = True,
                         box_color: str = "black",
                         box_opacity: float = 0.5,
                         delete_original: bool = False) -> bool:
        """
        为视频添加文字水印
        
        Args:
            input_file: 输入视频文件路径
            output_file: 输出视频文件路径，默认与输入文件同名
            watermark_text: 水印文字
            font: 字体名称
            font_size: 字体大小
            font_color: 字体颜色
            position: 水印位置，可选值：top-left, top-right, bottom-left, bottom-right, center
            margin: 边距（像素）
            opacity: 文字透明度（0-1）
            box: 是否添加背景框
            box_color: 背景框颜色
            box_opacity: 背景框透明度（0-1）
            delete_original: 处理完成后是否删除原文件
            
        Returns:
            bool: 添加水印成功返回True，失败返回False
        """
        # 检查输入文件是否存在
        if not os.path.exists(input_file):
            self.logger.error(f"输入文件不存在: {input_file}")
            return False
        
        # 设置输出文件路径
        if not output_file:
            # 添加_watermark后缀
            name, ext = os.path.splitext(input_file)
            output_file = f"{name}_watermark{ext}"
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # 计算水印位置
        x, y = self._calculate_position(position, margin)
        
        # 构建drawtext滤镜参数
        drawtext_params = []
        
        # 文字基本参数
        drawtext_params.append(f"text='{watermark_text}'")
        drawtext_params.append(f"fontfile={font}")
        drawtext_params.append(f"fontsize={font_size}")
        drawtext_params.append(f"fontcolor={font_color}@{opacity}")
        drawtext_params.append(f"x={x}")
        drawtext_params.append(f"y={y}")
        
        # 背景框参数
        if box:
            drawtext_params.append(f"box=1")
            drawtext_params.append(f"boxcolor={box_color}@{box_opacity}")
            drawtext_params.append(f"boxborderw=5")
        
        drawtext_filter = f"drawtext={':'.join(drawtext_params)}"
        
        try:
            # 构建FFmpeg命令
            cmd = [
                self.ffmpeg_path,
                "-i", input_file,
                "-vf", drawtext_filter,
                "-c:a", "copy",  # 复制音频流，不重新编码
                "-y",  # 覆盖输出文件
                output_file
            ]
            
            self.logger.info(f"开始添加水印: {input_file} -> {output_file}")
            self.logger.info(f"水印参数: {drawtext_filter}")
            
            # 执行命令
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=3600  # 1小时超时
            )
            
            # 检查结果
            if result.returncode == 0:
                self.logger.info(f"添加水印成功: {input_file} -> {output_file}")
                
                # 删除原文件
                if delete_original:
                    try:
                        os.remove(input_file)
                        self.logger.info(f"已删除原文件: {input_file}")
                    except Exception as e:
                        self.logger.error(f"删除原文件失败: {e}")
                
                return True
            else:
                self.logger.error(f"添加水印失败，返回码: {result.returncode}")
                self.logger.error(f"错误输出: {result.stderr}")
                return False
        
        except subprocess.TimeoutExpired:
            self.logger.error(f"添加水印超时: {input_file}")
            return False
        
        except Exception as e:
            self.logger.error(f"添加水印过程中发生错误: {e}")
            return False
    
    def _calculate_position(self, position: str, margin: int) -> tuple:
        """
        计算水印位置
        
        Args:
            position: 水印位置
            margin: 边距（像素）
            
        Returns:
            tuple: (x坐标表达式, y坐标表达式)
        """
        # 位置映射
        position_mapping = {
            "top-left": (f"{margin}", f"{margin}"),
            "top-right": (f"main_w - text_w - {margin}", f"{margin}"),
            "bottom-left": (f"{margin}", f"main_h - text_h - {margin}"),
            "bottom-right": (f"main_w - text_w - {margin}", f"main_h - text_h - {margin}"),
            "center": (f"(main_w - text_w) / 2", f"(main_h - text_h) / 2")
        }
        
        return position_mapping.get(position, (f"{margin}", f"main_h - text_h - {margin}"))
    
    def batch_add_watermark(self, 
                          input_dir: str, 
                          output_dir: Optional[str] = None, 
                          watermark_config: Optional[Dict[str, Any]] = None,
                          delete_original: bool = False) -> int:
        """
        批量为目录中的视频添加水印
        
        Args:
            input_dir: 输入目录
            output_dir: 输出目录，默认与输入目录相同
            watermark_config: 水印配置
            delete_original: 处理完成后是否删除原文件
            
        Returns:
            int: 成功添加水印的文件数量
        """
        if not os.path.exists(input_dir):
            self.logger.error(f"输入目录不存在: {input_dir}")
            return 0
        
        if not os.path.isdir(input_dir):
            self.logger.error(f"输入路径不是目录: {input_dir}")
            return 0
        
        # 设置默认水印配置
        default_config = {
            "watermark_text": "2233recorder录制",
            "font": "wqy-microhei",
            "font_size": 24,
            "font_color": "white",
            "position": "bottom-right",
            "margin": 10,
            "opacity": 0.8,
            "box": True,
            "box_color": "black",
            "box_opacity": 0.5
        }
        
        if watermark_config:
            default_config.update(watermark_config)
        
        # 设置输出目录
        if not output_dir:
            output_dir = input_dir
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        success_count = 0
        
        # 支持的视频格式
        supported_formats = [".mp4", ".flv", ".avi", ".mkv", ".mov"]
        
        # 遍历目录中的所有视频文件
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                # 检查文件格式是否支持
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext in supported_formats:
                    input_file = os.path.join(root, file)
                    
                    # 构建输出文件路径
                    if output_dir == input_dir:
                        # 添加_watermark后缀
                        name, ext = os.path.splitext(input_file)
                        output_file = f"{name}_watermark{ext}"
                    else:
                        # 保持相同的目录结构
                        relative_path = os.path.relpath(root, input_dir)
                        output_subdir = os.path.join(output_dir, relative_path)
                        os.makedirs(output_subdir, exist_ok=True)
                        # 添加_watermark后缀
                        name, ext = os.path.splitext(file)
                        output_file = os.path.join(output_subdir, f"{name}_watermark{ext}")
                    
                    # 执行添加水印
                    if self.add_text_watermark(
                        input_file=input_file,
                        output_file=output_file,
                        delete_original=delete_original,
                        **default_config
                    ):
                        success_count += 1
        
        self.logger.info(f"批量添加水印完成，成功处理 {success_count} 个文件")
        return success_count