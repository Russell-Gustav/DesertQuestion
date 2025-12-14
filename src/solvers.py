from typing import List, Optional
from .config import ProblemConfig
from .models import Environment, State, Action

class BeamSearchSolver:
    def __init__(self, cfg: ProblemConfig, beam_width: int = 30):
        self.cfg = cfg
        self.env = Environment(cfg)
        self.beam_width = beam_width

    def neighbors(self, state: State) -> List[Action]:
        actions: List[Action] = [Action(rest=True)]
        for nid, _dist in self.env.map_graph.adjacency.get(state.position, []):
            actions.append(Action(next_node_id=nid))
        node = self.env.map_graph.nodes.get(state.position)
        if node and node.supply:
            for bf in [0, 2, 5]:
                for bw in [0, 2, 5]:
                    actions.append(Action(next_node_id=None, buy_food=bf, buy_water=bw, rest=True))
        return actions

    def score(self, s: State) -> float:
        end_id = self.env.end_node()
        dist_heur = 0 if s.position == end_id else 1
        return -dist_heur + 0.01*s.cash + 0.005*(s.food + s.water)

    def solve_once(self, init_state: State) -> Optional[State]:
        frontier = [init_state]
        best = None
        for _ in range(self.cfg.days - init_state.day + 1):
            candidates = []
            for s in frontier:
                if self.env.reached_end(s):
                    return s
                for a in self.neighbors(s):
                    ns = self.env.step(s, a)
                    if ns:
                        candidates.append(ns)
            if not candidates:
                return None
            candidates.sort(key=self.score, reverse=True)
            frontier = candidates[:self.beam_width]
            best = frontier[0]
        return best if best and self.env.reached_end(best) else None

    def solve_monte_carlo(self, init_state: State) -> Optional[State]:
        return self.solve_once(init_state)