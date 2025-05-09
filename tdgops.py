import heapq
from collections import defaultdict
from typing import List, Dict, Tuple, NamedTuple

Type = str

class Cost(NamedTuple):
  time: int
  space: int
  side_effects: int

def dominates(a: Cost, b: Cost) -> bool:
  return all(getattr(a, k) <= getattr(b, k) for k in a._fields) and any(
    getattr(a, k) < getattr(b, k) for k in a._fields
  )

def add_cost(a: Cost, b: Cost) -> Cost:
  return Cost(
    a.time + b.time,
    a.space + b.space,
    a.side_effects + b.side_effects,
  )

Transform = Tuple[Type, Type, Cost, str]

TRANSFORMS: List[Transform] = [
  ("int[]", "int[]<sorted>",      Cost(5, 1, 0), "sort"),
  ("int[]", "Set<int>",           Cost(3, 2, 0), "to_set"),
  ("int[]", "bool",               Cost(10, 1, 0), "brute_force_search"),
  ("int[]<sorted>", "bool",       Cost(1, 1, 0), "binary_search"),
  ("Set<int>", "bool",            Cost(2, 2, 0), "hash_lookup"),
  ("Set<int>", "List<int>",       Cost(4, 1, 1), "to_list_impure"),
]

graph: Dict[Type, List[Tuple[Type, Cost, str]]] = defaultdict(list)
for src, dst, cost, name in TRANSFORMS:
  graph[src].append((dst, cost, name))

def plan_pareto(start: Type, goal: Type) -> List[Tuple[List[str], Cost]]:
  heap = []
  heapq.heappush(heap, (0, start, [], Cost(0, 0, 0)))

  visited: Dict[Type, List[Tuple[List[str], Cost]]] = defaultdict(list)
  pareto_solutions: List[Tuple[List[str], Cost]] = []

  while heap:
    _, current, path, total_cost = heapq.heappop(heap)

    if current == goal:
      dominated = any(dominates(existing_cost, total_cost) for _, existing_cost in pareto_solutions)
      if not dominated:
        pareto_solutions = [
          (p, c) for (p, c) in pareto_solutions if not dominates(total_cost, c)
        ]
        pareto_solutions.append((path, total_cost))
      continue

    dominated = any(dominates(c, total_cost) for _, c in visited[current])
    if dominated:
      continue
    visited[current] = [
      (p, c) for (p, c) in visited[current] if not dominates(total_cost, c)
    ] + [(path, total_cost)]

    for neighbor, edge_cost, func_name in graph[current]:
      new_cost = add_cost(total_cost, edge_cost)
      heapq.heappush(heap, (sum(new_cost), neighbor, path + [func_name], new_cost))

  return pareto_solutions

if __name__ == "__main__":
  goal = "bool"
  start = "int[]"
  solutions = plan_pareto(start, goal)

  print(f"\nPareto-optimal plans to reach {goal} from {start}:")
  for path, cost in solutions:
    print(f"Plan: {' -> '.join(path):40}  Cost: {cost}")
