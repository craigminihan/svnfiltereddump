
from unittest import TestCase
from StringIO import StringIO
import tempfile
import os

from svnfiltereddump import Config

class ConfigTest(TestCase):

    def test_simple_args(self):
        config = Config( [ '/repo/path', 'a/b/c', 'x/y' ] )
        self.assertEqual(config.source_repository, '/repo/path')
        self.assertEqual(sorted(config.include_paths), [ 'a/b/c', 'x/y' ])
        self.assertEqual(config.exclude_paths, [ ])
        self.assertEqual(config.drop_empty_revs, False)
        self.assertEqual(config.renumber_revs, False)
        self.assertEqual(config.start_rev, None)

    def test_include_file(self):
        ( fh ) = tempfile.NamedTemporaryFile(delete=False)
        fh.write("a/x\nb/y\nc/z\n")
        fh.close()
        config = Config( [ '/repo/path', '--include-file', fh.name ] )
        self.assertEqual(config.source_repository, '/repo/path')
        self.assertEqual(sorted(config.include_paths), [ 'a/x', 'b/y', 'c/z'  ])
        self.assertEqual(config.exclude_paths, [ ])
        os.remove(fh.name)

    def test_include_file_plus(self):
        ( fh ) = tempfile.NamedTemporaryFile(delete=False)
        fh.write("a/x\nb/y\nc/z\n")
        fh.close()
        config = Config( [ '/repo/path', '--include-file', fh.name, 'x/y' ] )
        self.assertEqual(sorted(config.include_paths), [ 'a/x', 'b/y', 'c/z', 'x/y'  ])
        self.assertEqual(config.exclude_paths, [ ])
        os.remove(fh.name)

    def test_exclude(self):
        config = Config( [ '/repo/path', 'a/b/c', '--exclude', 'x/y' ] )        
        self.assertEqual(sorted(config.include_paths), [ 'a/b/c' ])
        self.assertEqual(config.exclude_paths, [ 'x/y' ])

    def test_exclude_file_plus(self):
        ( fh ) = tempfile.NamedTemporaryFile(delete=False)
        fh.write("x1\nx2\n")
        fh.close()
        config = Config( [ '/repo/path', 'a/b/c', '--exclude-file', fh.name , '--exclude', 'x/y' ] )
        self.assertEqual(config.include_paths, [ 'a/b/c' ])
        self.assertEqual(sorted(config.exclude_paths), [ 'x/y', 'x1', 'x2' ])
        os.remove(fh.name)

    def test_drop_empty_revs(self):
        config = Config( [ '/repo/path', 'a/b', '--drop-empty-revs' ] )
        self.assertEqual(config.drop_empty_revs, True)

    def test_renumber_revs(self):
        config = Config( [ '/repo/path', 'a/b', '--renumber-revs' ] )
        self.assertEqual(config.renumber_revs, True)

    def test_renumber_revs(self):
        config = Config( [ '/repo/path', 'a/b', '--start-rev', '4711' ] )
        self.assertEqual(config.start_rev, 4711)

    # We need: 'assertExits' here!!
    # def test_bad_source_repo_path(self):
    #    self.assertRaises(Exception, Config, [ 'repo/path', 'a/b' ])
