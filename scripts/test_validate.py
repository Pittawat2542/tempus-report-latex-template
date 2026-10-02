"""Guard against false passes in release evidence checks."""
import tempfile
from pathlib import Path
import unittest

from pypdf import PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, NumberObject, TextStringObject

from validate import class_warnings, inspect_pdf, rendered_equal


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


if __name__ == '__main__':
    unittest.main()
