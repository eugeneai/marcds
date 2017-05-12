from importer import djvu
import re
import isbnlib


class FGen(object):
    """Class generating features list.
    """

    def __init__(self, path):
        super(FGen, self).__init__()
        self.context = djvu.Context()
        self.document = self.context.document(path)

    REGS = {
        re.compile(r"(978-)?\d-\d{3}-\d{5}-\d"): "check_ISBN",
        re.compile(r"\d{2,2}.\d{3,3}.\d{2,2}-"): "BBK",
        re.compile(r"\d{3,3}(\.\d+)?"): "UDC",
        re.compile(r"[А-Я]-?\d{2,2}"): "ORDER",
    }

    def metadata(self, sexprs, elems=None):
        for no, elem in enumerate(self.context.by_sexpr(sexprs=["page"],
                                                        document=self.document)):
            symb, text = elem
            lines = text.split("\n")
            if elems is not None and elems == 0:
                return

            for i, line in enumerate(lines):
                for _re, cons in self.REGS.items():
                    for mo in _re.finditer(line):
                        match = mo.group(0)

                        if hasattr(self, cons):
                            orig_cons = cons.replace("check_", "")
                            cons = getattr(self, cons)

                        if isinstance(cons, str):
                            yield (cons, match, line, i, no)
                        else:
                            # FIXME: Suppose cons to be callable object
                            answer = cons(match)
                            if isinstance(answer, bool):
                                if answer:
                                    yield (cons, match, line, i, no)
                                else:
                                    continue
                            if answer is None:
                                continue
                            yield (orig_cons, answer, line, i, no)

                    else:
                        continue

            if elems is not None:
                elems -= 1

#    def

    def check_ISBN(self, s):
        s = s.replace("-", "")
        if isbnlib.notisbn(s):
            return False
        return s
