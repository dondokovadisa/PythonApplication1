def run_analysis(args, graph):
    """Выводит результаты анализа в консоль и сохраняет файлы."""
    print("Граф зависимостей (рёбра):")
    for src, dsts in graph.items():
        for d in dsts:
            print(f"  {src} -> {d}")
    print()

    if args.reverse:
        rev = reverse_deps(args.package, graph)
        print(f"Обратные зависимости для '{args.package}':")
        if rev:
            for r in rev:
                print(f"  {r}")
        else:
            print("  (нет)")
        print()

    if args.ascii:
        print("ASCII-дерево зависимостей:")
        print_ascii_tree(args.package, graph)
        print()

    puml = to_plantuml(args.package, graph)
    save_svg(puml, args.output)
    
    mermaid_code = to_mermaid(args.package, graph)
    mmd_path = os.path.splitext(args.output)[0] + ".mmd"
    with open(mmd_path, "w", encoding="utf-8") as f:
        f.write(mermaid_code)
        
    print(f"SVG/PlantUML сохранён в: {args.output}")
    print(f"Mermaid сохранён в: {mmd_path}")


def main():
    """Точка входа в программу."""
    args = parse_args()
    try:
        validate(args)
    except ConfigError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

    print_config(args)
    print()

    if args.mode == "test":
        base_graph = load_test_graph(args.repo)
        fetch_fn = lambda name: base_graph.get(name, [])
    else:
        fetch_fn = lambda name: get_direct_deps(name, args.repo)

    graph = build_graph(args.package, fetch_fn, args.depth, args.exclude)
    run_analysis(args, graph)