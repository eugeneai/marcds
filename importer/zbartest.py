#!/usr/bin/env python
import subprocess as sp

ZBAR = "/usr/bin/zbarimg"

def zbar(image):
    cmd = [ZBAR, image]
    o = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    if len(o.stderr)>0:
        # raise RuntimeError("ERROR:\n{}".format(o.stderr))
        print(o.stderr)
    type_,value = o.stdout.rstrip().decode("utf-8").split(":", maxsplit=1)
    return type_,value
    

if __name__=="__main__":
    import sys
    fn = sys.argv[1]
    print(zbar(fn)[1])
    print("Ok")
