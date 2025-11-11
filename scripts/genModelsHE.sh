#SAMPLE 1 -----------------------------------------------------------------
echo "MAKING SAMPLE 1 --------------------------------------------------------------------------"
python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s1_getFacetFunction.py \
--dataPath   /mnt/d/Paper3/Models/invivo/he/sample1 \
--domainType    BiV \
--nProcesses    12 \
--chunksize     600 \
--maxNumPoints  600

python /mnt/d/HeartModelling/HeartModelling/auxiliar/transmuralComposition/perrottiLaplaciansFast.py \
--dataPath /mnt/d/Paper3/Models/invivo/he/sample1

python /mnt/d/HeartModelling/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath /mnt/d/Paper3/Models/invivo/he/sample1 \
--outName  mesh
--infAsHealthy

python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s2_getFibers.py \
--dataPath        /mnt/d/Paper3/Models/invivo/he/sample1 \
--addName         60_minus60_60_minus60 \
--domainType      BiV \
--alpha_endo_lv   60 \
--alpha_epi_lv    -60 \
--alpha_endo_rv   60 \
--alpha_epi_rv    -60

python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/he/sample1 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/he/sample1/mesh.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra

python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s2_getFibers.py \
--dataPath        /mnt/d/Paper3/Models/invivo/he/sample1 \
--addName         minus100_minus91_86_73 \
--domainType      BiV \
--alpha_endo_lv   -100 \
--alpha_epi_lv    -91 \
--alpha_endo_rv   86 \
--alpha_epi_rv    73

python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/he/sample1 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/he/sample1/mesh.vtk \
--fiberMeshName BiV_fiber_minus100_minus91_86_73 \
--dataPointName minus100_minus91_86_73 \
--writeFibersElectra




#SAMPLE 2 -----------------------------------------------------------------
echo "MAKING SAMPLE 2 --------------------------------------------------------------------------"
python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s1_getFacetFunction.py \
--dataPath   /mnt/d/Paper3/Models/invivo/he/sample2 \
--domainType    BiV \
--nProcesses    12 \
--chunksize     600 \
--maxNumPoints  600

python /mnt/d/HeartModelling/HeartModelling/auxiliar/transmuralComposition/perrottiLaplaciansFast.py \
--dataPath /mnt/d/Paper3/Models/invivo/he/sample2

python /mnt/d/HeartModelling/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath /mnt/d/Paper3/Models/invivo/he/sample2 \
--outName  mesh
--infAsHealthy

python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s2_getFibers.py \
--dataPath        /mnt/d/Paper3/Models/invivo/he/sample2 \
--addName         60_minus60_60_minus60 \
--domainType      BiV \
--alpha_endo_lv   60 \
--alpha_epi_lv    -60 \
--alpha_endo_rv   60 \
--alpha_epi_rv    -60

python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/he/sample2 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/he/sample2/mesh.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra

python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s2_getFibers.py \
--dataPath        /mnt/d/Paper3/Models/invivo/he/sample2 \
--addName         53_minus62_64_minus51 \
--domainType      BiV \
--alpha_endo_lv   53 \
--alpha_epi_lv    -62 \
--alpha_endo_rv   64 \
--alpha_epi_rv    -51

python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/he/sample2 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/he/sample2/mesh.vtk \
--fiberMeshName BiV_fiber_53_minus62_64_minus51 \
--dataPointName 53_minus62_64_minus51 \
--writeFibersElectra



#SAMPLE 3 -----------------------------------------------------------------
echo "MAKING SAMPLE 3 --------------------------------------------------------------------------"
python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s1_getFacetFunction.py \
--dataPath   /mnt/d/Paper3/Models/invivo/he/sample3 \
--domainType    BiV \
--nProcesses    12 \
--chunksize     600 \
--maxNumPoints  600

python /mnt/d/HeartModelling/HeartModelling/auxiliar/transmuralComposition/perrottiLaplaciansFast.py \
--dataPath /mnt/d/Paper3/Models/invivo/he/sample3

python /mnt/d/HeartModelling/HeartModelling/s5_perrottiEndoMidEpi.py \
--dataPath /mnt/d/Paper3/Models/invivo/he/sample3 \
--outName  mesh
--infAsHealthy

python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s2_getFibers.py \
--dataPath        /mnt/d/Paper3/Models/invivo/he/sample3 \
--addName         60_minus60_60_minus60 \
--domainType      BiV \
--alpha_endo_lv   60 \
--alpha_epi_lv    -60 \
--alpha_endo_rv   60 \
--alpha_epi_rv    -60

python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/he/sample3 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/he/sample3/mesh.vtk \
--fiberMeshName BiV_fiber_60_minus60_60_minus60 \
--dataPointName 60_minus60_60_minus60 \
--writeFibersElectra

python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/ldrb_s2_getFibers.py \
--dataPath        /mnt/d/Paper3/Models/invivo/he/sample3 \
--addName         90_minus14_25_minus63 \
--domainType      BiV \
--alpha_endo_lv   90 \
--alpha_epi_lv    -14 \
--alpha_endo_rv   25 \
--alpha_epi_rv    -63

python /mnt/d/HeartModelling/HeartModelling/auxiliar/rbm/addFibers2Mesh.py \
--dataPath      /mnt/d/Paper3/Models/invivo/he/sample3 \
--mesh3DPath    /mnt/d/Paper3/Models/invivo/he/sample3/mesh.vtk \
--fiberMeshName BiV_fiber_90_minus14_25_minus63 \
--dataPointName 90_minus14_25_minus63 \
--writeFibersElectra