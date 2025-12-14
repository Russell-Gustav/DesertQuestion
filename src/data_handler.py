"""
数据处理模块 - Data Handler Module
用于Excel文件的读取和写入操作
"""

import pandas as pd
import os
from config import EXCEL_ENGINE, INPUT_DIR, OUTPUT_DIR


class DataHandler:
    """处理Excel数据的读取和写入"""
    
    def __init__(self):
        """初始化数据处理器"""
        self.data = None
        
    def read_excel(self, file_path, sheet_name=0):
        """
        从Excel文件读取数据
        
        参数:
            file_path: str, Excel文件路径
            sheet_name: str or int, 工作表名称或索引，默认为第一个工作表
            
        返回:
            pandas.DataFrame, 读取的数据
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")
            
            self.data = pd.read_excel(file_path, sheet_name=sheet_name, engine=EXCEL_ENGINE)
            print(f"成功读取文件: {file_path}")
            print(f"数据形状: {self.data.shape}")
            return self.data
        except Exception as e:
            print(f"读取Excel文件时出错: {e}")
            raise
    
    def write_excel(self, data, file_path, sheet_name='Sheet1'):
        """
        将数据写入Excel文件
        
        参数:
            data: pandas.DataFrame, 要写入的数据
            file_path: str, 输出文件路径
            sheet_name: str, 工作表名称
        """
        try:
            # 确保输出目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 写入Excel文件
            data.to_excel(file_path, sheet_name=sheet_name, engine=EXCEL_ENGINE, index=False)
            print(f"成功写入文件: {file_path}")
        except Exception as e:
            print(f"写入Excel文件时出错: {e}")
            raise
    
    def read_multiple_sheets(self, file_path):
        """
        读取Excel文件的所有工作表
        
        参数:
            file_path: str, Excel文件路径
            
        返回:
            dict, 键为工作表名称，值为对应的DataFrame
        """
        try:
            sheets_dict = pd.read_excel(file_path, sheet_name=None, engine=EXCEL_ENGINE)
            print(f"成功读取文件: {file_path}")
            print(f"工作表数量: {len(sheets_dict)}")
            print(f"工作表名称: {list(sheets_dict.keys())}")
            return sheets_dict
        except Exception as e:
            print(f"读取多个工作表时出错: {e}")
            raise
    
    def write_multiple_sheets(self, data_dict, file_path):
        """
        将多个DataFrame写入Excel文件的不同工作表
        
        参数:
            data_dict: dict, 键为工作表名称，值为对应的DataFrame
            file_path: str, 输出文件路径
        """
        try:
            # 确保输出目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 写入多个工作表
            with pd.ExcelWriter(file_path, engine=EXCEL_ENGINE) as writer:
                for sheet_name, df in data_dict.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            print(f"成功写入文件: {file_path}")
            print(f"工作表数量: {len(data_dict)}")
        except Exception as e:
            print(f"写入多个工作表时出错: {e}")
            raise
    
    def get_data_info(self):
        """
        获取当前数据的基本信息
        
        返回:
            str, 数据的基本信息
        """
        if self.data is None:
            return "未加载数据"
        
        info = f"""
        数据形状: {self.data.shape}
        列名: {list(self.data.columns)}
        数据类型:
        {self.data.dtypes}
        
        前5行数据:
        {self.data.head()}
        
        基本统计信息:
        {self.data.describe()}
        """
        return info
