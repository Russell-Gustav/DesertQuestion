"""
主程序入口 - Main Entry Point
演示如何使用该架构进行数学建模
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_handler import DataHandler
from model import OptimizationModel, SimulationModel
from utils import plot_results, calculate_statistics, print_separator
import config
import numpy as np


def example_workflow():
    """示例工作流程"""
    
    print_separator()
    print("数学建模项目 - 示例工作流程")
    print_separator()
    
    # 1. 数据处理示例
    print("\n1. 数据处理模块示例")
    print("-" * 50)
    
    data_handler = DataHandler()
    
    # 创建示例数据
    import pandas as pd
    sample_data = pd.DataFrame({
        '参数A': [1, 2, 3, 4, 5],
        '参数B': [10, 20, 30, 40, 50],
        '结果': [11, 22, 33, 44, 55]
    })
    
    # 保存示例数据
    example_file = os.path.join(config.INPUT_DIR, 'example_data.xlsx')
    data_handler.write_excel(sample_data, example_file, sheet_name='示例数据')
    
    # 读取数据
    loaded_data = data_handler.read_excel(example_file)
    print("\n加载的数据:")
    print(loaded_data)
    
    # 2. 优化模型示例
    print("\n\n2. 优化模型示例")
    print("-" * 50)
    
    # 定义一个简单的优化问题: minimize (x-3)^2 + (y-2)^2
    def objective(x):
        return (x[0] - 3)**2 + (x[1] - 2)**2
    
    opt_model = OptimizationModel()
    opt_model.set_objective(objective)
    
    # 求解
    initial_guess = [0, 0]
    bounds = [(-10, 10), (-10, 10)]
    results = opt_model.solve(initial_guess, bounds=bounds)
    
    print(f"\n优化结果:")
    print(f"  成功: {results['success']}")
    print(f"  最优解: {results['optimal_solution']}")
    print(f"  最优值: {results['optimal_value']:.6f}")
    
    # 3. 数据统计示例
    print("\n\n3. 数据统计示例")
    print("-" * 50)
    
    test_data = np.random.randn(100)
    stats = calculate_statistics(test_data)
    
    print("\n随机数据统计信息:")
    for key, value in stats.items():
        print(f"  {key}: {value:.4f}")
    
    # 4. 结果导出
    print("\n\n4. 结果导出示例")
    print("-" * 50)
    
    results_df = pd.DataFrame({
        '优化变量X': [results['optimal_solution'][0]],
        '优化变量Y': [results['optimal_solution'][1]],
        '目标函数值': [results['optimal_value']],
        '迭代次数': [results['iterations']]
    })
    
    output_file = os.path.join(config.OUTPUT_DIR, 'optimization_results.xlsx')
    data_handler.write_excel(results_df, output_file, sheet_name='优化结果')
    
    print("\n所有结果已保存至 data/output/ 目录")
    
    print_separator()
    print("示例工作流程完成！")
    print_separator()


def main():
    """主函数"""
    
    print("""
    ====================================
    欢迎使用数学建模项目架构
    ====================================
    
    该项目提供了以下功能模块:
    
    1. 数据处理 (src/data_handler.py)
       - Excel文件读取和写入
       - 多工作表处理
       - 数据信息查看
    
    2. 数学模型 (src/model.py)
       - 优化模型类
       - 仿真模型类
       - 可扩展的模型基类
    
    3. 工具函数 (src/utils.py)
       - 数据可视化
       - 统计分析
       - 数据归一化
       - 日志记录
    
    4. 配置文件 (config.py)
       - 路径配置
       - 参数配置
    
    ====================================
    """)
    
    # 确保必要的目录存在
    os.makedirs(config.INPUT_DIR, exist_ok=True)
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    
    # 运行示例工作流程
    try:
        example_workflow()
    except Exception as e:
        print(f"\n运行示例时出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
