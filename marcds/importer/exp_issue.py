import pyknow
import re


class Fact(pyknow.Fact):

    @classmethod
    def _make(cls, string, pos):
        return cls(string=string, pos=pos)

    @classmethod
    def check(cls, *args, **kw):
        yield cls(*args, **kw)


class NAME(Fact):

    @classmethod
    def check(cls, string, pos):
        for c in string:
            if c.isdigit():
                return
        yield cls(string=string, pos=pos)


class PAGES(Fact):
    pass


class YEAR(Fact):
    pass


class IssueDataRecognizer(pyknow.KnowledgeEngine):
    """Recognizes issue data: Authors, year, etc.
    """

    RES = {
        re.compile(r"\w+\s+\w{1,2}\.(\s*\w{1,2}\.)?"): (NAME, 0),
        re.compile(r"\d+\s{1,3}[cCсС]\."): (PAGES, 0),
        re.compile(r"[12]\d{3}"): (YEAR, 0),
    }

    def __init__(self, text):
        """`Text` contains lines of text where take components."""
        super(IssueDataRecognizer, self).__init__()
        text = text.replace("-\n", "")
        text = text.replace("\n", "")
        self.text = text

    def _facts(self):
        for _re, v in self.__class__.RES.items():
            cls, group_no = v
            for m in _re.finditer(self.text):
                value = m.group(group_no)
                pos = m.start(group_no)
                yield from cls.check(string=value, pos=pos)

    def prepare(self):
        self.reset()
        for fact in self._facts():
            self.declare(fact)

    @pyknow.Rule('fn' << NAME())
    def print_name(_, **kw):
        print(_, kw["fn"])
