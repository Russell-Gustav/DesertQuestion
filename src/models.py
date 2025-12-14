from dataclasses import dataclass
from typing import Dict, Optional, List
from .configs import ProblemConfig, MapGraphNode, SupplyPoint

PositionType = str  # 节点 id

@dataclass
class State:
    day: int
    position: PositionType
    food: float
    water: float
    cash: float
    history: List[Dict]

@dataclass
class Action:
    next_node_id: Optional[str] = None
    buy_food: float = 0.0
    buy_water: float = 0.0
    sell_food: float = 0.0
    sell_water: float = 0.0
    rest: bool = False

class Environment:
    def __init__(self, cfg: ProblemConfig):
        self.cfg = cfg
        self.map_graph = cfg.map_graph
        # 简化：将 village/mine/start 视为可补给点，价格统一为 Params 的 food_cost/water_cost（若有）
        default_food_price = 8.0
        default_water_price = 5.0
        for node in self.map_graph.nodes.values():
            if node.type in ("village", "mine", "start"):
                node.supply = SupplyPoint(
                    id=node.id, name=node.name,
                    buy_price_food=default_food_price,
                    buy_price_water=default_water_price
                )

    def start_node(self) -> str:
        for nid, n in self.map_graph.nodes.items():
            if n.type == "start":
                return nid
        return list(self.map_graph.nodes.keys())[0]

    def end_node(self) -> str:
        for nid, n in self.map_graph.nodes.items():
            if n.type == "end":
                return nid
        return list(self.map_graph.nodes.keys())[-1]

    def reached_end(self, state: State) -> bool:
        node = self.map_graph.nodes.get(state.position)
        return node is not None and node.type == "end"

    def _apply_weather(self, day_idx: int):
        day = self.cfg.day_conditions[day_idx]
        weather = day.weather or "Sunny"
        mults = (self.cfg.weather_rules or {}).get(weather, {"travel_mult":1.0,"food_mult":1.0,"water_mult":1.0})

        max_travel = self.cfg.travel_base * mults["travel_mult"]
        food_cons  = self.cfg.food_base   * mults["food_mult"]
        water_cons = self.cfg.water_base  * mults["water_mult"]
        return max_travel, food_cons, water_cons

    def step(self, state: State, action: Action) -> Optional[State]:
        day_idx = state.day - 1
        if day_idx >= self.cfg.days:
            return None

        max_travel, food_cons, water_cons = self._apply_weather(day_idx)

        next_pos = state.position
        travel_dist = 0.0
        if not action.rest and action.next_node_id:
            neigh = dict(self.map_graph.adjacency.get(state.position, []))
            if action.next_node_id not in neigh:
                return None
            dist = neigh[action.next_node_id]
            if dist > max_travel:
                return None
            travel_dist = dist
            next_pos = action.next_node_id

        next_cash = state.cash
        next_food = state.food + action.buy_food - action.sell_food
        next_water = state.water + action.buy_water - action.sell_water

        cur_node = self.map_graph.nodes.get(state.position)
        if cur_node and cur_node.supply:
            sp = cur_node.supply
            next_cash -= action.buy_food * sp.buy_price_food
            next_cash -= action.buy_water * sp.buy_price_water
            if sp.sell_price_food:
                next_cash += action.sell_food * sp.sell_price_food
            if sp.sell_price_water:
                next_cash += action.sell_water * sp.sell_price_water

        bag = self.cfg.bag_cfg
        weight = next_food * bag.food_unit_weight + next_water * bag.water_unit_weight
        if weight > bag.max_weight:
            return None

        # 当日消耗
        next_food -= food_cons
        next_water -= water_cons
        if next_food < 0 or next_water < 0:
            return None

        next_day = state.day + 1
        next_history = list(state.history)
        next_history.append({
            "day": state.day,
            "pos": state.position,
            "next_pos": next_pos,
            "move_dist": travel_dist,
            "buy_food": action.buy_food,
            "buy_water": action.buy_water,
            "sell_food": action.sell_food,
            "sell_water": action.sell_water,
            "cash": next_cash,
            "food": next_food,
            "water": next_water,
            "weather": self.cfg.day_conditions[day_idx].weather
        })

        return State(
            day=next_day,
            position=next_pos,
            food=next_food,
            water=next_water,
            cash=next_cash,
            history=next_history
        )