"""Guard against false passes in release evidence checks."""
import tempfile
from pathlib import Path
import unittest

from pypdf import PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, NumberObject, TextStringObject, DecodedStreamObject

from deck_validation import deck_sources, on_page_text, theme_warnings
from validate import ROOT, check_behavior, class_warnings, inspect_pdf, rendered_equal


class EvidenceChecks(unittest.TestCase):
    def make_pdf(self, path, title='Fixture', destination=None, width=72):
        writer = PdfWriter()
        writer.add_blank_page(width=width, height=72)
        writer.add_metadata({'/Title': title, '/Author': 'Fixture Author'})
        if destination is not None:
            annotation = DictionaryObject({
                NameObject('/Type'): NameObject('/Annot'),
                NameObject('/Subtype'): NameObject('/Link'),
                NameObject('/Rect'): ArrayObject([NumberObject(0)] * 4),
                NameObject('/A'): DictionaryObject({
                    NameObject('/S'): NameObject('/GoTo'),
                    NameObject('/D'): destination,
                }),
            })
            writer.add_annotation(0, annotation)
        writer.write(path)

    def test_wrapped_and_duplicate_class_warnings_are_preserved(self):
        warning = "Class tempusreport Warning: Missing artwork\n(tempusreport)                'absent.pdf'.\n\n"
        self.assertEqual(class_warnings(warning * 2),
                         ["Missing artwork 'absent.pdf'"] * 2)

    def test_unknown_named_link_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad-link.pdf'
            self.make_pdf(path, destination=TextStringObject('absent-destination'))
            with self.assertRaisesRegex(AssertionError, 'unresolved destination'):
                inspect_pdf(path)

    def test_out_of_range_page_link_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad-page.pdf'
            self.make_pdf(path, destination=ArrayObject([NumberObject(99), NameObject('/Fit')]))
            with self.assertRaisesRegex(AssertionError, 'invalid page destination'):
                inspect_pdf(path)

    def test_metadata_is_ignored_but_page_geometry_drift_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            old, new = work / 'old.pdf', work / 'new.pdf'
            self.make_pdf(old, title='Old metadata')
            self.make_pdf(new, title='New metadata')
            rendered_equal(old, new, work)
            self.make_pdf(new, width=80)
            with self.assertRaisesRegex(AssertionError, 'size drift'):
                rendered_equal(old, new, work)


class DeckEvidenceChecks(unittest.TestCase):
    def test_variants_preserve_canonical_content(self):
        import re
        with tempfile.TemporaryDirectory() as directory:
            sources = deck_sources(ROOT, Path(directory))
            canonical = (ROOT / 'tempus-deck.tex').read_text()
            strip_class = lambda text: re.sub(r'\\documentclass\[[^]]*\]\{beamer\}', '', text)
            for source in sources:
                if source.stem in ('deck-43', 'deck-handout', 'deck-43-handout'):
                    self.assertEqual(strip_class(canonical), strip_class(source.read_text()))

    def test_shared_package_is_the_only_palette_and_mark_definition(self):
        shared = (ROOT / 'tempusdesign.sty').read_text()
        self.assertIn(r'\definecolor{TempusAccent}', shared)
        self.assertIn(r'\newcommand{\reportlogomark}', shared)
        for name in ('tempusreport.cls', 'beamerthemeTempus.sty'):
            source = (ROOT / name).read_text()
            self.assertIn('{tempusdesign}', source)
            self.assertNotIn(r'\definecolor{Tempus', source)
            self.assertNotIn(r'\newcommand{\reportlogomark}', source)
        self.assertNotIn(r'\RequirePackage{listings}', shared)

    def test_off_page_overlay_text_is_excluded(self):
        writer = PdfWriter()
        page = writer.add_blank_page(width=72, height=72)
        font = DictionaryObject({NameObject('/Type'): NameObject('/Font'),
                                 NameObject('/Subtype'): NameObject('/Type1'),
                                 NameObject('/BaseFont'): NameObject('/Helvetica')})
        page[NameObject('/Resources')] = DictionaryObject({
            NameObject('/Font'): DictionaryObject({NameObject('/F1'): writer._add_object(font)})})
        stream = DecodedStreamObject()
        stream.set_data(b'BT /F1 10 Tf 10 40 Td (VISIBLE) Tj ET '
                        b'q 1 0 0 1 2000 2000 cm BT /F1 10 Tf 10 40 Td (HIDDEN) Tj ET Q')
        page[NameObject('/Contents')] = writer._add_object(stream)
        self.assertIn('HIDDEN', page.extract_text())
        self.assertIn('VISIBLE', on_page_text(page))
        self.assertNotIn('HIDDEN', on_page_text(page))

    def test_theme_warning_multiplicity_is_preserved(self):
        warning = "Package beamerthemeTempus Warning: Missing artwork 'absent'.\n\n"
        self.assertEqual(theme_warnings(warning * 2), ["Missing artwork 'absent'"] * 2)
        wrapped = "Package beamerthemeTempus Warning: Missing artwork\n(beamerthemeTempus) 'absent'.\n\n"
        self.assertEqual(theme_warnings(wrapped), ["Missing artwork 'absent'"])


class ContinuationChecks(unittest.TestCase):
    spaced = ('Listing 1. Continued Algorithm 1. Continued '
              'Continuing box (continued) 3 checkpoint003 = 3 2 x ← x + 1')
    joined = ('Listing1.Continued Algorithm1.Continued '
              'Continuing box (continued) 3checkpoint003 = 3 2x←x+1')

    def check_text(self, text, entries=2):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            labels = {'lst:original': '1', 'alg:original': '1',
                      'lst:next': '2', 'alg:next': '2'}
            (work / 'continuations.aux').write_text(''.join(
                r'\newlabel{' + key + '}{{' + value + '}{1}}\n'
                for key, value in labels.items()))
            for extension in ('lol', 'loa'):
                (work / ('continuations.' + extension)).write_text(
                    r'\contentsline' * entries)
            check_behavior('continuations', work, [text], {'author': 'Fixture Author'})

    def test_spaced_and_joined_pdf_text_are_accepted(self):
        for text in (self.spaced, self.joined):
            with self.subTest(text=text):
                self.check_text(text)

    def test_wrong_caption_number_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'algorithm continuation heading'):
            self.check_text(self.joined.replace('Algorithm1.', 'Algorithm2.'))

    def test_wrong_listing_line_number_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'listing numbers did not continue'):
            self.check_text(self.joined.replace('3checkpoint003', '13checkpoint003'))

    def test_wrong_algorithm_line_number_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'algorithm numbers did not continue'):
            self.check_text(self.joined.replace('2x←', '12x←'))

    def test_duplicate_index_entry_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'duplicate continuation index'):
            self.check_text(self.joined, entries=3)


if __name__ == '__main__':
    unittest.main()
