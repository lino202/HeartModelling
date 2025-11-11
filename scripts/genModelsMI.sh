#SAMPLE 5 -----------------------------------------------------------------
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s1_getFacetFunction.py \
#--dataPath   /mnt/d/Paper3/Models/invivo/mi/cx/sample5 \
#--domainType BiV
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/transmuralComposition/perrottiLaplaciansFast.py \
#--dataPath /mnt/d/Paper3/Models/invivo/mi/cx/sample5
#
#python /mnt/d/HeartModelling/HeartModelling/s4_interpolation.py \
#--dataPath1  /mnt/d/Paper3/Models/invivo/mi/cx/sample5/mesh/mi_pointcloud.vtk \
#--dataPath2  /mnt/d/Paper3/Models/invivo/mi/cx/sample5/layers/laplacians.vtk \
#--interpType rbf \
#--neighbours 300 \
#--nameValue  layers_mi \
#--outPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample5/layers/laplacians.vtk
#
#python /mnt/d/HeartModelling/HeartModelling/s5_perrottiEndoMidEpi.py \
#--dataPath /mnt/d/Paper3/Models/invivo/mi/cx/sample5 \
#--outName  mesh
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s2_getFibers.py \
#--dataPath        /mnt/d/Paper3/Models/invivo/mi/cx/sample5 \
#--addName         60_minus60_60_minus60 \
#--domainType      BiV \
#--alpha_endo_lv   60 \
#--alpha_epi_lv    -60 \
#--alpha_endo_rv   60 \
#--alpha_epi_rv    -60
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
#--dataPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample5 \
#--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample5/mesh.vtk \
#--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
#--dataPointName 60_minus60_60_minus60 \
#--writeFibersElectra



##SAMPLE 6 -----------------------------------------------------------------
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s1_getFacetFunction.py \
#--dataPath   /mnt/d/Paper3/Models/invivo/mi/cx/sample6 \
#--domainType BiV
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/transmuralComposition/perrottiLaplaciansFast.py \
#--dataPath /mnt/d/Paper3/Models/invivo/mi/cx/sample6
#
#python /mnt/d/HeartModelling/HeartModelling/s4_interpolation.py \
#--dataPath1  /mnt/d/Paper3/Models/invivo/mi/cx/sample6/mesh/mi_pointcloud.vtk \
#--dataPath2  /mnt/d/Paper3/Models/invivo/mi/cx/sample6/layers/laplacians.vtk \
#--interpType rbf \
#--neighbours 300 \
#--nameValue  layers_mi \
#--outPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample6/layers/laplacians.vtk
#
#python /mnt/d/HeartModelling/HeartModelling/s5_perrottiEndoMidEpi.py \
#--dataPath /mnt/d/Paper3/Models/invivo/mi/cx/sample6 \
#--outName  mesh
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s2_getFibers.py \
#--dataPath        /mnt/d/Paper3/Models/invivo/mi/cx/sample6 \
#--addName         60_minus60_60_minus60 \
#--domainType      BiV \
#--alpha_endo_lv   60 \
#--alpha_epi_lv    -60 \
#--alpha_endo_rv   60 \
#--alpha_epi_rv    -60
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
#--dataPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample6 \
#--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample6/mesh.vtk \
#--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
#--dataPointName 60_minus60_60_minus60 \
#--writeFibersElectra

#SAMPLE 7 -----------------------------------------------------------------
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s1_getFacetFunction.py \
#--dataPath   /mnt/d/Paper3/Models/invivo/mi/cx/sample7 \
#--domainType BiV
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/transmuralComposition/perrottiLaplaciansFast.py \
#--dataPath /mnt/d/Paper3/Models/invivo/mi/cx/sample7

