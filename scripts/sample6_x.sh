#SAMPLE 6 X COMPLETE HE and MI meshes-----------------------------------------------------------------
echo "MAKING SAMPLE 6 X --------------------------------------------------------------------------"
#python /mnt/d/Code/HeartModelling/auxiliar/rbm/ldrb_s1_getFacetFunction.py \
#--dataPath   /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
#--domainType BiV
#
#python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/perrottiLaplaciansFast.py \
#--dataPath /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x
#
#python /mnt/d/Code/HeartModelling/s4_interpolation.py \
#--dataPath1  /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh/mi_pointcloud.vtk \
#--dataPath2  /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/layers/laplacians.vtk \
#--interpType rbf \
#--neighbours 300 \
#--nameValue  layers_mi \
#--outPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/layers/laplacians.vtk
#
#
#python /mnt/d/Code/HeartModelling/auxiliar/rbm/ldrb_s2_getFibers.py \
#--dataPath        /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
#--addName         60_minus60_60_minus60 \
#--domainType      BiV \
#--alpha_endo_lv   60 \
#--alpha_epi_lv    -60 \
#--alpha_endo_rv   60 \
#--alpha_epi_rv    -60
#
#python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
#--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
#--outName      mesh_he \
#--infAsHealthy
#
#python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
#--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
#--insert2Laplacians
#
#python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
#--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
#--meshName      mesh_he
#
#python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
#--inPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_he.vtk \
#--outPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_he.inp \
#--isMyo       \
#--useLayers
#
#python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
#--dataPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
#--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_he.vtk \
#--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
#--dataPointName 60_minus60_60_minus60 \
#--writeFibersElectra
#
#
#
#python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
#--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
#--outName      mesh_mi
#
#python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
#--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
#--insert2Laplacians
#
#python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
#--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
#--meshName      mesh_mi
#
#python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
#--inPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_mi.vtk \
#--outPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_mi.inp \
#--isMyo       \
#--useLayers
#
#python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
#--dataPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
#--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_mi.vtk \
#--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
#--dataPointName 60_minus60_60_minus60 \
#--writeFibersElectra
#
#
#python /mnt/d/Code/HeartModelling/miscellaneous/segmentMIIntoAPDHeter.py \
#--meshHE     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_he.vtk \
#--meshMI     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_mi.vtk \
#--outPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x
#
#
#python /mnt/d/Code/HeartModelling/s7_cleanScar.py \
#--meshPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_full_segmented.vtk \
#--outPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x
#
## CS --------------------------------------------------------------------------
#echo "MAKING SAMPLE 6 X CS --------------------------------------------------------------------------"
#
#python /mnt/d/Code/HeartModelling/auxiliar/conductionSystem/projectSubendo_5.py \
#--data_path           /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
#--cs_name             final \
#--out_name            cs_subendo \
#--endo_per            40 \
#--epi_per             25 \
#--subendo_window      50 \
#--intramyo_window     3 \
#--meanMag             5 \
#--meanNor             15 \
#--intramyo_percentage 75 \
#--lowMemoryDivision   10 \
#--projectRV           \
#--domainType          BiV \
#--debug_vtk
#	
#python /mnt/d/Code/HeartModelling/auxiliar/conductionSystem/projectSubendo_5.py \
#--data_path           /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
#--out_name            cs_subendo_intramyo \
#--cs_name             final \
#--endo_per            40 \
#--epi_per             25 \
#--subendo_window      50 \
#--intramyo_window     3 \
#--meanMag             5 \
#--meanNor             15 \
#--project_intramyo    \
#--intramyo_percentage 75 \
#--lowMemoryDivision   10 \
#--projectRV           \
#--domainType          BiV \
#--debug_vtk
#
#python /mnt/d/Code/HeartModelling/auxiliar/conductionSystem/projectMI_6.py \
#--data_path                 /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
#--cs_name                   final \
#--out_name                  cs_subendo_intramyo_mi \
#--endo_per                  40 \
#--epi_per                   25 \
#--meanMag                   5 \
#--meanNor                   15 \
#--intramyo_percentage       36 \
#--epi_percentage            13 \
#--pmjs_reduction_percentage 42
#
#python /mnt/d/Code/HeartModelling/auxiliar/conductionSystem/refine_7.py \
#--filePath           /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/stim/cs/final \
#--csName             cs_subendo_intramyo_mi \
#--size               0.5

python /mnt/d/Code/HeartModelling/auxiliar/conductionSystem/clean_debug_branches.py \
--filePath           /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/stim/cs/final \
--csName             cs_subendo.vtk

python /mnt/d/Code/HeartModelling/auxiliar/conductionSystem/clean_debug_branches.py \
--filePath           /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/stim/cs/final \
--csName             cs_subendo_intramyo.vtk
