from pymarc import MARCReader

STUBFN="marcds/data/malpas.dat"

def search(query, limit=1000):
    marcs=[]
    with open(STUBFN, "rb") as f:
        reader = MARCReader(f, to_unicode=True, force_utf8=True)
        for m in reader:
            marcs.append(m)
    return marcs
