#!/usr/bin/env python3
"""Compile the full suite from isolated copies; run from any directory."""
import argparse
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--only-cached", action="store_true")
parser.add_argument("--update-example", action="store_true", help="copy the validated main PDF into the repository")
args = parser.parse_args()
out = ROOT / ".build" / "validation"
out.mkdir(parents=True, exist_ok=True)
sources = [ROOT / "tempus-template.tex", *sorted((ROOT / "examples").glob("*.tex"))]
failures = []
for source in sources:
    work = out / source.stem
    work.mkdir(exist_ok=True)
    for filename in ("tempusreport.cls", "acl_natbib.bst", "reference.bib"):
        shutil.copy2(ROOT / filename, work / filename)
    shutil.copytree(ROOT / "examples", work / "examples", dirs_exist_ok=True)
    shutil.copy2(source, work / source.name)
    cmd = ["tectonic", "--keep-logs", "--keep-intermediates"]
    if args.only_cached:
        cmd.append("--only-cached")
    result = subprocess.run([*cmd, source.name], cwd=work, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (work / "build-output.txt").write_text(result.stdout)
    log = (work / (source.stem + ".log"))
    content = log.read_text(errors="replace") if log.exists() else result.stdout
    issues = re.findall(r"^.*(?:Overfull|Underfull|undefined|multiply defined|Missing character|LaTeX Warning|Package .* Warning).*$", content, re.MULTILINE)
    if result.returncode or issues:
        failures.append(source.stem)
        print(f"FAIL {source.stem}: exit {result.returncode}", flush=True)
        print("\n".join(issues) or result.stdout[-4000:], flush=True)
    else:
        print(f"PASS {source.stem}", flush=True)
# Disabled options must not load optional content packages.
for name in ("default", "banner", "nobanner", "wide", "empty", "long-metadata", "art-flat", "art-cuboid"):
    log = out / name / (name + ".log")
    if log.exists() and re.search(r"(?:^|[/\s(])(algorithm|algpseudocode|listings)\.sty", log.read_text(errors="replace")):
        failures.append(name)
        print(f"FAIL {name}: disabled optional package loaded")
for name, forbidden in (("algorithms", "listings"), ("listings", "algpseudocode")):
    log = out / name / (name + ".log")
    if log.exists() and forbidden + ".sty" in log.read_text(errors="replace"):
        failures.append(name)
        print(f"FAIL {name}: {forbidden} loaded")
# Verify appendix section and object numbering, including a second reset.
aux_path = out / "tempus-template" / "tempus-template.aux"
if aux_path.exists():
    aux = aux_path.read_text(errors="replace")
    expected = {"sec:appendix": "A", "sec:appendix-details": "B",
                "eq:appendix": "A.1", "eq:appendix-second": "B.1",
                "fig:appendix": "A.1", "tab:appendix": "A.1",
                "alg:appendix": "A.1", "lst:appendix": "A.1"}
    for key, number in expected.items():
        if "\\newlabel{" + key + "}{{" + number + "}" not in aux:
            failures.append("appendix numbering: " + key)
    if "\\newlabel{sec:appendix@cref}{{[appendix]" not in aux:
        failures.append("appendix reference name")
if failures:
    raise SystemExit("Validation failed: " + ", ".join(failures))
if args.update_example:
    shutil.copy2(out / "tempus-template" / "tempus-template.pdf", ROOT / "tempus-template.pdf")
print(f"Validated {len(sources)} documents. PDFs and logs: {out}")
