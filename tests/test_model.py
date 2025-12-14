"""
测试数学模型模块
"""

import unittest
import numpy as np

from src.model import OptimizationModel


class TestOptimizationModel(unittest.TestCase):
    """测试优化模型类"""
    
    def test_simple_optimization(self):
        """测试简单优化问题"""
        # 定义目标函数: (x-2)^2
        def objective(x):
            return (x[0] - 2)**2
        
        model = OptimizationModel()
        model.set_objective(objective)
        
        # 求解
        results = model.solve([0], bounds=[(-10, 10)])
        
        # 验证结果
        self.assertTrue(results['success'])
        self.assertAlmostEqual(results['optimal_solution'][0], 2.0, places=4)
        self.assertAlmostEqual(results['optimal_value'], 0.0, places=4)


if __name__ == '__main__':
    unittest.main()
