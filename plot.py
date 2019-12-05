#!/usr/bin/env python3
#import pcbnew
from pcbnew import *
import shutil
import git
repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha[0:7]
if repo.is_dirty:
    sha += '~'
print("Current version",sha)

exit(0)

PROJECT_NAME = "ch340-breakout"
LAYERS = [Edge_Cuts, F_Cu, B_Cu, F_SilkS,B_SilkS, F_Mask, B_Mask]

# Load board and initialize plot controller
board = LoadBoard(PROJECT_NAME + ".kicad_pcb")
pc = PLOT_CONTROLLER(board)
po = pc.GetPlotOptions()
po.SetPlotFrameRef(False)
po.SetOutputDirectory('gerber')


pc.OpenPlotfile('ch340-breakout', PLOT_FORMAT_GERBER,'')
for l in LAYERS:
    # Set current layer
    pc.SetLayer(l)
    layername = board.GetLayerName(l)
    print("LAYER: " , layername);

    # Plot single layer to file
    pc.OpenPlotfile(layername, PLOT_FORMAT_GERBER, '')
    print("Plotting to " + pc.GetPlotFileName())
    pc.PlotLayer()
    pc.ClosePlot()



drlwriter = EXCELLON_WRITER( board )
#drlwriter.SetMapFileFormat( PLOT_FORMAT_PDF )

mirror = False
minimalHeader = False
offset = wxPoint(0,0)
mergeNPTH = True
drlwriter.SetOptions( mirror, minimalHeader, offset, mergeNPTH )

metricFmt = True
drlwriter.SetFormat( metricFmt )

genDrl = True
genMap = False
drlwriter.CreateDrillandMapFilesSet( 'gerber', genDrl, genMap );



shutil.make_archive(PROJECT_NAME+'-fab', 'zip', 'gerber')
