from nose.plugins.skip import SkipTest
from nose.tools import nottest
# from .test_fos_apps import OUTDIR, INDIR
import os.path
from importer import djvu
from utils import INFILES, INDIR


class TestDJVU:

    def setUp(self):
        self.context = djvu.Context()
        self.path = INFILES[0]

    @nottest
    def test_render(self):
        pages = 2
        for i, item in enumerate(self.context.process(self.path)):
            symb, val = item
            if val is not None:
                print(val, end=" ")
            elif symb == "page":
                print("\n" + "=" * 40)
            else:
                print()
            if symb == "page":
                pages -= 1
                if pages == 0:
                    break

                # ISBN checksum recognition
                # view-source:http://www.hahnlibrary.net/libraries/isbncalc.html
    @nottest
    def test_inttree(self):
        elems = 4
        for elem in self.context.by_sexpr(self.path, set(["page"])):
            _, text = elem
            print(text)
            elems -= 1
            if elems == 0:
                break
