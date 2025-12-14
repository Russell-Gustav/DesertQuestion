"""
测试包初始化文件
"""
import sys
import os

# 将项目根目录添加到路径，以便能够导入src模块
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
