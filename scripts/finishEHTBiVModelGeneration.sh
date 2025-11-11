#!/bin/bash

#conda activate HeartModellingFenics

# EHT1 ---------------------------------------------------------------------------------------------
samples=(8 11 12)
for sample in "${samples[@]}"; do
	echo "Sample $sample -----------------------------------------------------------------------------------------------------"
	python /mnt/d/Code/HeartModelling/heartPatch/s8_getLayersFibers.py \
	--heartPatchMesh   /mnt/d/Paper4/Models/sample${sample}/EHT1/mesh/tetmesh.vtk \
	--layersMesh       /mnt/d/Paper3/Models/invivo/mi/la/sample${sample}/mesh_full_segmented.vtk \
	--fibsMesh         /mnt/d/Paper3/Models/invivo/mi/la/sample${sample}/mesh_mi.vtk \
	--outPath          /mnt/d/Paper4/Models/sample${sample}/EHT1/mesh/tetmesh.vtk

	python /mnt/d/Code/HeartModelling/heartPatch/s9_getPatchRandFibers.py \
	--meshHeart        /mnt/d/Paper4/Models/sample${sample}/epi_refine.obj \
	--meshMIPatch      /mnt/d/Paper4/Models/sample${sample}/EHT1/mesh/tetmesh.vtk \
	--outPath          /mnt/d/Paper4/Models/sample${sample}/EHT1/mesh/tetmesh.vtk

	# now we need to clean the scar, clean the fibers of the scar and make the AHA stim nodes for this mesh
	python /mnt/d/Code/HeartModelling/s7_cleanScar.py \
	--meshPath        /mnt/d/Paper4/Models/sample${sample}/EHT1/mesh/tetmesh.vtk \
	--outPath         /mnt/d/Paper4/Models/sample${sample}/EHT1/mesh

	python /mnt/d/Code/HeartModelling/heartPatch/s11_getFibersNoScar.py \
	--meshNoScar   /mnt/d/Paper4/Models/sample${sample}/EHT1/mesh/mesh_mi_noscar.vtk \
	--meshFibers   /mnt/d/Paper4/Models/sample${sample}/EHT1/mesh/tetmesh.vtk \
	--outPath      /mnt/d/Paper4/Models/sample${sample}/EHT1/mesh

	python /mnt/d/Code/HeartModelling/heartPatch/s12_AHA_getNoScar.py \
	--meshNoScarVtk   /mnt/d/Paper4/Models/sample${sample}/EHT1/mesh/mesh_mi_noscar.vtk \
	--meshNoScarInp   /mnt/d/Paper4/Models/sample${sample}/EHT1/mesh/mesh_mi_noscar.inp \
	--meshAHA         /mnt/d/Paper3/Models/invivo/mi/la/sample${sample}/aha_segments/mesh.vtk \
	--outPath         /mnt/d/Paper4/Models/sample${sample}/EHT1/mesh/mesh_no_scar

	python /mnt/d/Code/HeartModelling/aha_segments/AHA_getSimInVtk.py \
	--meshIn          /mnt/d/Paper4/Models/sample${sample}/EHT1/mesh/mesh_no_scar.vtk \
	--outPath         /mnt/d/Paper4/Models/sample${sample}/EHT1/mesh/mesh_no_scar.vtk


	python /mnt/d/Code/HeartModelling/heartPatch/s14_addPatch2inp.py \
	--meshNoScarVtk         /mnt/d/Paper4/Models/sample${sample}/EHT1/mesh/mesh_no_scar.vtk \
	--meshNoScarInp         /mnt/d/Paper4/Models/sample${sample}/EHT1/mesh/mesh_no_scar.inp
done


# EHT2 ------------------------------------------------------------------------------------------------
samples=(8 11 12)
for sample in "${samples[@]}"; do
	echo "Sample $sample -----------------------------------------------------------------------------------------------------"
	python /mnt/d/Code/HeartModelling/heartPatch/s8_getLayersFibers.py \
	--heartPatchMesh   /mnt/d/Paper4/Models/sample${sample}/EHT2/mesh/tetmesh.vtk \
	--layersMesh       /mnt/d/Paper3/Models/invivo/mi/la/sample${sample}/mesh_full_segmented.vtk \
	--fibsMesh         /mnt/d/Paper3/Models/invivo/mi/la/sample${sample}/mesh_mi.vtk \
	--outPath          /mnt/d/Paper4/Models/sample${sample}/EHT2/mesh/tetmesh.vtk

	python /mnt/d/Code/HeartModelling/heartPatch/s9_getPatchRandFibers.py \
	--meshHeart        /mnt/d/Paper4/Models/sample${sample}/epi_refine.obj \
	--meshMIPatch      /mnt/d/Paper4/Models/sample${sample}/EHT2/mesh/tetmesh.vtk \
	--outPath          /mnt/d/Paper4/Models/sample${sample}/EHT2/mesh/tetmesh.vtk

	# now we need to clean the scar, clean the fibers of the scar and make the AHA stim nodes for this mesh
	python /mnt/d/Code/HeartModelling/s7_cleanScar.py \
	--meshPath        /mnt/d/Paper4/Models/sample${sample}/EHT2/mesh/tetmesh.vtk \
	--outPath         /mnt/d/Paper4/Models/sample${sample}/EHT2/mesh

	python /mnt/d/Code/HeartModelling/heartPatch/s11_getFibersNoScar.py \
	--meshNoScar   /mnt/d/Paper4/Models/sample${sample}/EHT2/mesh/mesh_mi_noscar.vtk \
	--meshFibers   /mnt/d/Paper4/Models/sample${sample}/EHT2/mesh/tetmesh.vtk \
	--outPath      /mnt/d/Paper4/Models/sample${sample}/EHT2/mesh

	python /mnt/d/Code/HeartModelling/heartPatch/s12_AHA_getNoScar.py \
	--meshNoScarVtk   /mnt/d/Paper4/Models/sample${sample}/EHT2/mesh/mesh_mi_noscar.vtk \
	--meshNoScarInp   /mnt/d/Paper4/Models/sample${sample}/EHT2/mesh/mesh_mi_noscar.inp \
	--meshAHA         /mnt/d/Paper3/Models/invivo/mi/la/sample${sample}/aha_segments/mesh.vtk \
	--outPath         /mnt/d/Paper4/Models/sample${sample}/EHT2/mesh/mesh_no_scar

	python /mnt/d/Code/HeartModelling/aha_segments/AHA_getSimInVtk.py \
	--meshIn          /mnt/d/Paper4/Models/sample${sample}/EHT2/mesh/mesh_no_scar.vtk \
	--outPath         /mnt/d/Paper4/Models/sample${sample}/EHT2/mesh/mesh_no_scar.vtk


	python /mnt/d/Code/HeartModelling/heartPatch/s14_addPatch2inp.py \
	--meshNoScarVtk         /mnt/d/Paper4/Models/sample${sample}/EHT2/mesh/mesh_no_scar.vtk \
	--meshNoScarInp         /mnt/d/Paper4/Models/sample${sample}/EHT2/mesh/mesh_no_scar.inp
done
