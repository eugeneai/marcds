from utils import INFILES, INDIR
from features import FGen
from expert import DataPageRecognizer
from nose.plugins.skip import SkipTest


@SkipTest
class TestFeatureExtractor:

    def setUp(self):
        self.f = FGen(INFILES[0])

    def test_simple(self):
        facts = False
        for feature in self.f.metadata(set(["page"]), elems=20):
            print(feature)
            facts = True

        assert facts, "no facts"


class TestDataPageRecognizer:

    def setUp(self):
        self.r = DataPageRecognizer(INFILES[0])

    def test_recognition(self):
        self.r.reset()
        self.r.run()
        assert self.r.issue_date is not None
        # print(self.r.facts)
