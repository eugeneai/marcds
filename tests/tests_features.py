from utils import INFILES, INDIR
from features import FGen


class TestFeatureExtractor:

    def setUp(self):
        self.f = FGen(INFILES[0])

    def test_simple(self):
        for feature in self.f.metadata(set(["page"]), elems=20):
            print(feature)
