"""
批量文件名处理工具, 用于PT/BT下载文件的整理
"""
import os

video_suffix = ['.mp4','.mkv']
subtitle_suffix = ['.ass']

files = os.listdir('.')
files = [file for file in os.listdir('.') if not os.path.isdir(file)]
print(files)
input()