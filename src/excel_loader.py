import pandas as pd
from typing import Dict, List, Tuple, Optional
from configs import (
    MapGraph, MapGraphNode, MapGraphEdge, ProblemConfig,
    BagConfig, EconomicConfig, DayCondition, default_weather_rules, SupplyPoint
)


def load_params_sheet(xls: pd.ExcelFile) -> Dict[str, float]:
    df = pd.read_excel(xls, "Params")
    params: Dict[str, float] = {}
    for _, row in df.iterrows():
        k = str(row["Key"]).strip()
        v = float(row["Value"])
        params[k] = v
    return params


def load_nodes_sheet(xls: pd.ExcelFile) -> Dict[str, MapGraphNode]:
    df = pd.read_excel(xls, "Nodes")
    nodes: Dict[str, MapGraphNode] = {}
    for _, row in df.iterrows():
        rid = str(row["NodeID"])
        t = str(row["Type"]).strip()
        t_lower = t.lower()
        type_map = {
            "start": "start",
            "end": "end",
            "mine": "mine",
            "village": "village",
            "forbidden": "forbidden"
        }
        std_type = type_map.get(t_lower, "normal")
        nodes[rid] = MapGraphNode(id=rid, name=t, type=std_type)
    return nodes


def load_map_sheet(xls: pd.ExcelFile, nodes: Dict[str, MapGraphNode]) -> Tuple[List[MapGraphEdge], Dict[str, List[Tuple[str, float]]]]:
    df = pd.read_excel(xls, "Map")
    edges: List[MapGraphEdge] = []
    adjacency: Dict[str, List[Tuple[str, float]]] = {rid: [] for rid in nodes.keys()}
    dist_col = "Distance" if "Distance" in df.columns else None
    for _, row in df.iterrows():
        src = str(row["Node1"])
        dst = str(row["Node2"])
        dist = float(row[dist_col]) if dist_col else 1.0
        bidirectional = True
        e = MapGraphEdge(src=src, dst=dst, distance=dist, bidirectional=bidirectional)
        edges.append(e)
        adjacency.setdefault(src, []).append((dst, dist))
        if bidirectional:
            adjacency.setdefault(dst, []).append((src, dist))
    return edges, adjacency


def load_weather_sheet(xls: pd.ExcelFile, days_limit: int) -> List[DayCondition]:
    """
    读取 Weather 表；若缺失或为空，则为所有天生成默认 "Sunny"。
    空表默认不会出错；若列名缺失则也走默认。
    """
    try:
        if "Weather" not in xls.sheet_names:
            # 缺失 Weather sheet：全 Sunny
            return [
                DayCondition(day=d, max_travel_dist=0.0, food_consumption=0.0, water_consumption=0.0, weather="Sunny")
                for d in range(1, days_limit + 1)
            ]
        df = pd.read_excel(xls, "Weather")
        # 空表直接使用默认
        if df is None or df.shape[0] == 0:
            return [
                DayCondition(day=d, max_travel_dist=0.0, food_consumption=0.0, water_consumption=0.0, weather="Sunny")
                for d in range(1, days_limit + 1)
            ]
        # 尝试读取列
        conds: Dict[int, str] = {}
        if "Day" in df.columns and "Weather" in df.columns:
            for _, row in df.iterrows():
                day = int(row["Day"]) if not pd.isna(row["Day"]) else None
                weather = str(row["Weather"]).strip() if not pd.isna(row["Weather"]) else None
                if day is not None and weather:
                    conds[day] = weather
        # 生成列表，默认 Sunny
        day_conditions = []
        for d in range(1, days_limit + 1):
            w = conds.get(d, "Sunny")
            day_conditions.append(
                DayCondition(day=d, max_travel_dist=0.0, food_consumption=0.0, water_consumption=0.0, weather=w)
            )
        return day_conditions
    except Exception:
        # 任意异常都回退到全 Sunny，保证运行健壮性
        return [
            DayCondition(day=d, max_travel_dist=0.0, food_consumption=0.0, water_consumption=0.0, weather="Sunny")
            for d in range(1, days_limit + 1)
        ]


def build_problem_config_from_excel(path: str, level_name: str = None) -> ProblemConfig:
    xls = pd.ExcelFile(path)
    params = load_params_sheet(xls)
    nodes = load_nodes_sheet(xls)
    edges, adjacency = load_map_sheet(xls, nodes)
    map_graph = MapGraph(nodes=nodes, edges=edges, adjacency=adjacency)

    max_weight   = params.get("max_weight", 1200.0)
    init_money   = params.get("init_money", 10000.0)
    water_weight = params.get("water_weight", 5.0)
    food_weight  = params.get("food_weight", 3.0)
    base_profit  = params.get("base_profit", 1000.0)
    days_limit   = int(params.get("days_limit", 30))

    # 可选：读取基础行程与消耗
    travel_base  = float(params.get("travel_base", 12.0))
    food_base    = float(params.get("food_base", 2.0))
    water_base   = float(params.get("water_base", 3.0))

    bag_cfg = BagConfig(
        max_weight=max_weight,
        food_unit_weight=food_weight,
        water_unit_weight=water_weight
    )
    econ_cfg = EconomicConfig(
        initial_cash=init_money,
        base_profit=base_profit
    )

    day_conditions = load_weather_sheet(xls, days_limit)
    weather_rules = default_weather_rules()

    return ProblemConfig(
        days=days_limit,
        bag_cfg=bag_cfg,
        econ_cfg=econ_cfg,
        day_conditions=day_conditions,
        map_graph=map_graph,
        level_name=level_name,
        weather_rules=weather_rules,
        travel_base=travel_base,
        food_base=food_base,
        water_base=water_base
    )