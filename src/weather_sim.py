import numpy as np
from typing import List, Dict
from .configs import DayCondition, WeatherType

class WeatherMonteCarlo:
    def __init__(self, days: int, seed: int = 42,
                 base_probs: Dict[WeatherType, float] = None,
                 transition: Dict[WeatherType, Dict[WeatherType, float]] = None):
        self.days = days
        self.rng = np.random.default_rng(seed)
        self.base_probs = base_probs or {
            "Sunny": 0.5,
            "Hot":   0.3,
            "Sand":  0.2
        }
        self.transition = transition or {
            "Sunny": {"Sunny": 0.6, "Hot": 0.25, "Sand": 0.15},
            "Hot":   {"Sunny": 0.4, "Hot": 0.4,  "Sand": 0.2},
            "Sand":  {"Sunny": 0.3, "Hot": 0.3,  "Sand": 0.4},
        }

    def sample_sequence(self, init_weather: WeatherType = "Sunny") -> List[WeatherType]:
        seq = [init_weather]
        for _ in range(1, self.days):
            prev = seq[-1]
            probs = self.transition.get(prev, self.base_probs)
            weathers = list(probs.keys())
            p = np.array(list(probs.values()), dtype=float)
            p = p / p.sum()
            next_w = self.rng.choice(weathers, p=p)
            seq.append(next_w)
        return seq

    def generate_conditions(self, init_weather: WeatherType = "Sunny") -> List[DayCondition]:
        seq = self.sample_sequence(init_weather)
        return [DayCondition(day=i+1, max_travel_dist=0.0, food_consumption=0.0,
                             water_consumption=0.0, weather=w)
                for i, w in enumerate(seq)]