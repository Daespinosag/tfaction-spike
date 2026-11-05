#!/usr/bin/env python3
"""Calcula las units de Terragrunt afectadas por los archivos cambiados y las
fusiona con los targets que devolvio `list-targets` de tfaction.

Uso:
  affected-units.py --changed changed.txt --targets targets.json \
      [--terragrunt terragrunt] [--root .] [--with-dependents]

- changed.txt: un archivo cambiado por linea (ruta relativa a la raiz del repo).
- targets.json: salida JSON de list-targets (array de objetos con `target`).
- Imprime en stdout el array JSON fusionado (targets de tfaction + extras).
- Detalle en stderr: units afectadas y cuales se anadieron.

Como ve el modulo compartido: `terragrunt find --json --reading` lista, por
unit, los archivos que lee (incluye el .tf del `source` local de
terraform { source = ... }). Una unit queda afectada si un archivo cambiado
esta en el mismo directorio que alguno de los que lee, o bajo la propia unit.
`--dependencies` aporta el grafo para `--with-dependents` (opcional).
"""
import argparse
import json
import os
import subprocess
import sys


def under(path, directory):
    return path == directory or path.startswith(directory.rstrip("/") + "/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--changed", required=True)
    ap.add_argument("--targets", required=True)
    ap.add_argument("--terragrunt", default="terragrunt")
    ap.add_argument("--root", default=".")
    ap.add_argument("--with-dependents", action="store_true")
    a = ap.parse_args()

    changed = [l.strip() for l in open(a.changed) if l.strip()]
    targets = json.load(open(a.targets)) or []

    out = subprocess.run(
        [a.terragrunt, "find", "--working-dir", a.root, "--json",
         "--dependencies", "--reading", "--no-tips"],
        check=True, capture_output=True, text=True,
    ).stdout
    units = [u for u in json.loads(out) if u.get("type") == "unit"]

    affected = set()
    for u in units:
        p = u["path"]
        read_dirs = {os.path.dirname(r) for r in u.get("reading", [])}
        for f in changed:
            if under(f, p) or any(under(f, d) for d in read_dirs if d):
                affected.add(p)
                break

    if a.with_dependents:
        rdeps = {}
        for u in units:
            for d in u.get("dependencies", []):
                rdeps.setdefault(d, set()).add(u["path"])
        stack = list(affected)
        while stack:
            for dep in rdeps.get(stack.pop(), ()):
                if dep not in affected:
                    affected.add(dep)
                    stack.append(dep)

    have = {t["target"] for t in targets}
    added = sorted(affected - have)
    merged = list(targets)
    for p in added:
        merged.append({
            "target": p,
            "working_directory": p,
            "runs_on": "ubuntu-latest",
            "job_type": "terraform",
            "skip_terraform": False,
        })
    print("affected-units: afectadas=%s" % json.dumps(sorted(affected)), file=sys.stderr)
    print("affected-units: de list-targets=%s" % json.dumps(sorted(have)), file=sys.stderr)
    print("affected-units: anadidas=%s" % json.dumps(added), file=sys.stderr)
    json.dump(merged, sys.stdout)
    print()


if __name__ == "__main__":
    main()
