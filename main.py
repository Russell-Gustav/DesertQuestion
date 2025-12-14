import argparse
import os
import pandas as pd

from src.excel_loader import build_problem_config_from_excel
from src.weather_sim import WeatherMonteCarlo
from solvers import BeamSearchSolver
from src.models import State

def init_state_start(cfg) -> State:
    env = BeamSearchSolver(cfg).env
    start_id = env.start_node()
    return State(day=1, position=start_id, food=0.0, water=0.0, cash=cfg.econ_cfg.initial_cash, history=[])

def run_level_with_weather(cfg, samples: int, seed: int, output_prefix: str):
    mc = WeatherMonteCarlo(days=cfg.days, seed=seed)
    best_res = None
    best_cash = float("-inf")
    results = []

    for i in range(samples):
        conds = mc.generate_conditions(init_weather="Sunny")
        for d in range(cfg.days):
            cfg.day_conditions[d].weather = conds[d].weather

        solver = BeamSearchSolver(cfg, beam_width=40)
        s0 = init_state_start(cfg)
        res = solver.solve_monte_carlo(s0)
        if res:
            cash = res.cash
            results.append({"sample": i+1, "success": True, "cash": cash, "days_used": res.day - 1})
            if cash > best_cash:
                best_cash = cash
                best_res = res
        else:
            results.append({"sample": i+1, "success": False, "cash": None, "days_used": None})

    pd.DataFrame(results).to_excel(f"{output_prefix}_mc_summary.xlsx", index=False)
    if best_res:
        pd.DataFrame(best_res.history).to_excel(f"{output_prefix}_best_path.xlsx", index=False)
        print(f"Best cash={best_cash}, path saved to {output_prefix}_best_path.xlsx")
    else:
        print("No successful path found under Monte Carlo samples.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--excel", type=str, default=os.path.join("data", "game_data.xlsx"),
                        help="Excel path with sheets Map/Nodes/Weather/Params, default data/game_data.xlsx")
    parser.add_argument("--level", type=str, default="第二关", help="Level name tag used only for output file prefix")
    parser.add_argument("--samples", type=int, default=200, help="Monte Carlo samples for unknown weather levels")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--unknown_weather", action="store_true", help="Enable Monte Carlo for unknown-weather levels")
    args = parser.parse_args()

    cfg = build_problem_config_from_excel(args.excel, level_name=args.level)

    if args.unknown_weather:
        run_level_with_weather(cfg, samples=args.samples, seed=args.seed, output_prefix=f"Result_{args.level}")
    else:
        solver = BeamSearchSolver(cfg, beam_width=40)
        s0 = init_state_start(cfg)
        res = solver.solve_once(s0)
        if res:
            print("Reached end.", "day", res.day-1, "cash", res.cash)
            pd.DataFrame(res.history).to_excel(f"Result_{args.level}_path.xlsx", index=False)
        else:
            print("Failed to reach end under known weather.")

if __name__ == "__main__":
    main()