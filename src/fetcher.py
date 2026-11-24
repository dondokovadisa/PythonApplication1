import json
import urllib.request
import re


NAME_RE = re.compile(r"^\s*([A-Za-z0-9._-]+)")


def _normalize(name: str) -> str:
    # PEP 503
    return re.sub(r"[-_.]+", "-", name).lower()


def get_direct_deps(package: str, repo_url: str = "https://pypi.org") -> list:
    base = repo_url.rstrip("/")
    url = f"{base}/pypi/{package}/json"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        msg = f"  [warn] не удалось получить данные для '{package}': {e}"
        print(msg)
        return []

    requires = data.get("info", {}).get("requires_dist") or []
    deps = []
    for req in requires:
        m = NAME_RE.match(req)
        if m:
            deps.append(_normalize(m.group(1)))
            
    seen = set()
    out = []
    for d in deps:
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out