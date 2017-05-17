from expret import DataPageRecognizer


class NoIssueDataException(Exception):
    pass


class DJVUtoMARC(object):
    """Recognize issue data in a DJVU file.
    """

    def __init__(self, filename):
        self.filename = filename

    def issue_data(self, noexc=True):
        r = DataPageRecognizer(self.filename)
        r.reset()
        r.run()
        if r.issue_data is None:
            if noexc:
                return None
            else:
                raise NoIssueDataException()
