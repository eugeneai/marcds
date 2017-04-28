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
        for i, page in enumerate(context.process(INFILES[0])):
            print(page)
            if i > 10:
                break
