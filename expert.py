from features import *
from pyknow import *


class DataPageRecognizer(KnowledgeEngine):
    def __init__(self, book, pages=5):
        super(DataPageRecognizer, self).__init__()
        self.book = book
        self.pages = pages

    @DefFacts()
    def __init__fact_db__(self):
        gen = FKnowGen(self.book)

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
        self.declare(DATAPAGE(isbn=isbn, page=po))
        self.retract(f1)

    @Rule(BBK(page='pb' << W()),
          'f1' << ISBN(page="pi" << W(), match="isbn" << W()),
          TEST(lambda pb, pi: pb == pi),
          salience=-100)
    def rule_page(self, pb, pi, isbn, f1):
        self.declare(DATAPAGE(isbn=isbn, page=pb))
        self.retract(f1)
