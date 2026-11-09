def load_test_graph(path: str) -> dict:
    """
    Читает файл тестового репозитория:
        A: B C
        B: D
        D: A
    Возвращает dict: пакет -> [зависимости].
    """
    graph = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                continue
            name, deps = line.split(":", 1)
            name = name.strip()
            deps = [d.strip() for d in deps.split() if d.strip()]
            graph[name] = deps
    return graph


def build_graph(root: str, fetch_fn, max_depth: int, exclude: str = "") -> dict:
    """
    Рекурсивный DFS. Возвращает dict рёбер: пакет -> [зависимости].
    Учитывает max_depth, exclude (подстрока в имени), циклы.
    """
    graph = {}
    visited = set()

    def dfs(pkg: str, depth: int):
        if pkg in visited:
            return
        visited.add(pkg)
        if depth >= max_depth:
            graph.setdefault(pkg, [])
            return
        deps = fetch_fn(pkg) or []
        # фильтр по подстроке
        deps = [d for d in deps if not (exclude and exclude.lower() in d.lower())]
        graph.setdefault(pkg, [])
        for d in deps:
            if d not in graph[pkg]:
                graph[pkg].append(d)
            dfs(d, depth + 1)

    dfs(root, 0)
    return graph


def reverse_deps(target: str, graph: dict) -> list:
    """Пакеты, которые зависят от target."""
    result = []
    for src, dsts in graph.items():
        if target in dsts and src != target:
            result.append(src)
    return sorted(set(result))