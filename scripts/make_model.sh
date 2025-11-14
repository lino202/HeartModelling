# This script shows how scripts are sequentially called to generate cardiac models from MRI data.

# This info assumes you have thorughly read our article:
# https://doi.org/10.1101/2025.10.31.685788

# A folder must be set with the subfolders:
#   init: with all segmentations and labels obtained from Slicer3D
#   mesh: with the surface mesh which is usually called surfMesh.obj
#   layers: here the laplacians for the APD heterogeneity will be saved
#   RBM_LDRB: here the fiber field and related files will be saved
#   stim: here a subfolder cs will be created to save the conduction system files

# Moreover, before running this bash script, the following scripts should be run:
#   ge_s1_getGEGeometry.py (optional): only if you have an infarction, it must be run to apply the segmentation of the 
#   affected zone found in the LGE data to actual scar and border zone. 
#   s3_genTetraMeshSurface.mat: to create the initial tetrahedral mesh from the surface mesh. Please adjust the path in the script.
#   getShellandXDMF.py (optional): to create the XDMF files for visualization in Paraview and a surface mesh. This surface mesh can be
#   cut in the base to generate epi, lv_endo and rv_endo surface meshes. Note that meshes are saved in .vtu from Paraview, the script fromVtu2Obj.py 
#   can be used to pass these to .obj, which serves for reading in Meshlab and adjustment of the normals coherently.

# Once you have the /path/to/folder/mesh/tetmesh.vtk
                #   /path/to/folder/mesh/surfMesh.obj 
                #   /path/to/folder/init/lv_endo.obj
                #   /path/to/folder/init/rv_endo.obj
                #   /path/to/folder/init/epi.obj
                #   /path/to/folder/mesh/mi_pointcloud.vtk (optional, only if infarction)
# you can run this script to generate the model with fibers, APD heterogeneity and conduction system.

echo "MAKING MODEL --------------------------------------------------------------------------"
python /mnt/d/Code/HeartModelling/auxiliar/rbm/ldrb_s1_getFacetFunction.py \
--dataPath   /path/to/folder \
--domainType BiV

python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/perrottiLaplaciansFast.py \
--dataPath /path/to/folder

python /mnt/d/Code/HeartModelling/s4_interpolation.py \
--dataPath1  /path/to/folder/mesh/mi_pointcloud.vtk \
--dataPath2  /path/to/folder/layers/laplacians.vtk \
--interpType rbf \
--neighbours 300 \
--nameValue  layers_mi \
--outPath    /path/to/folder/layers/laplacians.vtk


python /mnt/d/Code/HeartModelling/auxiliar/rbm/ldrb_s2_getFibers.py \
--dataPath        /path/to/folder \
--addName         60_minus60_60_minus60 \
--domainType      BiV \
--alpha_endo_lv   60 \
--alpha_epi_lv    -60 \
--alpha_endo_rv   60 \
--alpha_epi_rv    -60

python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /path/to/folder \
--outName      mesh_he \
--infAsHealthy

python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
--dataPath     /path/to/folder \
--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /path/to/folder \
--meshName      mesh_he

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /path/to/folder/mesh_he.vtk \
--outPath     /path/to/folder/mesh_he.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /path/to/folder \
--mesh3DPath    /path/to/folder/mesh_he.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra



python /mnt/d/Code/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath     /path/to/folder \
--outName      mesh_mi

python /mnt/d/Code/HeartModelling/auxiliar/transmuralComposition/apex2BaseGradient.py \
--dataPath     /path/to/folder \
--insert2Laplacians

python /mnt/d/Code/HeartModelling/s6_BaseApexDivisions.py \
--dataPath     /path/to/folder \
--meshName      mesh_mi

python /mnt/d/Code/HeartModelling/miscellaneous/mesh2inp.py \
--inPath      /path/to/folder/mesh_mi.vtk \
--outPath     /path/to/folder/mesh_mi.inp \
--isMyo       \
--useLayers

python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /path/to/folder \
--mesh3DPath    /path/to/folder/mesh_mi.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra


python /mnt/d/Code/HeartModelling/miscellaneous/segmentMIIntoAPDHeter.py \
--meshHE     /path/to/folder/mesh_he.vtk \
--meshMI     /path/to/folder/mesh_mi.vtk \
--outPath    /path/to/folder


python /mnt/d/Code/HeartModelling/s7_cleanScar.py \
--meshPath     /path/to/folder/mesh_full_segmented.vtk \
--outPath      /path/to/folder


python /mnt/d/Code/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath            /path/to/folder/ \
--mesh3DPath          /path/to/folder/mesh_mi_noscar.vtk \
--fiberMeshName       BiV_fiber_60_minus60_60_minus60 \
--dataPointName       60_minus60_60_minus60_noscar \
--writeFibersElectra


# CS --------------------------------------------------------------------------
# For the CS generation, you will need to define the anatomical landmarks using genPurkInitNodes_1.py beforehand.
# Then, the main bundle of the CS (without the Purkinje network) can be obtained with getInitBundle_2.py. Finally, the Purkinje
# network can be created with createPurkinjeBranch_3.py from the endpoints of the main bundle and all the bundles are assembled with
# getCS_4.py to create the final conduction system mesh.

# The following scripts will project the conduction system onto the myocardial mesh, refine it, adjust it for generating a post-MI
# spatial modification and clean debug branches.

echo "MAKING MODEL CS --------------------------------------------------------------------------"

python /mnt/d/Code/HeartModelling/auxiliar/conductionSystem/projectSubendo_5.py \
--data_path           /path/to/folder \
--cs_name             final \
--out_name            cs_subendo \
--endo_per            40 \
--epi_per             25 \
--subendo_window      50 \
--intramyo_window     3 \
--meanMag             5 \
--meanNor             15 \
--intramyo_percentage 75 \
--lowMemoryDivision   10 \
--projectRV           \
--domainType          BiV \
--debug_vtk
	
python /mnt/d/Code/HeartModelling/auxiliar/conductionSystem/projectSubendo_5.py \
--data_path           /path/to/folder \
--out_name            cs_subendo_intramyo \
--cs_name             final \
--endo_per            40 \
--epi_per             25 \
--subendo_window      50 \
--intramyo_window     3 \
--meanMag             5 \
--meanNor             15 \
--project_intramyo    \
--intramyo_percentage 75 \
--lowMemoryDivision   10 \
--projectRV           \
--domainType          BiV \
--debug_vtk

python /mnt/d/Code/HeartModelling/auxiliar/conductionSystem/projectMI_6.py \
--data_path                 /path/to/folder \
--cs_name                   final \
--out_name                  cs_subendo_intramyo_mi \
--endo_per                  40 \
--epi_per                   25 \
--meanMag                   5 \
--meanNor                   15 \
--intramyo_percentage       36 \
--epi_percentage            13 \
--pmjs_reduction_percentage 42

python /mnt/d/Code/HeartModelling/auxiliar/conductionSystem/refine_7.py \
--filePath           /path/to/folder/stim/cs/final \
--csName             cs_subendo_intramyo_mi \
--size               0.5

python /mnt/d/Code/HeartModelling/auxiliar/conductionSystem/clean_debug_branches.py \
--filePath           /path/to/folder/stim/cs/final \
--csName             cs_subendo.vtk

python /mnt/d/Code/HeartModelling/auxiliar/conductionSystem/clean_debug_branches.py \
--filePath           /path/to/folder/stim/cs/final \
--csName             cs_subendo_intramyo.vtk