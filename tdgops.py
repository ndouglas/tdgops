import heapq
from collections import defaultdict
from typing import List, Dict, Tuple

Type = str
Transform = Tuple[Type, Type, int, str]  # (from, to, cost, name)

TRANSFORMS: List[Transform] = [
    ("int[]", "int[]<sorted>", 5, "sort"),
    ("int[]", "Set<int>", 3, "to_set"),
    ("int[]", "bool", 10, "brute_force_search"),
    ("int[]<sorted>", "bool", 1, "binary_search"),
    ("Set<int>", "bool", 2, "hash_lookup"),
]

graph: Dict[Type, List[Tuple[Type, int, str]]] = defaultdict(list)
for src, dst, cost, name in TRANSFORMS:
    graph[src].append((dst, cost, name))

def plan_transform(start: Type, goal: Type) -> List[str]:
  heap = []
  heapq.heappush(heap, (0, start, []))
  visited = {}

  while heap:
    cost, current, path = heapq.heappop(heap)

    if current in visited and visited[current] <= cost:
      continue
    visited[current] = cost

    if current == goal:
      return path

    for neighbor, edge_cost, func_name in graph[current]:
      heapq.heappush(heap, (cost + edge_cost, neighbor, path + [func_name]))

  return None

steps = plan_transform("int[]", "bool")
print("Plan:", " -> ".join(steps) if steps else "No plan found.")
