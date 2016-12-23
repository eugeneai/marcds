import requests
from lxml import etree, html
import re
import pymarc

SPACED = re.compile(r"\s+")

class BookDataRequest(object):
    def __init__(self, isbn):
        self.isbn = isbn

    def do(self):
        self.data = "Data!"
        pass

def tostring(t):
    return etree.tostring(t, pretty_print=True, encoding=str)

M={
    "Вид документа": ("650", " ","1",  "a"),
    "Шифр издания": ("082", "0","4",  "a"),
    "Автор(ы)": ("100", "1"," ",  "a"),
    "Заглавие": ("245", "1","0",  "a"),
    "Выходные данные": ("260", " "," ",  "b"),
    "Колич.характеристики": ("300", " "," ",  "a"),
    "Предметные рубрики": ("246", "1"," ",  "a"),
}

def makefield(k,v):
    if k in M:
        code, i1, i2, sf = M[k]
        f = pymarc.Field(tag = code, indicators = [i1,i2],
                     subfields = [sf, v]
                     )
        return f
    return None


class TIUBookDataRequest(BookDataRequest):
    URL = "http://217.116.51.39/cgi-bin/irbis64r_12/cgiirbis_64.exe"

    #
    #
    def do(self):
        req = requests.post(
            self.__class__.URL,
            data={
                "S21ALL": "(<.>B={}$<.>)".format(self.isbn),
                "I21DBN": "READB",  # READB
                "P21DBN": "READB",
#                "I21DBN": "IBIS",  # READB
#                "P21DBN": "IBIS",
                "LNG": "",
                "S21STN": "1",
                "S21CNR": "10",
                "S21REF": "3",
                "S21FMT": "infow_wh",
                # "S21FMT": "FULLW_print",
                # "S21FMT": "RQST_W",
                # "S21FMT": "WEB_URUB0_WN",

                # "S21FMT": "fullwebr",
                "C21COM": "S",               # E, S
                #"EXP21FMT": "TEXT"

            })
        text = req.text

        tree = html.fromstring(text)

        # tables = tree.xpath('//table[@class="advanced" and @color]')
        tables = tree.xpath('//table[@class="advanced" and @bgcolor]')
        # for t in tables:
        #     print ("-"*100)
        #     print (tostring(t))

        table = tables[0]

        marcrec = pymarc.Record(force_utf8=True)

        # field = pymarc.Field(
        #     tag = "245", indicators = ["0","1"],
        #     subfields = ["a", "The pragmatic programmer : ",
        #                  "b", "from journeyman to master /",
        #                  "c", "Andrew Hunt, David Thomas.",
        #     ]
        #)

        #marcrec.add_field(field)

        rc = table.xpath("./tr/td/b")
        for e in rc:
            l = etree.tostring(e, encoding=str, method="text")
            if ":" not in l:
                continue
            a = SPACED.split(l)
            l=" ".join(a)

            l=l.strip()

            k,v = l.split(":", maxsplit=1)
            k,v = [a.strip() for a in [k,v]]
            field = makefield(k,v)
            if field is not None:
                marcrec.add_field(field)


            print("{}: {}".format(k,v))

        # print (rc)


        # print (table)

        self.data = "Ok!!"
        #return req
        return marcrec


def test_Malpas():
    isbn = ["5020145092", "5272000781", "9785272000781",
            "5030015922", "530004823", "013196031801", "5020145092"]
    for i in isbn:
        r = TIUBookDataRequest(i)
        marc = r.do()
        print(marc)
        print(r.data)
        fn=i+".dat"
        print(marc.leader, ":", marc.leader[9])
        with open(fn, "wb") as f:
            f.write(marc.as_marc())


if __name__ == "__main__":
    test_Malpas()
    quit()
