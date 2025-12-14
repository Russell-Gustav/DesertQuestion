from typing import List, Dict, Literal, Optional
import numpy as np
from src.configs import DayCondition

WeatherStr = Literal["Sunny", "Hot", "Sand"]

def _normalize_probs(dist: Dict[WeatherStr, float]) -> Dict[WeatherStr, float]:
    total = float(sum(dist.values()))
    if total <= 0:
        raise ValueError("Probability distribution sums to zero.")
    return {k: v / total for k, v in dist.items()}

def generate_weather_days_iid(
    days: int,
    seed: int,
    probs: Dict[WeatherStr, float],
) -> List[WeatherStr]:
    """
    独立同分布采样天气序列。
    """
    probs = _normalize_probs(probs)
    rng = np.random.default_rng(seed)
    weathers = list(probs.keys())
    p = [probs[w] for w in weathers]
    return list(rng.choice(weathers, size=days, p=p))

def to_day_conditions(seq: List[WeatherStr]) -> List[DayCondition]:
    return [
        DayCondition(
            day=i + 1,
            max_travel_dist=0.0,
            food_consumption=0.0,
            water_consumption=0.0,
            weather=w,
        )
        for i, w in enumerate(seq)
    ]

def generate_level_conditions(
    level: Literal["第三关", "第四关", "第六关"],
    seed: int = 42,
) -> List[DayCondition]:
    """
    按要求生成各关卡天气条件：
    - 第三关：10天，仅晴朗(Sunny)与高温(Hot)，等概率
    - 第四关、第六关：30天，沙暴(Sand)10%，晴朗(Sunny)45%，高温(Hot)45%
    """
    if level == "第三关":
        days = 10
        probs = {"Sunny": 0.5, "Hot": 0.5}
    elif level in ("第四关", "第六关"):
        days = 30
        probs = {"Sand": 0.1, "Sunny": 0.45, "Hot": 0.45}
    else:
        raise ValueError(f"Unsupported level for generator: {level}")

    seq = generate_weather_days_iid(days=days, seed=seed, probs=probs)
    return to_day_conditions(seq)
