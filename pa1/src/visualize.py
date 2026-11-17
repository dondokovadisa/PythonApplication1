import os
import subprocess
import shutil


def to_plantuml(root: str, graph: dict) -> str:
    # Явно указываем PlantUML, что это граф (component diagram)
    lines = ["@startuml", "skinparam componentStyle rectangle"]
    
    # Для графа заголовок лучше делать в комментарии
    lines.append(f"title Dependencies for {root}")
    
    for src, dsts in graph.items():
        if not dsts:
            # Изолированные узлы тоже добавляем в граф
            lines.append(f'[{src}]')
        for d in dsts:
            # Используем синтаксис с квадратными скобками для компонентов
            lines.append(f'[{src}] --> [{d}]')
            
    lines.append("@enduml")
    return "\n".join(lines)

def save_svg(puml_text: str, out_svg: str):
    """
    Пишет .puml рядом с .svg и пытается отрендерить через plantuml.
    Если plantuml не установлен — сохраняет только .puml и предупреждает.
    """
    puml_path = os.path.splitext(out_svg)[0] + ".puml"
    with open(puml_path, "w", encoding="utf-8") as f:
        f.write(puml_text)

    plantuml = shutil.which("plantuml")
    if plantuml:
        try:
            subprocess.run([plantuml, "-tsvg", puml_path], check=True)
            return
        except subprocess.CalledProcessError as e:
            print(f"  [warn] plantuml вернул ошибку: {e}")

    # fallback: java -jar plantuml.jar
    jar = "plantuml.jar"
    if os.path.isfile(jar):
        try:
            subprocess.run(["java", "-jar", jar, "-tsvg", puml_path], check=True)
            return
        except Exception as e:
            print(f"  [warn] java -jar plantuml.jar: {e}")

    print("  [warn] plantuml не найден — сохранён только .puml (SVG не создан).")


def print_ascii_tree(root: str, graph: dict):
    """Печать дерева зависимостей с правильными отступами."""
    
    def rec(node, prefix, is_last, path):
        connector = "└── " if is_last else "├── "
        marker = " (цикл)" if node in path else ""
        print(prefix + connector + node + marker)
        
        if node in path:
            return
            
        path = path | {node}
        children = graph.get(node, [])
        
        # Формируем префикс для детей
        if is_last:
            new_prefix = prefix + "    "
        else:
            new_prefix = prefix + "│   "
            
        for i, ch in enumerate(children):
            rec(ch, new_prefix, i == len(children) - 1, path)

    print(root)
    children = graph.get(root, [])
    for i, ch in enumerate(children):
        # Для корня префикс пустой
        rec(ch, "", i == len(children) - 1, {root})