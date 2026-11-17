import argparse
import sys
import os
from urllib.parse import urlparse

from fetcher import get_direct_deps
from graph import load_test_graph, build_graph, reverse_deps
from visualize import to_plantuml, save_svg, print_ascii_tree


class ConfigError(Exception):
    pass


def parse_args():
    p = argparse.ArgumentParser(description="Визуализатор графа зависимостей пакетов pip")
    p.add_argument("--package", "-p", required=True, help="Имя анализируемого пакета")
    p.add_argument("--repo", "-r", required=True, help="URL репозитория или путь к тестовому файлу")
    p.add_argument("--mode", "-m", required=True, choices=["online", "test"], help="Режим работы")
    p.add_argument("--output", "-o", required=True, help="Имя файла SVG")
    p.add_argument("--ascii", "-a", action="store_true", help="Вывод ASCII-дерева")
    p.add_argument("--depth", "-d", required=True, type=int, help="Максимальная глубина")
    p.add_argument("--exclude", "-e", default="", help="Подстрока для фильтрации пакетов")
    p.add_argument("--reverse", "-R", action="store_true", help="Показать обратные зависимости")
    return p.parse_args()


def validate(args):
    if not args.package.strip():
        raise ConfigError("--package не может быть пустым.")
    if args.depth < 0:
        raise ConfigError("--depth должен быть целым числом >= 0.")
    if not args.output.lower().endswith(".svg"):
        raise ConfigError("--output должен иметь расширение .svg.")

    if args.mode == "test":
        if not os.path.isfile(args.repo):
            raise ConfigError(f"--repo: файл '{args.repo}' не найден.")
    else:  # online
        parsed = urlparse(args.repo)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ConfigError("--repo должен быть корректным URL (http:// или https://) в режиме online.")


def print_config(args):
    print("Конфигурация приложения:")
    print(f"  package = {args.package}")
    print(f"  repo    = {args.repo}")
    print(f"  mode    = {args.mode}")
    print(f"  output  = {args.output}")
    print(f"  ascii   = {args.ascii}")
    print(f"  depth   = {args.depth}")
    print(f"  exclude = {args.exclude or '(не задано)'}")
    print(f"  reverse = {args.reverse}")


def main():
    args = parse_args()
    try:
        validate(args)
    except ConfigError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

    print_config(args)
    print()

    # Источник данных
    if args.mode == "test":
        base_graph = load_test_graph(args.repo)
        fetch_fn = lambda name: base_graph.get(name, [])
    else:
        fetch_fn = lambda name: get_direct_deps(name, args.repo)

    # Построение графа DFS
    graph = build_graph(args.package, fetch_fn, args.depth, args.exclude)

    # Печать графа (рёбра)
    print("Граф зависимостей (рёбра):")
    for src, dsts in graph.items():
        for d in dsts:
            print(f"  {src} -> {d}")
    print()

    # Обратные зависимости
    if args.reverse:
        rev = reverse_deps(args.package, graph)
        print(f"Обратные зависимости для '{args.package}':")
        if rev:
            for r in rev:
                print(f"  {r}")
        else:
            print("  (нет)")
        print()

    # ASCII-дерево
    if args.ascii:
        print("ASCII-дерево зависимостей:")
        print_ascii_tree(args.package, graph)
        print()

    # Визуализация
    puml = to_plantuml(args.package, graph)
    save_svg(puml, args.output)
    print(f"SVG сохранён в: {args.output}")


if __name__ == "__main__":
    main()
