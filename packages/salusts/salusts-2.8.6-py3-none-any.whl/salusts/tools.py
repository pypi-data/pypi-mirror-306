#! /usr/bin/env python3

import sys
from os import path

if __package__ is None:
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from nfo import ChipZoneEdges
else:
    from .nfo import ChipZoneEdges

def npy2tif(npyinf, tifoutf):
    import tifffile
    import numpy as np
    mask = np.load(npyinf)
    dpi = (7112000, 69)
    tifffile.imwrite(tifoutf, mask, photometric='miniswhite',
        compression='zlib',compressionargs={'level': 9},
        predictor=True, resolution=(dpi,dpi), resolutionunit='INCH'
    )

def eprint(*args, **kwargs) -> None:
    print(*args, **kwargs, file=sys.stderr, flush=True)

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    if len(args) < 2:
        eprint(f'Usage: {sys.argv[0]} <mask.npy> <mask.tif>')
        exit(0);
    elif len(args) >= 2:
        npyinf = args[0]
        tifoutf = args[1]
        eprint(f'Convert:[{npyinf}]->[{tifoutf}]')
        npy2tif(npyinf, tifoutf)
    return None

if __name__ == "__main__":
    sys.exit(main())