#python /mnt/d/HeartModelling/HeartModelling/s4_interpolation.py \
#--dataPath1  /mnt/d/Paper3/Models/invivo/mi/cx/sample7/mesh/mi_pointcloud.vtk \
#--dataPath2  /mnt/d/Paper3/Models/invivo/mi/cx/sample7/layers/laplacians.vtk \
#--interpType rbf \
#--neighbours 300 \
#--nameValue  layers_mi \
#--outPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample7/layers/laplacians.vtk
#
#python /mnt/d/HeartModelling/HeartModelling/s5_perrottiEndoMidEpi.py \
#--dataPath /mnt/d/Paper3/Models/invivo/mi/cx/sample7 \
#--outName  mesh
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s2_getFibers.py \
#--dataPath        /mnt/d/Paper3/Models/invivo/mi/cx/sample7 \
#--addName         60_minus60_60_minus60 \
#--domainType      BiV \
#--alpha_endo_lv   60 \
#--alpha_epi_lv    -60 \
#--alpha_endo_rv   60 \
#--alpha_epi_rv    -60
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
#--dataPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample7 \
#--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample7/mesh.vtk \
#--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
#--dataPointName 60_minus60_60_minus60 \
#--writeFibersElectra



##SAMPLE 8 -----------------------------------------------------------------
#echo "MAKING SAMPLE 8 --------------------------------------------------------------------------"
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s1_getFacetFunction.py \
#--dataPath   /mnt/d/Paper3/Models/invivo/mi/la/sample8 \
#--domainType BiV
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/transmuralComposition/perrottiLaplaciansFast.py \
#--dataPath /mnt/d/Paper3/Models/invivo/mi/la/sample8
#
#python /mnt/d/HeartModelling/HeartModelling/s4_interpolation.py \
#--dataPath1  /mnt/d/Paper3/Models/invivo/mi/la/sample8/mesh/mi_pointcloud.vtk \
#--dataPath2  /mnt/d/Paper3/Models/invivo/mi/la/sample8/layers/laplacians.vtk \
#--interpType rbf \
#--neighbours 200 \
#--nameValue  layers_mi \
#--outPath    /mnt/d/Paper3/Models/invivo/mi/la/sample8/layers/laplacians.vtk
#
#python /mnt/d/HeartModelling/HeartModelling/s5_perrottiEndoMidEpi.py \
#--dataPath /mnt/d/Paper3/Models/invivo/mi/la/sample8 \
#--outName  mesh
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s2_getFibers.py \
#--dataPath        /mnt/d/Paper3/Models/invivo/mi/la/sample8 \
#--addName         60_minus60_60_minus60 \
#--domainType      BiV \
#--alpha_endo_lv   60 \
#--alpha_epi_lv    -60 \
#--alpha_endo_rv   60 \
#--alpha_epi_rv    -60
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
#--dataPath      /mnt/d/Paper3/Models/invivo/mi/la/sample8 \
#--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/la/sample8/mesh.vtk \
#--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
#--dataPointName 60_minus60_60_minus60 \
#--writeFibersElectra
#
#
#
#
##SAMPLE 9 -----------------------------------------------------------------
#echo "MAKING SAMPLE 9 --------------------------------------------------------------------------"
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s1_getFacetFunction.py \
#--dataPath   /mnt/d/Paper3/Models/invivo/mi/la/sample9 \
#--domainType BiV
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/transmuralComposition/perrottiLaplaciansFast.py \
#--dataPath /mnt/d/Paper3/Models/invivo/mi/la/sample9
#
#python /mnt/d/HeartModelling/HeartModelling/s4_interpolation.py \
#--dataPath1  /mnt/d/Paper3/Models/invivo/mi/la/sample9/mesh/mi_pointcloud.vtk \
#--dataPath2  /mnt/d/Paper3/Models/invivo/mi/la/sample9/layers/laplacians.vtk \
#--interpType rbf \
#--neighbours 200 \
#--nameValue  layers_mi \
#--outPath    /mnt/d/Paper3/Models/invivo/mi/la/sample9/layers/laplacians.vtk
#
#python /mnt/d/HeartModelling/HeartModelling/s5_perrottiEndoMidEpi.py \
#--dataPath /mnt/d/Paper3/Models/invivo/mi/la/sample9 \
#--outName  mesh
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s2_getFibers.py \
#--dataPath        /mnt/d/Paper3/Models/invivo/mi/la/sample9 \
#--addName         60_minus60_60_minus60 \
#--domainType      BiV \
#--alpha_endo_lv   60 \
#--alpha_epi_lv    -60 \
#--alpha_endo_rv   60 \
#--alpha_epi_rv    -60
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
#--dataPath      /mnt/d/Paper3/Models/invivo/mi/la/sample9 \
#--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/la/sample9/mesh.vtk \
#--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
#--dataPointName 60_minus60_60_minus60 \
#--writeFibersElectra



