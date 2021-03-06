#!/usr/bin/env python3
#import pcbnew
from pcbnew import *
import shutil
import git
import argparse

## Config options
PROJECT_NAME = "ch340-breakout"
LAYERS = [Edge_Cuts, F_Cu, B_Cu, F_SilkS,B_SilkS, F_Mask, B_Mask,F_Paste]


## Getting the version, either from the release tag given at the command line
## or getting the git version
VERSION = None
RELEASE_MODE = False
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--release", help="Use this version to set the version tag on the PCB")
args = parser.parse_args()
RELEASE_MODE = args.release

if RELEASE_MODE:
    print ("Release mode, tag: ",args.release)
    VERSION = args.release
else:
    repo = git.Repo(search_parent_directories=True)
    VERSION = repo.head.object.hexsha[0:7]
#    if repo.is_dirty():
#        VERSION += '~'

print("Version: ", VERSION)

# Load board and initialize plot controller
board = LoadBoard(PROJECT_NAME + ".kicad_pcb")

# setting the version tag on the PCB itself
for drawing in board.GetDrawings():
        if isinstance(drawing,TEXTE_PCB):
            print ("Found text " , drawing.GetText())
            if (drawing.GetText().lower().startswith("$$version")):
                drawing.SetText("Version: " + VERSION);



# plotting the gerber files into the output folder
pc = PLOT_CONTROLLER(board)
po = pc.GetPlotOptions()
po.SetPlotFrameRef(False)
po.SetOutputDirectory('gerber')


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


# plotting the drill file
drlwriter = EXCELLON_WRITER( board )

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

# Creating .zip pack for the fab
shutil.make_archive(PROJECT_NAME+'-fab-'+VERSION, 'zip', 'gerber')
