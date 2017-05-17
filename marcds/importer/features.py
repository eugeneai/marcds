from marcds.importer import djvu
import re
import isbnlib
from collections import namedtuple
import pyknow


class FGen(object):
    """Class generating features list.
    """

    def __init__(self, path=None, context=None, document=None):
        super(FGen, self).__init__()
        if context is not None and document is not None:
            self.context = context
            self.document = document
        else:
            self.context = djvu.Context()
            self.document = self.context.document(path)

    REGS = {
        re.compile(r"(978-)?\d-\d{3}-\d{5}-\d"): "check_ISBN",
        re.compile(r"\d{2,2}.\d{3,3}.\d{2,2}-"): "BBK",
        re.compile(r"\d{3,3}(\.\d+)?"): "UDC",
        re.compile(r"(\d{2,4})\s+[cсCС]\."): ("PAGECOUNT", 1),
        re.compile(r"[А-Я]-?\d{2,2}"): "ORDER",
        re.compile(r"^\s*$"): "EMPTYLINE",
    }

    def metadata(self, sexprs, elems=None):
        for no, elem in enumerate(self.context.by_sexpr(sexprs=["page"],
                                                        document=self.document)):
            symb, text = elem
            lines = text.split("\n")
            if elems is not None and elems == 0:
                return

            for i, line in enumerate(lines):
                _l = line.strip()
                if _l:
                    yield self.wrap("LINE", line, line, i, no)
                for _re, cons in self.REGS.items():
                    for mo in _re.finditer(line):
                        group_no = 0
                        if isinstance(cons, tuple):
                            cons, group_no = cons
                        match = mo.group(group_no)
                        if hasattr(self, cons):
                            orig_cons = cons.replace("check_", "")
                            cons = getattr(self, cons)

                        if isinstance(cons, str):
                            yield self.wrap(cons, match, line, i, no)
                        else:
                            # FIXME: Suppose cons to be callable object
                            answer = cons(match)
                            if isinstance(answer, bool):
                                if answer:
                                    yield self.wrap(cons, match, line, i, no)
                                else:
                                    continue
                            if answer is None:
                                continue
                            yield self.wrap(orig_cons, answer, line, i, no)

                    else:
                        continue

            if elems is not None:
                elems -= 1

    def wrap(self, *args):
        return args

    def check_ISBN(self, s):
        s = s.replace("-", "")
        if isbnlib.notisbn(s):
            return False
        return s


class Fact(pyknow.Fact):

    @classmethod
    def _make(cls, match, string, line, page):
        return cls(match=match, string=string, line=line, page=page)


class ISBN(Fact):
    pass


class UDC(Fact):
    pass


class BBK(Fact):
    pass


class ORDER(Fact):
    pass


class PAGECOUNT(Fact):
    pass


class LINE(Fact):
    pass


class EMPTYLINE(Fact):
    pass


class ISSUEDATAPAGE(pyknow.Fact):

    @classmethod
    def _make(cls, isbn, page):
        return cls(isbn=isbn, page=page)


class ISSUEDATALINES(pyknow.Fact):
    pass


class FKnowGen(FGen):
    """Documentation for FKnowGen

    """

    def wrap(self, name, *args):
        cls = globals()[name]
        return cls._make(*args)
