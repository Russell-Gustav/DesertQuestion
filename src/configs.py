from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

WeatherType = str  # "Sunny" | "Hot" | "Sand"

@dataclass
class SupplyPoint:
    id: str
    name: str
    buy_price_food: float
    buy_price_water: float
    sell_price_food: Optional[float] = None
    sell_price_water: Optional[float] = None

@dataclass
class MapGraphNode:
    id: str
    name: str
    type: str  # "start" | "end" | "mine" | "village" | "normal" | "forbidden"
    coord: Optional[Tuple[float, float]] = None
    supply: Optional[SupplyPoint] = None

@dataclass
class MapGraphEdge:
    src: str
    dst: str
    distance: float
    bidirectional: bool = True

@dataclass
class MapGraph:
    nodes: Dict[str, MapGraphNode]
    edges: List[MapGraphEdge]
    adjacency: Dict[str, List[Tuple[str, float]]]

@dataclass
class DayCondition:
    day: int
    max_travel_dist: float
    food_consumption: float
    water_consumption: float
    weather: Optional[WeatherType] = None
    note: str = ""

@dataclass
class BagConfig:
    max_weight: float
    food_unit_weight: float
    water_unit_weight: float

@dataclass
class EconomicConfig:
    initial_cash: float
    base_profit: float = 0.0

@dataclass
class ProblemConfig:
    days: int
    bag_cfg: BagConfig
    econ_cfg: EconomicConfig
    day_conditions: List[DayCondition]
    map_graph: MapGraph
    level_name: Optional[str] = None
    weather_rules: Dict[WeatherType, Dict[str, float]] = None
    # 可选：从 Params 读取的基础行程与消耗
    travel_base: float = 12.0
    food_base: float = 2.0
    water_base: float = 3.0

def default_weather_rules() -> Dict[WeatherType, Dict[str, float]]:
    return {
        "Sunny": {"travel_mult": 1.0, "food_mult": 1.0, "water_mult": 1.0},
        "Hot":   {"travel_mult": 0.8, "food_mult": 1.1, "water_mult": 1.3},
        "Sand":  {"travel_mult": 0.5, "food_mult": 1.2, "water_mult": 1.5},
    }