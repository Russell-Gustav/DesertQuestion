"""
数学建模模块 - Mathematical Model Module
用于实现具体的数学建模算法
"""

import numpy as np
import pandas as pd
from scipy import optimize
from config import PRECISION, MAX_ITERATIONS


class MathematicalModel:
    """数学建模基类"""
    
    def __init__(self):
        """初始化模型"""
        self.parameters = {}
        self.results = {}
    
    def set_parameters(self, **kwargs):
        """
        设置模型参数
        
        参数:
            **kwargs: 模型参数的键值对
        """
        self.parameters.update(kwargs)
        print(f"已设置参数: {kwargs}")
    
    def solve(self):
        """
        求解模型（需要在子类中实现）
        
        返回:
            dict, 求解结果
        """
        raise NotImplementedError("子类需要实现solve方法")
    
    def get_results(self):
        """
        获取求解结果
        
        返回:
            dict, 模型求解结果
        """
        return self.results
    
    def export_results(self):
        """
        将结果转换为DataFrame格式，便于导出
        
        返回:
            pandas.DataFrame, 结果数据
        """
        return pd.DataFrame([self.results])


class OptimizationModel(MathematicalModel):
    """优化模型类"""
    
    def __init__(self):
        """初始化优化模型"""
        super().__init__()
        self.objective_function = None
        self.constraints = []
    
    def set_objective(self, func):
        """
        设置目标函数
        
        参数:
            func: callable, 目标函数
        """
        self.objective_function = func
        print("已设置目标函数")
    
    def add_constraint(self, constraint):
        """
        添加约束条件
        
        参数:
            constraint: dict, 约束条件（格式参考scipy.optimize）
        """
        self.constraints.append(constraint)
        print(f"已添加约束条件，当前约束数量: {len(self.constraints)}")
    
    def solve(self, x0, method='SLSQP', bounds=None):
        """
        求解优化问题
        
        参数:
            x0: array-like, 初始值
            method: str, 优化方法
            bounds: sequence, 变量边界
            
        返回:
            dict, 优化结果
        """
        if self.objective_function is None:
            raise ValueError("未设置目标函数")
        
        try:
            result = optimize.minimize(
                self.objective_function,
                x0,
                method=method,
                bounds=bounds,
                constraints=self.constraints,
                options={'maxiter': MAX_ITERATIONS}
            )
            
            self.results = {
                'success': result.success,
                'optimal_value': result.fun,
                'optimal_solution': result.x,
                'iterations': result.nit,
                'message': result.message
            }
            
            print(f"优化完成: {'成功' if result.success else '失败'}")
            print(f"最优值: {result.fun}")
            
            return self.results
        
        except Exception as e:
            print(f"求解优化问题时出错: {e}")
            raise


class SimulationModel(MathematicalModel):
    """仿真模型类"""
    
    def __init__(self):
        """初始化仿真模型"""
        super().__init__()
        self.time_steps = 100
        self.initial_state = None
    
    def set_initial_state(self, state):
        """
        设置初始状态
        
        参数:
            state: array-like, 初始状态向量
        """
        self.initial_state = np.array(state)
        print(f"已设置初始状态: {self.initial_state}")
    
    def step(self, state, t):
        """
        单步仿真（需要在子类中实现）
        
        参数:
            state: array-like, 当前状态
            t: float, 当前时间
            
        返回:
            array-like, 下一时刻状态
        """
        raise NotImplementedError("子类需要实现step方法")
    
    def solve(self):
        """
        运行仿真
        
        返回:
            dict, 仿真结果
        """
        if self.initial_state is None:
            raise ValueError("未设置初始状态")
        
        try:
            states = [self.initial_state]
            
            for t in range(self.time_steps):
                next_state = self.step(states[-1], t)
                states.append(next_state)
            
            self.results = {
                'states': np.array(states),
                'time_steps': self.time_steps,
                'final_state': states[-1]
            }
            
            print(f"仿真完成，共 {self.time_steps} 步")
            
            return self.results
        
        except Exception as e:
            print(f"运行仿真时出错: {e}")
            raise
