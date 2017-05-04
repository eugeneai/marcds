import os
import os.path
from glob import glob

INDIR = __file__

INDIR = os.path.join(os.path.split(INDIR)[0], "../../ISDCT")
INDIR = os.path.abspath(INDIR)

INFILES = glob(os.path.join(INDIR, "*.djvu"))
INFILES.sort()
# print(INFILES)
