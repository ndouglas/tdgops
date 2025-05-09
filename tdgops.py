import heapq
from collections import defaultdict
from typing import List, Dict, Tuple, NamedTuple, Optional

Type = str

class Cost(NamedTuple):
  time: int
  space: int
  side_effects: int  # 0 = pure, 1 = impure, etc.

Transform = Tuple[Type, Type, Cost, str]  # from_type, to_type, cost, name
TRANSFORMS: List[Transform] = [
  ("int[]", "int[]<sorted>",      Cost(5, 1, 0),    "sort"),
  ("int[]", "Set<int>",           Cost(3, 2, 0),    "to_set"),
  ("int[]", "bool",               Cost(10, 1, 0),   "brute_force_search"),
  ("int[]<sorted>", "bool",       Cost(1, 1, 0),    "binary_search"),
  ("Set<int>", "bool",            Cost(2, 2, 0),    "hash_lookup"),
  ("Set<int>", "List<int>",       Cost(4, 1, 1),    "to_list_impure"),
]

def score(cost: Cost, weights: Cost) -> int:
  return (
    cost.time * weights.time +
    cost.space * weights.space +
    cost.side_effects * weights.side_effects
  )

def add_cost(a: Cost, b: Cost) -> Cost:
  return Cost(
    time=a.time + b.time,
    space=a.space + b.space,
    side_effects=a.side_effects + b.side_effects
  )

graph: Dict[Type, List[Tuple[Type, Cost, str]]] = defaultdict(list)
for src, dst, cost, name in TRANSFORMS:
  graph[src].append((dst, cost, name))

def plan_transform(start: Type, goal: Type, weights: Cost) -> Optional[Tuple[List[str], Cost]]:
  heap = []
  heapq.heappush(heap, (0, start, [], Cost(0, 0, 0)))  # (priority_score, current_type, path_so_far, cost_so_far)
  visited: Dict[Type, int] = {}

  while heap:
    _, current, path, total_cost = heapq.heappop(heap)

    if current in visited and visited[current] <= score(total_cost, weights):
      continue
    visited[current] = score(total_cost, weights)

    if current == goal:
      return (path, total_cost)

    for neighbor, edge_cost, func_name in graph[current]:
      new_cost = add_cost(total_cost, edge_cost)
      priority = score(new_cost, weights)
      heapq.heappush(heap, (priority, neighbor, path + [func_name], new_cost))

  return None

if __name__ == "__main__":
  goal = "bool"
  start = "int[]"

  # ⚖️ Preference: minimize time, ignore space/side-effects
  weights = Cost(time=1, space=0, side_effects=0)
  result = plan_transform(start, goal, weights)
  print("\n[Minimize Time]")
  if result:
    path, cost = result
    print("Plan:", " -> ".join(path))
    print("Total Cost:", cost)
  else:
    print("No plan found.")

  # ⚖️ Preference: minimize space
  weights = Cost(time=0, space=1, side_effects=0)
  result = plan_transform(start, goal, weights)
  print("\n[Minimize Space]")
  if result:
    path, cost = result
    print("Plan:", " -> ".join(path))
    print("Total Cost:", cost)
  else:
    print("No plan found.")

  # ⚖️ Preference: minimize side effects (e.g. for FP systems)
  weights = Cost(time=0, space=0, side_effects=1)
  result = plan_transform(start, goal, weights)
  print("\n[Minimize Side Effects]")
  if result:
    path, cost = result
    print("Plan:", " -> ".join(path))
    print("Total Cost:", cost)
  else:
    print("No plan found.")
