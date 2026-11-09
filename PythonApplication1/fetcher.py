import json
import urllib.request
import re


NAME_RE = re.compile(r"^\s*([A-Za-z0-9._-]+)")


def _normalize(name: str) -> str:
    # PEP 503
    return re.sub(r"[-_.]+", "-", name).lower()


def get_direct_deps(package: str, repo_url: str = "https://pypi.org"):
    """
    Возвращает список имён прямых зависимостей пакета.
    Использует PyPI JSON API: <repo>/pypi/<package>/json -> info.requires_dist
    Никаких pip / pipdeptree.
    """
    base = repo_url.rstrip("/")
    url = f"{base}/pypi/{package}/json"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  [warn] не удалось получить данные для '{package}': {e}")
        return []

    requires = data.get("info", {}).get("requires_dist") or []
    deps = []
    for req in requires:
        # отбрасываем extras и маркеры окружения: "foo[bar]>=1.0; python_version<'3.8'"
        if ";" in req:
            # маркер окружения — по желанию можно учитывать; здесь пропускаем
            pass
        m = NAME_RE.match(req)
        if m:
            deps.append(_normalize(m.group(1)))
    # убрать дубликаты, сохранив порядок
    seen = set()
    out = []
    for d in deps:
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out