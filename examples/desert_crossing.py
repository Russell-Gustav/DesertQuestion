"""
沙漠穿越问题示例 - Desert Crossing Example
展示如何使用该架构解决实际的数学建模问题
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_handler import DataHandler
from src.model import OptimizationModel
from src.utils import print_separator
import config
import pandas as pd


def desert_crossing_example():
    """
    沙漠穿越问题示例
    
    问题描述：
    探险队需要穿越沙漠，需要考虑：
    - 物资补给策略
    - 行进路线优化
    - 资源分配
    
    这是一个简化的示例，展示了如何使用该架构建模
    """
    
    print_separator()
    print("沙漠穿越问题 - 数学建模示例")
    print_separator()
    
    # 1. 问题参数设置
    print("\n1. 设置问题参数")
    print("-" * 50)
    
    # 示例参数（实际问题需要根据题目调整）
    total_distance = 1000  # 总距离 (km)
    initial_supply = 500   # 初始物资 (kg)
    daily_consumption = 10  # 每日消耗 (kg/day)
    max_carry_weight = 100  # 最大携带重量 (kg)
    
    print(f"总距离: {total_distance} km")
    print(f"初始物资: {initial_supply} kg")
    print(f"每日消耗: {daily_consumption} kg/day")
    print(f"最大携带重量: {max_carry_weight} kg")
    
    # 2. 创建优化模型
    print("\n\n2. 建立优化模型")
    print("-" * 50)
    
    # 目标：最小化穿越时间
    # 决策变量：每个补给点的物资量
    
    def objective_function(x):
        """
        目标函数：总时间（简化模型）
        x: 决策变量数组 [补给点1物资量, 补给点2物资量, ...]
        """
        # 这是一个简化示例，实际模型需要根据具体问题建立
        num_supply_points = len(x)
        total_time = 0
        
        # 计算每段的时间
        segment_distance = total_distance / (num_supply_points + 1)
        
        for i in range(num_supply_points + 1):
            supply = x[i] if i < num_supply_points else 0
            # 简化计算：时间 = 距离 / 速度（速度与负重相关）
            weight = supply + 50  # 基础重量
            speed = max(10, 50 - weight * 0.1)  # 速度随重量减小
            time = segment_distance / speed
            total_time += time
        
        return total_time
    
    # 3. 求解优化问题
    print("\n\n3. 求解优化问题")
    print("-" * 50)
    
    model = OptimizationModel()
    model.set_objective(objective_function)
    
    # 设置约束条件
    def supply_constraint(x):
        """物资总量约束"""
        return initial_supply - sum(x)
    
    model.add_constraint({
        'type': 'ineq',
        'fun': supply_constraint
    })
    
    # 初始猜测：3个补给点，平均分配
    num_supply_points = 3
    x0 = [initial_supply / num_supply_points] * num_supply_points
    
    # 边界：每个补给点物资在0到最大携带重量之间
    bounds = [(0, max_carry_weight)] * num_supply_points
    
    print("开始优化求解...")
    results = model.solve(x0, bounds=bounds)
    
    if results['success']:
        print(f"\n优化成功！")
        print(f"最优总时间: {results['optimal_value']:.2f} 小时")
        print(f"\n各补给点物资分配:")
        for i, supply in enumerate(results['optimal_solution']):
            print(f"  补给点 {i+1}: {supply:.2f} kg")
    else:
        print(f"\n优化失败: {results['message']}")
    
    # 4. 保存结果
    print("\n\n4. 保存结果到Excel")
    print("-" * 50)
    
    handler = DataHandler()
    
    # 创建结果DataFrame
    results_df = pd.DataFrame({
        '补给点': [f'补给点{i+1}' for i in range(num_supply_points)],
        '物资量(kg)': results['optimal_solution']
    })
    
    # 创建参数DataFrame
    params_df = pd.DataFrame({
        '参数': ['总距离(km)', '初始物资(kg)', '每日消耗(kg/day)', '最大携带(kg)', '最优时间(小时)'],
        '值': [total_distance, initial_supply, daily_consumption, max_carry_weight, results['optimal_value']]
    })
    
    # 保存到多个工作表
    output_file = os.path.join(config.OUTPUT_DIR, 'desert_crossing_results.xlsx')
    handler.write_multiple_sheets({
        '参数设置': params_df,
        '优化结果': results_df
    }, output_file)
    
    print(f"结果已保存至: {output_file}")
    
    # 5. 数据分析
    print("\n\n5. 数据分析")
    print("-" * 50)
    
    # 分析不同策略的效果
    strategies = ['均匀分配', '前重后轻', '优化分配']
    times = [
        objective_function([initial_supply/3, initial_supply/3, initial_supply/3]),
        objective_function([initial_supply*0.5, initial_supply*0.3, initial_supply*0.2]),
        results['optimal_value']
    ]
    
    comparison_df = pd.DataFrame({
        '策略': strategies,
        '总时间(小时)': times,
        '效率提升(%)': [(times[0] - t) / times[0] * 100 for t in times]
    })
    
    print("\n策略对比:")
    print(comparison_df.to_string(index=False))
    
    print_separator()
    print("沙漠穿越问题建模完成！")
    print_separator()


if __name__ == "__main__":
    # 确保输出目录存在
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    
    try:
        desert_crossing_example()
    except Exception as e:
        print(f"\n运行示例时出错: {e}")
        import traceback
        traceback.print_exc()
