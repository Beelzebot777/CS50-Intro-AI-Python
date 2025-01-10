# Búsqueda en Profundidad (DFS) - Resumen

La búsqueda en profundidad (Depth First Search, DFS) es un algoritmo fundamental para explorar y recorrer grafos o árboles de manera exhaustiva.

---

## Concepto Básico
DFS explora tan profundamente como sea posible por cada rama antes de retroceder, lo que lo hace ideal para:
- Detectar ciclos en grafos.
- Resolver problemas de conectividad.
- Generar recorridos en grafos.

---

## Características Clave
1. **Tipos de Estructura de Datos Utilizadas:**
   - **Recursiva:** Utiliza la pila de llamadas del sistema.   
   - **Iterativa:** Emplea una pila explícita para mantener el seguimiento de los nodos.

2. **Complejidad Temporal:**
   - **O(V + E):** Siendo V el numero de vértices y E el numero de aristas del grafo.

3. **Complejidad Espacial:**
   - **O(V):** Dependiendo de la implementación y del espacio requerido para el almacenamiento de nodos visitados.

---

## Implementación
### Recursiva
```python
# Implementación recursiva de DFS

def dfs_recursive(graph, node, visited):
    if node not in visited:
        print(node)
        visited.add(node)
        for neighbor in graph[node]:
            dfs_recursive(graph, neighbor, visited)

# Ejemplo de uso
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}
visited = set()
dfs_recursive(graph, 'A', visited)
```

### Iterativa
```python
# Implementación iterativa de DFS

def dfs_iterative(graph, start):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()
        if node not in visited:
            print(node)
            visited.add(node)
            stack.extend(graph[node])

# Ejemplo de uso
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}
dfs_iterative(graph, 'A')
```

---

## Aplicaciones
- Resolver laberintos.
- Detectar ciclos en grafos dirigidos.
- Encontrar componentes conexas.
- Resolver problemas de backtracking (e.g., Sudoku).

---

## Ventajas
- Fácil de implementar.
- Requiere menos memoria en su versión recursiva.

## Desventajas
- Puede quedarse atascado en bucles en grafos cíclicos si no se lleva un registro de nodos visitados.
- No garantiza el camino más corto (en comparación con BFS).

---

## Consideraciones
- Útil en grafos densos donde el orden de exploración importa.
- Elegir entre la versión iterativa o recursiva depende de las limitaciones de memoria y el entorno de ejecución.

