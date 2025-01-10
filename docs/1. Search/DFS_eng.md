# Depth-First Search (DFS)

## Overview
Depth-First Search (DFS) is an algorithm for traversing or searching graph or tree data structures. It starts at a source node and explores as far as possible along each branch before backtracking.

---

## Characteristics
- **Type**: Graph traversal (or tree traversal).
- **Order**: Explores depth before breadth.
- **Structure Used**:
  - **Recursive version**: Utilizes the system’s call stack (implicit).
  - **Iterative version**: Requires an explicit stack data structure.

---

## Applications
1. **Pathfinding** in mazes or puzzles.
2. **Cycle detection** in graphs.
3. Topological sorting of Directed Acyclic Graphs (DAGs).
4. Solving connected components in graphs.
5. Parsing expressions in compilers (syntax trees).

---

## Algorithm

### Recursive Implementation
```python
# DFS Recursive Function
def dfs_recursive(graph, node, visited):
    if node not in visited:
        visited.add(node)
        print(node)  # Process the node
        for neighbor in graph[node]:
            dfs_recursive(graph, neighbor, visited)

# Example Usage
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': []
}
visited = set()
dfs_recursive(graph, 'A', visited)
```

### Iterative Implementation
```python
# DFS Iterative Function
def dfs_iterative(graph, start):
    stack = [start]
    visited = set()

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            print(node)  # Process the node
            stack.extend(reversed(graph[node]))  # Add neighbors to stack

# Example Usage
dfs_iterative(graph, 'A')
```

---

## Complexity
- **Time Complexity**:
  - \( O(V + E) \) where \( V \) is the number of vertices and \( E \) is the number of edges.
- **Space Complexity**:
  - Recursive: \( O(V) \) for call stack in worst case.
  - Iterative: \( O(V) \) for the explicit stack.

---

## Advantages
- Simple and easy to implement.
- Uses less memory than BFS when searching deep trees/graphs.

## Disadvantages
- May explore unnecessary paths in large or infinite graphs.
- Can get stuck in cycles (unless properly handled).

---

## Key Points
- DFS is inherently **stack-based** (explicit or implicit).
- **Recursive DFS** is concise but can lead to stack overflow in deep graphs.
- **Iterative DFS** avoids recursion and is more robust for large graphs.

---

Use DFS when depth exploration is critical, and cycle handling is ensured!

