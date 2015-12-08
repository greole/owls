#!/bin/sh

ln -s $FOAM_TUTORIALS/heatTransfer/buoyantSimpleFoam/buoyantCavity buoyantCavity
exec buoyantCavity/Allrun
