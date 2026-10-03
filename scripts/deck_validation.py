"""Beamer release fixtures: standard APIs, page geometry, overlays and fonts."""
import json
import re

from pypdf import PdfReader
from pypdf.generic import ContentStream


def deck_sources(root, out):
    sources = [root / 'tempus-deck.tex', root / 'tempus-deck-starter.tex',
               *sorted((root / 'examples' / 'decks').glob('*.tex'))]
    generated = out / 'sources'
    generated.mkdir(exist_ok=True)
    variants = json.loads((root / 'examples' / 'decks' / 'variants.json').read_text())
    for name, config in variants.items():
        source = (root / config['source']).read_text()
        source, count = re.subn(r'\\documentclass\[[^]]*\]\{beamer\}',
                               lambda _: r'\documentclass[' + config['options'] + ']{beamer}',
                               source, count=1)
        assert count == 1, f'no standard Beamer class declaration in {name}'
        path = generated / (name + '.tex')
        path.write_text(source)
        sources.append(path)
    return sources


def theme_warnings(log):
    messages = re.findall(r'^Package beamerthemeTempus Warning: (.*?)\.\n\n', log, re.M | re.S)
    return [' '.join(re.sub(r'\(beamerthemeTempus\)', '', message).split()).rstrip('.')
            for message in messages]


def on_page_text(page):
    """Exclude Beamer's off-page hidden overlay text from extraction.

    PDF text extraction alone includes covered material translated outside the
    media box. Transform text origins by both PDF matrices before testing it.
    This fixture check is not a general PDF visibility/accessibility analysis.
    """
    pieces = []
    def visit(text, cm, tm, font, size):
        x = tm[4] * cm[0] + tm[5] * cm[2] + cm[4]
        y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
        if 0 <= x <= float(page.mediabox.width) and 0 <= y <= float(page.mediabox.height):
            pieces.append(text)
    page.extract_text(visitor_text=visit)
    return ''.join(pieces)


def check_deck(source, work, pages, evidence):
    name = source.stem
    assert evidence['author'], 'missing PDF author metadata'
    text = source.read_text()
    handout = bool(re.search(r'\\documentclass\[[^]]*\bhandout\b', text))
    four_three = 'aspectratio=43' in text
    reader = PdfReader(work / (name + '.pdf'))
    for page in reader.pages:
        ratio = float(page.mediabox.width / page.mediabox.height)
        assert abs(ratio - (4 / 3 if four_three else 16 / 9)) < .001, 'theme changed aspect ratio'
    nav = (work / (name + '.nav')).read_text()
    frames = int(re.search(r'\\inserttotalframenumber\s*\{(\d+)\}', nav)[1])
    expected_frames = len(re.findall(r'\\begin\{frame\}', text))
    assert frames == expected_frames, 'unexpected automatic or missing frame'
    expected_pages = frames
    if name in ('tempus-deck', 'deck-43'):
        expected_pages += 2
    if name == 'deck-overlays':
        expected_pages = 3
    assert len(pages) == expected_pages, f'overlay/handout pages: {len(pages)} != {expected_pages}'
    if 'deck-overlays' in name:
        pages = [on_page_text(page) for page in reader.pages]
        assert 'FIRSTOVERLAY' in pages[0], 'first overlay is absent'
        if handout:
            assert all(word in pages[0] for word in ('SECONDOVERLAY', 'THIRDOVERLAY', 'IMPORTANTOVERLAY')), 'handout lost overlay content'
        else:
            assert 'SECONDOVERLAY' not in pages[0] and 'THIRDOVERLAY' not in pages[1], 'overlays revealed too early'
            assert 'SECONDOVERLAY' in pages[1] and 'THIRDOVERLAY' in pages[2], 'overlay content missing'
            assert 'IMPORTANTOVERLAY' not in pages[0] and 'IMPORTANTOVERLAY' in pages[1], 'important block ignores overlay specification'
    if name in ('tempus-deck', 'deck-43', 'deck-handout', 'deck-43-handout'):
        combined = ' '.join(pages)
        for required in ('References', 'Vaswani', '87', 'accept_candidate', 'Week 4', 'research@example.org'):
            assert required in combined, f'missing deck content {required}'
        assert evidence['external_links'] >= 2 and evidence['internal_links'] >= 3, 'missing citation/contact/navigation links'
    # The footer is suppressed by standard plain frames. Non-plain frames
    # deliberately have a short title, with no auto-shrinking template.
    if name in ('tempus-deck', 'deck-43', 'deck-handout', 'deck-43-handout'):
        assert 'From pilot to practice' not in pages[-1], 'closing frame has footer'
    fonts = set()
    for page in reader.pages:
        for font in page['/Resources'].get('/Font', {}).values():
            fonts.add(str(font.get_object().get('/BaseFont', '')))
    evidence.update(aspect_ratio='4:3' if four_three else '16:9',
                    handout=handout, frames=frames, fonts=sorted(fonts))
    assert any('Libertine' in font or 'LinLibertine' in font for font in fonts), 'missing Libertine body font'
    assert any(any(family in font for family in ('Heros', 'Helvetica', 'NimbusSans', 'NimbusSanL')) for font in fonts), 'missing Helvetica-compatible headings'
    if r'\usetheme[listings]' in text:
        assert any('LMMono' in font for font in fonts), 'missing Latin Modern code font'
        sizes = []
        def code_size(text, cm, tm, font, size):
            if text.strip() and font and 'LMMono' in str(font.get('/BaseFont', '')):
                sizes.append(size)
        for page in reader.pages:
            page.extract_text(visitor_text=code_size)
        # PDF units are bp: 8 TeX pt is approximately 7.97 bp.
        assert sizes and min(sizes) >= 7.95, 'code text is smaller than 8 TeX pt'
        evidence['minimum_code_size_bp'] = min(sizes)
    if name == 'deck-palette':
        fills = [tuple(float(x) for x in args) for page in reader.pages
                 for args, operator in ContentStream(page.get_contents(), reader).operations
                 if operator == b'rg']
        teal = (39/255, 102/255, 94/255)
        navy = (30/255, 58/255, 95/255)
        close = lambda a, b: all(abs(x-y) < .002 for x, y in zip(a,b))
        assert any(close(color, teal) for color in fills), 'palette override not rendered'
        assert not any(close(color, navy) for color in fills), 'theme froze the original navy color'
