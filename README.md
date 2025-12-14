# DesertQuestion
2020中国全国大学生数学建模竞赛穿行沙漠问题

## 项目简介

本项目为数学建模问题提供了一个基础的Python架构，支持Excel数据处理、数学建模、优化求解和结果可视化。

## 项目结构

```
DesertQuestion/
├── main.py                 # 主程序入口
├── config.py              # 配置文件
├── requirements.txt       # 项目依赖
├── src/                   # 源代码目录
│   ├── __init__.py        # 包初始化
│   ├── data_handler.py    # 数据处理模块（Excel读写）
│   ├── model.py          # 数学模型模块（优化、仿真）
│   └── utils.py          # 工具函数模块（可视化、统计）
├── data/                  # 数据目录
│   ├── input/            # 输入数据目录
│   └── output/           # 输出结果目录
├── tests/                # 测试代码目录
│   ├── __init__.py
│   ├── test_data_handler.py
│   └── test_model.py
└── examples/             # 示例代码目录
    └── desert_crossing.py  # 沙漠穿越问题示例
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行示例程序

运行基础示例：
```bash
python main.py
```

运行沙漠穿越问题示例：
```bash
python examples/desert_crossing.py
```

## 使用说明

### 数据处理

使用 `DataHandler` 类处理Excel文件：

```python
from src.data_handler import DataHandler
import pandas as pd

# 创建数据处理器
handler = DataHandler()

# 读取Excel文件
data = handler.read_excel('data/input/input_data.xlsx')

# 写入Excel文件
output_data = pd.DataFrame({'result': [1, 2, 3]})
handler.write_excel(output_data, 'data/output/results.xlsx')

# 处理多个工作表
sheets = handler.read_multiple_sheets('data/input/multi_sheet.xlsx')
```

### 数学建模

#### 优化模型

```python
from src.model import OptimizationModel

# 创建优化模型
model = OptimizationModel()

# 定义目标函数
def objective(x):
    return x[0]**2 + x[1]**2

model.set_objective(objective)

# 添加约束（可选）
constraint = {'type': 'ineq', 'fun': lambda x: x[0] + x[1] - 1}
model.add_constraint(constraint)

# 求解
results = model.solve(
    x0=[0, 0],              # 初始值
    bounds=[(-10, 10), (-10, 10)]  # 变量边界
)

print(f"最优解: {results['optimal_solution']}")
print(f"最优值: {results['optimal_value']}")
```

#### 仿真模型

```python
from src.model import SimulationModel
import numpy as np

# 创建自定义仿真模型
class MySimulation(SimulationModel):
    def step(self, state, t):
        # 定义状态转移规则
        return state * 0.9 + np.random.randn() * 0.1

# 运行仿真
sim = MySimulation()
sim.set_initial_state([1.0, 2.0])
sim.time_steps = 100
results = sim.solve()
```

### 工具函数

```python
from src.utils import plot_results, calculate_statistics, normalize_data

# 绘制结果
x = range(100)
y = [i**2 for i in x]
plot_results(x, y, xlabel='时间', ylabel='值', title='结果图')

# 计算统计信息
stats = calculate_statistics(y)
print(stats)

# 数据归一化
normalized = normalize_data(y, method='minmax')
```

### 配置参数

在 `config.py` 中修改项目配置：

```python
# 数据目录
INPUT_DIR = 'data/input'
OUTPUT_DIR = 'data/output'

# 计算参数
PRECISION = 1e-6
MAX_ITERATIONS = 1000

# 可视化配置
FIGURE_SIZE = (10, 6)
DPI = 300
```

## 运行测试

```bash
# 测试数据处理模块
python -m pytest tests/test_data_handler.py

# 测试模型模块
python -m pytest tests/test_model.py

# 运行所有测试
python -m pytest tests/
```

或使用unittest:

```bash
python -m unittest discover tests
```

## 核心功能

### 1. Excel数据处理
- 单工作表读写
- 多工作表读写
- 数据信息查看
- 自动创建目录

### 2. 数学建模
- 优化模型求解（基于scipy.optimize）
- 仿真模型框架
- 可扩展的模型基类
- 参数配置管理

### 3. 数据分析与可视化
- 统计分析
- 数据归一化
- 结果绘图
- 多曲线对比

### 4. 工具支持
- 日志记录
- 配置管理
- 路径管理

## 依赖库

- **numpy**: 数值计算
- **pandas**: 数据处理
- **scipy**: 科学计算和优化
- **openpyxl**: Excel文件处理
- **matplotlib**: 数据可视化
- **seaborn**: 高级可视化

## 扩展开发

### 沙漠穿越问题示例

项目包含了一个具体的沙漠穿越问题示例 (`examples/desert_crossing.py`)，展示了完整的建模流程：

1. 参数设置
2. 建立优化模型
3. 求解优化问题
4. 结果保存
5. 策略对比分析

运行示例：
```bash
python examples/desert_crossing.py
```

### 添加自定义模型

继承 `MathematicalModel` 基类：

```python
from src.model import MathematicalModel

class CustomModel(MathematicalModel):
    def solve(self):
        # 实现你的求解逻辑
        self.results = {'custom_result': 42}
        return self.results
```

### 添加自定义工具函数

在 `src/utils.py` 中添加新函数或创建新的工具模块。

## 注意事项

1. 输入数据请放在 `data/input/` 目录
2. 输出结果会保存在 `data/output/` 目录
3. 修改配置请编辑 `config.py` 文件
4. 大型数据文件不会被git跟踪（已在.gitignore中配置）

## 许可证

本项目用于学习和研究目的。
