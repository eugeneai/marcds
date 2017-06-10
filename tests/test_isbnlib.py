# -*- coding: utf-8 -*-
from math import sqrt
# import matplotlib.pyplot as plt
import isbnlib
from isbnlib import *
from nose.plugins.skip import SkipTest
from nose.tools import nottest
from urllib import request


class TestISBNlib:
    """
    """

    def test_simple(self):
        q = "полиситемное моделирование"
        q = request.quote(q.encode("utf-8"))
        isbn = isbnlib.isbn_from_words(q)
        print("ISBN:")
        print(isbn)
        print("Metadata1:")
        print(isbnlib.meta(isbn))
        print("Metadata:")
        isbns = ["5-02-032422-1", "978-5-9221-0466-1",
                 "978-5-8114-0674-6", "978-5-8114-0672-2",
                 "9780137308392", "9780137308057"]
        for isbn in isbns:
            print("ISBN: {}, METADATA: {}".format(isbn, meta(isbn)))
