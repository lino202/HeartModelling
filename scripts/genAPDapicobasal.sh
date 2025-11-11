##SAMPLE 4 -----------------------------------------------------------------
#echo "Processing SAMPLE 4"
#
## HE ---------------------------
#python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
#--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample4 \
#--outName      mesh_he \
#--infAsHealthy
#
#python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
#--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample4 \
#--insert2Laplacians
#
#python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
#--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample4 \
#--meshName      mesh_he
#
#python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
#--inPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample4/mesh_he.vtk \
#--outPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample4/mesh_he.inp \
#--isMyo       \
#--useLayers
#
#python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
#--dataPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample4 \
#--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample4/mesh_he.vtk \
#--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
#--dataPointName 60_minus60_60_minus60 \
#--writeFibersElectra
#
#
## MI --------
#python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
#--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample4 \
#--outName      mesh_mi
#
##python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
##--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample4 \
##--insert2Laplacians
#
#python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
#--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample4 \
#--meshName      mesh_mi
#
#python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
#--inPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample4/mesh_mi.vtk \
#--outPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample4/mesh_mi.inp \
#--isMyo       \
#--useLayers
#
#python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
#--dataPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample4 \
#--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample4/mesh_mi.vtk \
#--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
#--dataPointName 60_minus60_60_minus60 \
#--writeFibersElectra












#SAMPLE 5 -----------------------------------------------------------------
echo "Processing SAMPLE 5"

# HE ---------------------------
python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample5 \
--outName      mesh_he \
--infAsHealthy

python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample5 \
--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample5 \
--meshName      mesh_he

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample5/mesh_he.vtk \
--outPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample5/mesh_he.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample5 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample5/mesh_he.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra


# MI --------
python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample5 \
--outName      mesh_mi

#python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
#--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample5 \
#--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample5 \
--meshName      mesh_mi

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample5/mesh_mi.vtk \
--outPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample5/mesh_mi.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample5 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample5/mesh_mi.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra






#SAMPLE 6 -----------------------------------------------------------------
echo "Processing SAMPLE 6"

# HE ---------------------------
python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6 \
--outName      mesh_he \
--infAsHealthy

python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6 \
--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6 \
--meshName      mesh_he

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample6/mesh_he.vtk \
--outPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6/mesh_he.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample6 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample6/mesh_he.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra


# MI --------
python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6 \
--outName      mesh_mi

#python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
#--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6 \
#--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6 \
--meshName      mesh_mi

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample6/mesh_mi.vtk \
--outPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6/mesh_mi.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample6 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample6/mesh_mi.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra









#SAMPLE 7 -----------------------------------------------------------------
echo "Processing SAMPLE 7"

# HE ---------------------------
python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample7 \
--outName      mesh_he \
--infAsHealthy

python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample7 \
--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample7 \
--meshName      mesh_he

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample7/mesh_he.vtk \
--outPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample7/mesh_he.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample7 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample7/mesh_he.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra


# MI --------
python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample7 \
--outName      mesh_mi

#python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
#--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample7 \
#--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample7 \
--meshName      mesh_mi

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample7/mesh_mi.vtk \
--outPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample7/mesh_mi.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample7 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample7/mesh_mi.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra









#SAMPLE 8 -----------------------------------------------------------------
echo "Processing SAMPLE 8"

# HE ---------------------------
python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample8 \
--outName      mesh_he \
--infAsHealthy

python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample8 \
--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample8 \
--meshName      mesh_he

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /mnt/d/Paper3/Models/invivo/mi/la/sample8/mesh_he.vtk \
--outPath     /mnt/d/Paper3/Models/invivo/mi/la/sample8/mesh_he.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/mi/la/sample8 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/la/sample8/mesh_he.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra


# MI --------
python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample8 \
--outName      mesh_mi

