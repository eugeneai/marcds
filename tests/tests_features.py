from utils import INFILES, INDIR
from marcds.importer.features import FGen
from marcds.importer.expert import DataPageRecognizer
from nose.plugins.skip import SkipTest
from marcds.importer.issuerecog import DJVUtoMARC


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


@SkipTest
class TestDataPageRecognizer:

    def setUp(self):
        self.r = DataPageRecognizer(INFILES[0])

    def test_recognition(self):
        self.r.reset()
        self.r.run()
        assert self.r.issue_date is not None
        # print(self.r.facts)


class TestDJVUtoMARC(object):
    """Documentation for TestDJVUtoMARC

    """

    def test_basic(self):
        dj = DJVUtoMARC(INFILES[0])
        assert dj.issue_data()
