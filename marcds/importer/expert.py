from marcds.importer.features import *
from pyknow import *
import re


class DataPageRecognizer(KnowledgeEngine):

    def __init__(self, filename=None, context=None, document=None, pages=5):
        super(DataPageRecognizer, self).__init__()
        self.book = filename
        self.context = context
        self.document = document
        self.pages = pages
        self.issue_data = None
        self.isbn = None

    @DefFacts()
    def __init__fact_db__(self):
        gen = FKnowGen(self.book, context=self.context, document=self.document)
        yield from gen.metadata(set(["page"]), elems=self.pages)

    @Rule(ORDER(page='po' << W()),
          BBK(page='pb' << W()),
          TEST(lambda po, pb: po == pb),
          'f1' << ISBN(page="pi" << W(), match="isbn" << W()),
          TEST(lambda pb, pi: pb == pi),
          UDC(page="pu" << W()),
          TEST(lambda pu, pi: pi == pu),
          salience=100)
    def rule_page(self, po, pb, pi, isbn, pu, f1):
        self.isbn = isbn
        self.declare(ISSUEDATAPAGE(isbn=isbn, page=po))
        self.retract(f1)

    @Rule(BBK(page='pb' << W()),
          'f1' << ISBN(page="pi" << W(), match="isbn" << W()),
          TEST(lambda pb, pi: pb == pi),
          salience=-100)
    def rule_page(self, pb, pi, isbn, f1):
        self.declare(ISSUEDATAPAGE(isbn=isbn, page=pb))
        self.retract(f1)

    @Rule(ISSUEDATAPAGE(page='pi' << W()),
          PAGECOUNT(match='m' << W(), page='pp' << W(), line='pl' << W()),
          TEST(lambda pi, pp: pi == pp),
          EMPTYLINE(page='ep1' << W(), line='l1' << W()),
          TEST(lambda pi, ep1, pl, l1: pi == ep1 and (
              pl - l1) <= 4 and (pl - l1) > 0),
          EMPTYLINE(page='ep2' << W(), line='l2' << W()),
          TEST(lambda pi, ep2, pl, l2: pi == ep2 and (
              l2 - pl) <= 2 and (l2 - pl) > 0),
          )
    def determ(self, l1, l2, pp, **kwargs):
        l1 += 1
        l2 -= 1
        self.issue_data = ISSUEDATALINES(start=l1, end=l2, page=pp)
        self.declare(self.issue_data)
        self.halt()
