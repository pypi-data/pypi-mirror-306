#! /usr/bin/env python3

import sys
import importlib

if __package__ is None:
    from os import path
    upper_path = path.dirname( path.abspath(__file__) )
    package_name = path.basename(upper_path)
    sys.path.append( path.dirname(upper_path) )
    salusts = importlib.import_module(package_name)
else:
    # Dynamically import the current package
    salusts = importlib.import_module(__package__)

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    print(f"Args:{args}")
    print(f'FOVStep:[{salusts.FOVStepX},{salusts.FOVStepY}], FOVResolution:{salusts.FOVResolution:e} mm/px = {int(280000 * salusts.FOVResolution)}/280 um/px')
    edges = salusts.ChipZoneEdges()
    print("Chip Zone Edges:")
    for zone_id, coordinates in edges.items():
        print(f"{zone_id}: {coordinates}")
    return None

if __name__ == "__main__":
    sys.exit(main())