#SAMPLE 10 -----------------------------------------------------------------
#echo "MAKING SAMPLE 10 --------------------------------------------------------------------------"
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s1_getFacetFunction.py \
#--dataPath      /mnt/d/Paper3/Models/invivo/mi/la/sample10 \
#--domainType    BiV \
#--nProcesses    12 \
#--chunksize     600 \
#--maxNumPoints  600
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/transmuralComposition/perrottiLaplaciansFast.py \
#--dataPath /mnt/d/Paper3/Models/invivo/mi/la/sample10
#
#python /mnt/d/HeartModelling/HeartModelling/s4_interpolation.py \
#--dataPath1  /mnt/d/Paper3/Models/invivo/mi/la/sample10/mesh/mi_pointcloud.vtk \
#--dataPath2  /mnt/d/Paper3/Models/invivo/mi/la/sample10/layers/laplacians.vtk \
#--interpType rbf \
#--neighbours 200 \
#--nameValue  layers_mi \
#--outPath    /mnt/d/Paper3/Models/invivo/mi/la/sample10/layers/laplacians.vtk
#
#python /mnt/d/HeartModelling/HeartModelling/s5_perrottiEndoMidEpi.py \
#--dataPath /mnt/d/Paper3/Models/invivo/mi/la/sample10 \
#--outName  mesh
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s2_getFibers.py \
#--dataPath        /mnt/d/Paper3/Models/invivo/mi/la/sample10 \
#--addName         60_minus60_60_minus60 \
#--domainType      BiV \
#--alpha_endo_lv   60 \
#--alpha_epi_lv    -60 \
#--alpha_endo_rv   60 \
#--alpha_epi_rv    -60
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
#--dataPath      /mnt/d/Paper3/Models/invivo/mi/la/sample10 \
#--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/la/sample10/mesh.vtk \
#--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
#--dataPointName 60_minus60_60_minus60 \
#--writeFibersElectra
#
#
#
##SAMPLE 11 -----------------------------------------------------------------
#echo "MAKING SAMPLE 11 --------------------------------------------------------------------------"
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s1_getFacetFunction.py \
#--dataPath   /mnt/d/Paper3/Models/invivo/mi/la/sample11 \
#--domainType    BiV \
#--nProcesses    12 \
#--chunksize     600 \
#--maxNumPoints  600
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/transmuralComposition/perrottiLaplaciansFast.py \
#--dataPath /mnt/d/Paper3/Models/invivo/mi/la/sample11
#
#python /mnt/d/HeartModelling/HeartModelling/s4_interpolation.py \
#--dataPath1  /mnt/d/Paper3/Models/invivo/mi/la/sample11/mesh/mi_pointcloud.vtk \
#--dataPath2  /mnt/d/Paper3/Models/invivo/mi/la/sample11/layers/laplacians.vtk \
#--interpType rbf \
#--neighbours 200 \
#--nameValue  layers_mi \
#--outPath    /mnt/d/Paper3/Models/invivo/mi/la/sample11/layers/laplacians.vtk
#
#python /mnt/d/HeartModelling/HeartModelling/s5_perrottiEndoMidEpi.py \
#--dataPath /mnt/d/Paper3/Models/invivo/mi/la/sample11 \
#--outName  mesh
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s2_getFibers.py \
#--dataPath        /mnt/d/Paper3/Models/invivo/mi/la/sample11 \
#--addName         60_minus60_60_minus60 \
#--domainType      BiV \
#--alpha_endo_lv   60 \
#--alpha_epi_lv    -60 \
#--alpha_endo_rv   60 \
#--alpha_epi_rv    -60
#
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
#--dataPath      /mnt/d/Paper3/Models/invivo/mi/la/sample11 \
#--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/la/sample11/mesh.vtk \
#--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
#--dataPointName 60_minus60_60_minus60 \
#--writeFibersElectra
#
#
##SAMPLE 12 -----------------------------------------------------------------
#echo "MAKING SAMPLE 12 --------------------------------------------------------------------------"
#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s1_getFacetFunction.py \
#--dataPath   /mnt/d/Paper3/Models/invivo/mi/la/sample12 \
#--domainType    BiV \
#--nProcesses    12 \
#--chunksize     600 \
#--maxNumPoints  600

