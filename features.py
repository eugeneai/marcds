from importer import djvu


class FGen(object):
    """Class generating features list.
    """

    def __init__(self, path):
        super(FGen, self).__init__()
        self.context = djvu.Context()
        self.document = self.context.document(path)

    def metadata(self, sexprs):
        for elem in self.context.by_sexpr(sexprs=["page"],
                                          document=self.document):
            yield ("ISBN", "5-477-00208-5", 32)
            break
