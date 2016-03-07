#!/bin/sh

cp -a $FOAM_TUTORIALS/heatTransfer/buoyantSimpleFoam/buoyantCavity buoyantCavity
exec buoyantCavity/Allrun
