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


#@SkipTest
class TestDJVUtoMARC(object):
    """Documentation for TestDJVUtoMARC
    """

    def test_basic(self):
        dj = DJVUtoMARC(INFILES[0])
        assert dj.issue_data()
        print("ISBN:", dj.isbn)
        assert dj.isbn
        rc = dj.query_with_isbn(services=("wcat", "goob", "openl"))
        print("Queries:", rc)


class TestIssueDataRecognizer(object):

    def test_basic(self):
        from marcds.importer.exp_issue import IssueDataRecognizer
        dr = IssueDataRecognizer("Иванов И.И., Петрова А. В., Зеленая И.")

        dr.prepare()
        dr.run()
        print(dr.facts)

    def test_father(self):
        from marcds.importer.exp_issue import IssueDataRecognizer
        dr = IssueDataRecognizer(
            "Черкашин А.К. Полисистемное моделированиею -"
            " Новосибирск: Наука, 2005. - 280 с.")

        dr.prepare()
        dr.run()
        print(dr.facts)

    def test_yablonsky(self):
        from marcds.importer.exp_issue import IssueDataRecognizer
        dr = IssueDataRecognizer(
            "Введение в дискретную математику. Яблонский С. В. - М.: Нау-"
            "ка. Главная редакция физико-математической литературы, 1979.")

        dr.prepare()
        dr.run()
        print(dr.facts)
