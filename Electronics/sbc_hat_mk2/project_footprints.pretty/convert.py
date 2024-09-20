#!/usr/bin/python

import sys
from pcbnew import *

infile = sys.argv[1]
outdir = sys.argv[2]

inplugin = IO_MGR.PluginFind(IO_MGR.GuessPluginTypeFromLibPath(infile))
outplugin = IO_MGR.PluginFind(IO_MGR.GuessPluginTypeFromLibPath(outdir))

for name in inplugin.FootprintEnumerate(infile):
    fp = inplugin.FootprintLoad(infile, name)
    outplugin.FootprintSave(outdir, fp)
