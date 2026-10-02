#!/usr/bin/env python3
"""Build isolated report fixtures and inspect logs, navigation, and pagination."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

try:
    from pypdf import PdfReader
except ImportError:
    raise SystemExit('Install validation dependencies: python3 -m pip install -r scripts/requirements.txt')

if not __debug__:
    raise SystemExit('Validation requires Python assertions; do not use -O or PYTHONOPTIMIZE')

ROOT = Path(__file__).resolve().parents[1]


def run(command, work):
    result = subprocess.run(command, cwd=work, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return result.returncode, result.stdout


def build(source, work, engine, cached, staged_asset=None):
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    for filename in ('tempusreport.cls', 'acl_natbib.bst', 'reference.bib'):
        shutil.copy2(ROOT / filename, work / filename)
    shutil.copytree(ROOT / 'examples', work / 'examples')
    if staged_asset is not None:
        shutil.copy2(staged_asset, work / 'examples' / 'assets' / 'mark.pdf')
    shutil.copy2(source, work / source.name)
    if engine == 'tectonic':
        commands = [['tectonic', '--keep-logs', '--keep-intermediates',
                     *(['--only-cached'] if cached else []), source.name]]
    else:
        latex = [engine, '-interaction=nonstopmode', '-halt-on-error',
                 '-file-line-error', source.name]
        code, output = run(latex, work)
        outputs = [output]
        aux = work / (source.stem + '.aux')
        if code == 0 and aux.exists() and r'\bibdata' in aux.read_text():
            code, output = run(['bibtex', source.stem], work)
            outputs.append(output)
        # Resolve bibliography and navigation, including delayed index writes.
        commands = [latex, latex, latex] if code == 0 else []
        if code:
            (work / 'build-output.txt').write_text('\n'.join(outputs))
            return code
    if engine == 'tectonic':
        outputs = []
    for command in commands:
        code, output = run(command, work)
        outputs.append(output)
        if code:
            break
    (work / 'build-output.txt').write_text('\n'.join(outputs))
    return code


def class_warnings(log):
    messages = re.findall(r'^Class tempusreport Warning: (.*(?:\n\(tempusreport\).*|\n[^\n]+)*?)(?:\.\n\n|\n\n)', log, re.M)
    return [' '.join(re.sub(r'\(tempusreport\)', '', m).split()).rstrip('.') for m in messages]


def inspect_pdf(path):
    reader = PdfReader(path)
    pages = [' '.join((page.extract_text() or '').split()) for page in reader.pages]
    page_ids = {page.indirect_reference.idnum for page in reader.pages}
    destinations = reader.named_destinations
    def check_destination(dest):
        if isinstance(dest, str):
            assert dest in destinations, f'unresolved destination {dest}'
        else:
            first = dest[0]
            assert getattr(first, 'idnum', None) in page_ids or (isinstance(first, int) and 0 <= first < len(reader.pages)), 'invalid page destination'
    for name, dest in destinations.items():
        assert reader.get_destination_page_number(dest) is not None, f'invalid named destination {name}'
    outline_count = 0
    def outlines(items):
        nonlocal outline_count
        for item in items:
            if isinstance(item, list):
                outlines(item)
            else:
                assert reader.get_destination_page_number(item) is not None, 'invalid bookmark'
                outline_count += 1
    outlines(reader.outline)
    internal = external = 0
    for page in reader.pages:
        for ref in page.get('/Annots', []):
            annotation = ref.get_object()
            action = annotation.get('/A', {})
            if '/Dest' in annotation:
                check_destination(annotation['/Dest'])
                internal += 1
            elif action.get('/S') == '/GoTo':
                check_destination(action['/D'])
                internal += 1
            elif action.get('/S') == '/URI':
                assert action.get('/URI'), 'empty external link'
                external += 1
    assert reader.metadata.title, 'missing PDF title metadata'
    return pages, {'pages': len(pages), 'title': reader.metadata.title,
                   'author': reader.metadata.author, 'bookmarks': outline_count,
                   'destinations': len(destinations), 'internal_links': internal,
                   'external_links': external}


def label_number(aux, key):
    match = re.search(r'\\newlabel\{' + re.escape(key) + r'\}\{\{([^}]*)\}', aux)
    assert match, f'missing label {key}'
    return match[1]


def check_behavior(name, work, pages, evidence):
    aux = (work / (name + '.aux')).read_text(errors='replace')
    if name != 'empty':
        assert evidence['author'], 'missing PDF author metadata'
    if name == 'tempus-template':
        expected = {'sec:appendix': 'A', 'sec:appendix-details': 'B',
                    'eq:appendix': 'A.1', 'eq:appendix-second': 'B.1',
                    'fig:appendix': 'A.1', 'tab:appendix': 'A.1',
                    'alg:appendix': 'A.1', 'lst:appendix': 'A.1'}
        for key, number in expected.items():
            assert label_number(aux, key) == number, f'appendix numbering: {key}'
        assert r'\newlabel{sec:appendix@cref}{{[appendix]' in aux
        assert evidence['bookmarks'] >= 20 and evidence['internal_links'] >= 80
        assert evidence['external_links'] >= 5
        text = ' '.join(pages)
        for heading in ('Contents', 'List of Figures', 'List of Tables', 'List of Algorithms', 'Listings'):
            assert heading in text, f'missing navigation index {heading}'
    if name == 'listing-pagination':
        layout = '\n'.join(page.extract_text(extraction_mode='layout') for page in PdfReader(work / (name + '.pdf')).pages)
        assert any(re.search(r'Inline:\s*inlinecode\.', line) for line in layout.splitlines()), 'inline listing was split into paragraphs'
        for caption, first, second, before in (
                ('CAPENV', 'FIRSTENV', 'SECONDENV', 'Before environment'),
                ('CAPFILE', 'FIRSTFILE', 'SECONDFILE', 'Before external')):
            first_page = next(i for i, text in enumerate(pages) if first in text)
            assert caption in pages[first_page] and second in pages[first_page], 'caption/code split'
            assert before not in pages[first_page], 'near-bottom listing did not move'
        start = next(i for i, text in enumerate(pages) if 'FIRSTFILE' in text)
        end = next(i for i, text in enumerate(pages) if 'LASTFILE' in text)
        assert end > start, 'long listing no longer breaks'
        assert label_number(aux, 'lst:env') == '1' and label_number(aux, 'lst:file') == '2'
        assert label_number(aux, 'lst:float') == '3'
        for i in range(3, 101):
            assert f'checkpoint{i:03d}' in ' '.join(pages), f'lost listing line {i}'
    if name == 'continuations':
        assert label_number(aux, 'lst:original') == '1'
        assert label_number(aux, 'alg:original') == '1'
        lol = (work / (name + '.lol')).read_text()
        loa = (work / (name + '.loa')).read_text()
        assert lol.count(r'\contentsline') == loa.count(r'\contentsline') == 2, 'duplicate continuation index'
        assert label_number(aux, 'lst:next') == '2', 'continuation consumed listing number'
        assert label_number(aux, 'alg:next') == '2', 'continuation consumed algorithm number'
        text = ' '.join(pages)
        assert 'Listing 1. Continued' in text and 'Algorithm 1. Continued' in text
        assert 'Continuing box (continued)' in text
        # Numbering must resume at 3 after the two-line first segment.
        assert re.search(r'3\s+checkpoint003', text), 'listing numbers did not continue'
        assert re.search(r'2\s+x', text), 'algorithm numbers did not continue'


def rendered_equal(old, new, work):
    """Ignore metadata; allow minor rasterizer antialiasing differences only."""
    old_reader, new_reader = PdfReader(old), PdfReader(new)
    assert len(old_reader.pages) == len(new_reader.pages), 'tracked PDF page-count drift'
    for a, b in zip(old_reader.pages, new_reader.pages):
        assert ' '.join(a.extract_text().split()) == ' '.join(b.extract_text().split()), 'tracked PDF text drift'
    renders = work / 'drift'
    renders.mkdir(exist_ok=True)
    for label, pdf in [('tracked', old), ('generated', new)]:
        code, output = run(['pdftoppm', '-r', '72', str(pdf), str(renders / label)], work)
        assert code == 0, output
    def ppm(path):
        with path.open('rb') as stream:
            header = stream.readline()
            dimensions = stream.readline()
            while dimensions.startswith(b'#'):
                dimensions = stream.readline()
            maximum = stream.readline()
            return header + dimensions + maximum, stream.read()
    for a, b in zip(sorted(renders.glob('tracked-*.ppm')), sorted(renders.glob('generated-*.ppm'))):
        ha, pa = ppm(a); hb, pb = ppm(b)
        assert ha == hb and len(pa) == len(pb), 'tracked PDF size drift'
        different = sum(abs(x-y) > 16 for x, y in zip(pa, pb))
        assert different <= len(pa) * .001, f'tracked PDF visual drift: {a.name}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', choices=['tectonic', 'pdflatex', 'xelatex', 'lualatex'], default='tectonic')
    parser.add_argument('--only-cached', action='store_true')
    parser.add_argument('--rebuild-assets', action='store_true')
    parser.add_argument('--update-example', action='store_true')
    parser.add_argument('--check-example', action='store_true')
    args = parser.parse_args()
    if (args.update_example or args.check_example or args.rebuild_assets) and args.engine != 'tectonic':
        parser.error('asset/PDF publishing and drift checks require the canonical Tectonic engine')
    if args.update_example and args.check_example:
        parser.error('choose either --update-example or --check-example')
    if args.only_cached and args.engine != 'tectonic':
        parser.error('--only-cached is specific to Tectonic')
    if not shutil.which(args.engine):
        parser.error(f'{args.engine} is not installed')
    if args.engine != 'tectonic' and not shutil.which('bibtex'):
        parser.error('TeX Live engine validation requires BibTeX')
    if args.check_example and not shutil.which('pdftoppm'):
        parser.error('--check-example requires Poppler pdftoppm')
    out = ROOT / '.build' / 'validation' / args.engine
    out.mkdir(parents=True, exist_ok=True)
    _, version = run([args.engine, '--version'], out)
    toolchain = version + '\nPython: ' + sys.version
    if args.engine != 'tectonic':
        _, bibtex_version = run(['bibtex', '--version'], out)
        toolchain += '\nBibTeX: ' + bibtex_version
    (out / 'toolchain.txt').write_text(toolchain)
    expected = json.loads((ROOT / 'examples' / 'expected-warnings.json').read_text())
    sources = [ROOT / 'tempus-template.tex', ROOT / 'tempus-starter.tex', *sorted((ROOT / 'examples').glob('*.tex'))]
    failures, report = [], {}
    if args.rebuild_assets:
        sources.insert(0, ROOT / 'examples' / 'assets' / 'mark.tex')
    staged_asset = None
    for source in sources:
        name = source.stem
        work = out / name
        try:
            code = build(source, work, args.engine, args.only_cached, staged_asset)
            assert code == 0, 'compilation failed; see build-output.txt'
            log = (work / (name + '.log')).read_text(errors='replace')
            issues = re.findall(r'^.*(?:Overfull|Underfull|undefined|multiply defined|Missing character|LaTeX Warning|Package .* Warning|Class (?!tempusreport).* Warning).*$', log, re.M)
            assert not issues, '\n'.join(issues)
            actual = class_warnings(log)
            assert Counter(actual) == Counter(expected.get(name, [])), f'class warnings: {actual}; expected {expected.get(name, [])}'
            match = re.search(r'\\documentclass(?:\[([^]]*)\])?', source.read_text())
            options = match[1].split(',') if match and match[1] else []
            for option, packages in [('algorithms', ['algorithm', 'algpseudocode']), ('listings', ['listings', 'needspace'])]:
                for package in packages:
                    loaded = bool(re.search(r'(?:^|[/\s(])' + package + r'\.sty', log))
                    assert loaded == (option in options), f'optional package activation: {package}'
            if name != 'mark':
                pages, evidence = inspect_pdf(work / (name + '.pdf'))
                # Empty-author reports intentionally omit author metadata.
                titles = re.findall(r'\\title\{([^{}]*)\}', source.read_text())
                if titles:
                    assert evidence['title'] == titles[-1], 'PDF title does not match source metadata'
                check_behavior(name, work, pages, evidence)
                report[name] = evidence
            if name == 'mark':
                staged_asset = work / 'mark.pdf'
                assert staged_asset.exists(), 'asset export produced no PDF'
            print(f'PASS {name}', flush=True)
        except (AssertionError, ValueError, OSError, StopIteration) as error:
            failures.append(name)
            print(f'FAIL {name}: {error}', flush=True)
    # Always preserve machine-readable inspection evidence, even on failure.
    (out / 'inspection.json').write_text(json.dumps({'engine': args.engine, 'documents': report, 'failures': failures}, indent=2)+'\n')
    if failures:
        raise SystemExit('Validation failed: ' + ', '.join(failures))
    if args.check_example:
        rendered_equal(ROOT / 'tempus-template.pdf', out / 'tempus-template' / 'tempus-template.pdf', out)
        print('PASS tracked example text/render drift')
    if args.rebuild_assets:
        shutil.copy2(out / 'mark' / 'mark.pdf', ROOT / 'examples' / 'assets' / 'mark.pdf')
    if args.update_example:
        shutil.copy2(out / 'tempus-template' / 'tempus-template.pdf', ROOT / 'tempus-template.pdf')
    print(f'Validated {len(sources)} documents with {args.engine}. Evidence: {out}')


if __name__ == '__main__':
    main()