#python /mnt/d/HeartModelling/HeartModelling/auxiliar/transmuralComposition/perrottiLaplaciansFast.py \
#--dataPath /mnt/d/Paper3/Models/invivo/mi/la/sample12

#python /mnt/d/HeartModelling/HeartModelling/s4_interpolation.py \
#--dataPath1  /mnt/d/Paper3/Models/invivo/mi/la/sample12/mesh/mi_pointcloud.vtk \
#--dataPath2  /mnt/d/Paper3/Models/invivo/mi/la/sample12/layers/laplacians.vtk \
#--interpType rbf \
#--neighbours 200 \
#--nameValue  layers_mi \
#--outPath    /mnt/d/Paper3/Models/invivo/mi/la/sample12/layers/laplacians.vtk
#
#python /mnt/d/HeartModelling/HeartModelling/s5_perrottiEndoMidEpi.py \
#--dataPath /mnt/d/Paper3/Models/invivo/mi/la/sample12 \
#--outName  mesh

#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s2_getFibers.py \
#--dataPath        /mnt/d/Paper3/Models/invivo/mi/la/sample12 \
#--addName         60_minus60_60_minus60 \
#--domainType      BiV \
#--alpha_endo_lv   60 \
#--alpha_epi_lv    -60 \
#--alpha_endo_rv   60 \
#--alpha_epi_rv    -60

#python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
#--dataPath      /mnt/d/Paper3/Models/invivo/mi/la/sample12 \
#--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/la/sample12/mesh.vtk \
#--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
#--dataPointName 60_minus60_60_minus60 \
#--writeFibersElectra



#SAMPLE 6 X COMPLETE HE and MI meshes-----------------------------------------------------------------
#echo "MAKING SAMPLE 6 --------------------------------------------------------------------------"
python /mnt/d/Code/HeartModelling/auxiliar/rbm/ldrb_s1_getFacetFunction.py \
--dataPath   /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
--domainType BiV

python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/perrottiLaplaciansFast.py \
--dataPath /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x

python /mnt/d/Code/HeartModelling/s4_interpolation.py \
--dataPath1  /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh/mi_pointcloud.vtk \
--dataPath2  /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/layers/laplacians.vtk \
--interpType rbf \
--neighbours 300 \
--nameValue  layers_mi \
--outPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/layers/laplacians.vtk


python /mnt/d/Code/HeartModelling/auxiliar/rbm/ldrb_s2_getFibers.py \
--dataPath        /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
--addName         60_minus60_60_minus60 \
--domainType      BiV \
--alpha_endo_lv   60 \
--alpha_epi_lv    -60 \
--alpha_endo_rv   60 \
--alpha_epi_rv    -60

python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
--outName      mesh_he \
--infAsHealthy

python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
--meshName      mesh_he

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_he.vtk \
--outPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_he.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_he.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra



python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
--outName      mesh_mi

python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
--meshName      mesh_mi

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_mi.vtk \
--outPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_mi.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_mi.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra


python /mnt/d/Code/HeartModelling/miscellaneous/segmentMIIntoAPDHeter.py \
--meshHE     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_he.vtk \
--meshMI     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_mi.vtk \
--outPath    /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x


python /mnt/d/Code/HeartModelling/s7_cleanScar.py \
--meshPath     /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_full_segmented.vtk \
--outPath      /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x