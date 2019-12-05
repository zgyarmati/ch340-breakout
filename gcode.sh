#!/bin/sh

DRILLFILE=gerber/ch340-breakout.drl
EDGEFILE=gerber/ch340-breakout-Edge_Cuts.gbr
mkdir -p gcode
pcb2gcode --outline ${EDGEFILE} --metric --zsafe 5 --zchange 15 --zcut -1.7 --cutter-diameter 0.8 --bridges 1 --zero-start --cut-feed 200 --cut-speed 800 --cut-infeed 0.5 --zbridges -1 \
            --drill ${DRILLFILE} --zdrill -1.8 --drill-feed 200 --milldrill --onedrill --drill-speed 900  --output-dir gcode
