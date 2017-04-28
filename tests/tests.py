from nose.plugins.skip import SkipTest
from nose.tools import nottest
# from .test_fos_apps import OUTDIR, INDIR
import os.path
from importer import djvu
from glob import glob

INDIR = __file__

INDIR = os.path.join(os.path.split(INDIR)[0], "../../ISDCT")
INDIR = os.path.abspath(INDIR)

INFILES = glob(os.path.join(INDIR, "*.djvu"))
INFILES.sort()
# print(INFILES)


class TestDJVU:

    def setUp(self):
        pass

#    @nottest
    def test_render(self):
        context = djvu.Context()
        print(INFILES[0])
        pages = 10
        for i, item in enumerate(context.process(INFILES[0])):
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