#python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
#--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample8 \
#--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample8 \
--meshName      mesh_mi

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /mnt/d/Paper3/Models/invivo/mi/la/sample8/mesh_mi.vtk \
--outPath     /mnt/d/Paper3/Models/invivo/mi/la/sample8/mesh_mi.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/mi/la/sample8 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/la/sample8/mesh_mi.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra













#SAMPLE 9 -----------------------------------------------------------------
echo "Processing SAMPLE 9"

# HE ---------------------------
python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample9 \
--outName      mesh_he \
--infAsHealthy

python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample9 \
--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample9 \
--meshName      mesh_he

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /mnt/d/Paper3/Models/invivo/mi/la/sample9/mesh_he.vtk \
--outPath     /mnt/d/Paper3/Models/invivo/mi/la/sample9/mesh_he.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/mi/la/sample9 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/la/sample9/mesh_he.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra


# MI --------
python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample9 \
--outName      mesh_mi

#python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
#--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample9 \
#--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample9 \
--meshName      mesh_mi

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /mnt/d/Paper3/Models/invivo/mi/la/sample9/mesh_mi.vtk \
--outPath     /mnt/d/Paper3/Models/invivo/mi/la/sample9/mesh_mi.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/mi/la/sample9 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/la/sample9/mesh_mi.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra












#SAMPLE 10 -----------------------------------------------------------------
echo "Processing SAMPLE 10"

# HE ---------------------------
python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample10 \
--outName      mesh_he \
--infAsHealthy

python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample10 \
--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample10 \
--meshName      mesh_he

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /mnt/d/Paper3/Models/invivo/mi/la/sample10/mesh_he.vtk \
--outPath     /mnt/d/Paper3/Models/invivo/mi/la/sample10/mesh_he.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/mi/la/sample10 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/la/sample10/mesh_he.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra


# MI --------
python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample10 \
--outName      mesh_mi

#python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
#--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample10 \
#--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample10 \
--meshName      mesh_mi

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /mnt/d/Paper3/Models/invivo/mi/la/sample10/mesh_mi.vtk \
--outPath     /mnt/d/Paper3/Models/invivo/mi/la/sample10/mesh_mi.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/mi/la/sample10 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/la/sample10/mesh_mi.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra










#SAMPLE 11 -----------------------------------------------------------------
echo "Processing SAMPLE 11"

# HE ---------------------------
python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample11 \
--outName      mesh_he \
--infAsHealthy

python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample11 \
--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample11 \
--meshName      mesh_he

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /mnt/d/Paper3/Models/invivo/mi/la/sample11/mesh_he.vtk \
--outPath     /mnt/d/Paper3/Models/invivo/mi/la/sample11/mesh_he.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/mi/la/sample11 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/la/sample11/mesh_he.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra


# MI --------
python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample11 \
--outName      mesh_mi

#python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
#--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample11 \
#--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample11 \
--meshName      mesh_mi

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /mnt/d/Paper3/Models/invivo/mi/la/sample11/mesh_mi.vtk \
--outPath     /mnt/d/Paper3/Models/invivo/mi/la/sample11/mesh_mi.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/mi/la/sample11 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/la/sample11/mesh_mi.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra
















#SAMPLE 12 -----------------------------------------------------------------
echo "Processing SAMPLE 12"

# HE ---------------------------
python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample12 \
--outName      mesh_he \
--infAsHealthy

python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample12 \
--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample12 \
--meshName      mesh_he

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /mnt/d/Paper3/Models/invivo/mi/la/sample12/mesh_he.vtk \
--outPath     /mnt/d/Paper3/Models/invivo/mi/la/sample12/mesh_he.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/mi/la/sample12 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/la/sample12/mesh_he.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra


# MI --------
python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample12 \
--outName      mesh_mi

#python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
#--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample12 \
#--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/la/sample12 \
--meshName      mesh_mi

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /mnt/d/Paper3/Models/invivo/mi/la/sample12/mesh_mi.vtk \
--outPath     /mnt/d/Paper3/Models/invivo/mi/la/sample12/mesh_mi.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/mi/la/sample12 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/la/sample12/mesh_mi.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra