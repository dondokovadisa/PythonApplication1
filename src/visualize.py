import os
import subprocess
import shutil


def to_plantuml(root: str, graph: dict) -> str:
    lines = ["@startuml", "skinparam componentStyle rectangle"]
    lines.append(f"title Dependencies for {root}")
    
    for src, dsts in graph.items():
        if not dsts:
            lines.append(f'[{src}]')
        for d in dsts:
            lines.append(f'[{src}] --> [{d}]')
            
    lines.append("@enduml")
    return "\n".join(lines)


def save_svg(puml_text: str, out_svg: str):
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

    jar = "plantuml.jar"
    if os.path.isfile(jar):
        try:
            cmd = ["java", "-jar", jar, "-tsvg", puml_path]
            subprocess.run(cmd, check=True)
            return
        except Exception as e:
            print(f"  [warn] java -jar plantuml.jar: {e}")

    print("  [warn] plantuml не найден — сохранён только .puml.")


def to_mermaid(root: str, graph: dict) -> str:
    lines = ["graph TD"]
    for src, dsts in graph.items():
        if not dsts:
            lines.append(f'    {src}["{src}"]')
        for d in dsts:
            lines.append(f'    {src}["{src}"] --> {d}["{d}"]')
    return "\n".join(lines)


def print_ascii_tree(root: str, graph: dict):
    def rec(node, prefix, is_last, path):
        connector = "└── " if is_last else "├── "
        marker = " (цикл)" if node in path else ""
        print(prefix + connector + node + marker)
        
        if node in path:
            return
            
        path = path | {node}
        children = graph.get(node, [])
        
        if is_last:
            new_prefix = prefix + "    "
        else:
            new_prefix = prefix + "│   "
            
        for i, ch in enumerate(children):
            rec(ch, new_prefix, i == len(children) - 1, path)

    print(root)
    children = graph.get(root, [])
    for i, ch in enumerate(children):
        rec(ch, "", i == len(children) - 1, {root})