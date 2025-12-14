"""
测试数据处理模块
"""

import unittest
import pandas as pd
import tempfile
import os

from src.data_handler import DataHandler


class TestDataHandler(unittest.TestCase):
    """测试DataHandler类"""
    
    def setUp(self):
        """设置测试环境"""
        self.handler = DataHandler()
        self.test_dir = tempfile.mkdtemp()
        
    def test_write_and_read_excel(self):
        """测试Excel读写功能"""
        # 创建测试数据
        test_data = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })
        
        # 写入文件
        test_file = os.path.join(self.test_dir, 'test.xlsx')
        self.handler.write_excel(test_data, test_file)
        
        # 读取文件
        loaded_data = self.handler.read_excel(test_file)
        
        # 验证数据
        self.assertEqual(loaded_data.shape, test_data.shape)
        self.assertTrue(all(loaded_data.columns == test_data.columns))
    
    def test_multiple_sheets(self):
        """测试多工作表功能"""
        # 创建测试数据
        data_dict = {
            'Sheet1': pd.DataFrame({'A': [1, 2]}),
            'Sheet2': pd.DataFrame({'B': [3, 4]})
        }
        
        # 写入文件
        test_file = os.path.join(self.test_dir, 'test_multi.xlsx')
        self.handler.write_multiple_sheets(data_dict, test_file)
        
        # 读取文件
        loaded_dict = self.handler.read_multiple_sheets(test_file)
        
        # 验证
        self.assertEqual(len(loaded_dict), 2)
        self.assertIn('Sheet1', loaded_dict)
        self.assertIn('Sheet2', loaded_dict)


if __name__ == '__main__':
    unittest.main()
