#!/bin/bash

echo "The Heart modelling code is under ${HEART_MODELLING_CODE}"
echo "The Data is under ${PAPER3_DATA}"


#for i in 10 11 12
#do
#	echo "MAKING CS SAMPLE ${i} --------------------------------------------------------------------------"
#	
#	python ${HEART_MODELLING_CODE}/auxiliar/conductionSystem/projectSubendo_5.py \
#	--data_path           ${PAPER3_DATA}/Models/invivo/mi/la/sample${i} \
#	--cs_name             final \
#	--out_name            cs_subendo \
#	--endo_per            40 \
#	--epi_per             25 \
#	--subendo_window      50 \
#	--intramyo_window     3 \
#	--meanMag             5 \
#	--meanNor             15 \
#	--intramyo_percentage 75 \
#	--lowMemoryDivision   10 \
#	--projectRV           \
#	--domainType          BiV \
#	--debug_vtk
#	
#	python ${HEART_MODELLING_CODE}/auxiliar/conductionSystem/projectSubendo_5.py \
#	--data_path           ${PAPER3_DATA}/Models/invivo/mi/la/sample${i} \
#	--out_name            cs_subendo_intramyo \
#	--cs_name             final \
#	--endo_per            40 \
#	--epi_per             25 \
#	--subendo_window      50 \
#	--intramyo_window     3 \
#	--meanMag             5 \
#	--meanNor             15 \
#	--project_intramyo    \
#	--intramyo_percentage 75 \
#	--lowMemoryDivision   10 \
#	--projectRV           \
#	--domainType          BiV \
#	--debug_vtk
#	
#	python ${HEART_MODELLING_CODE}/auxiliar/conductionSystem/projectMI_6.py \
#	--data_path                 ${PAPER3_DATA}/Models/invivo/mi/la/sample${i} \
#	--cs_name                   final \
#	--out_name                  cs_subendo_intramyo_mi \
#	--endo_per                  40 \
#	--epi_per                   25 \
#	--meanMag                   5 \
#	--meanNor                   15 \
#	--intramyo_percentage       36 \
#	--epi_percentage            13 \
#	--pmjs_reduction_percentage 42
#	
#	python ${HEART_MODELLING_CODE}/auxiliar/conductionSystem/refine_7.py \
#	--filePath           ${PAPER3_DATA}/Models/invivo/mi/la/sample${i}/stim/cs/final \
#	--csName             cs_subendo_intramyo_mi \
#	--size               0.5
#	
#	#python ${HEART_MODELLING_CODE}/auxiliar/conductionSystem/clean_debug_branches.py \
#	#--filePath           ${PAPER3_DATA}/Models/invivo/mi/la/sample${i}/stim/cs/final \
#	#--csName             cs_subendo.vtk
#	#
#	#python ${HEART_MODELLING_CODE}/auxiliar/conductionSystem/clean_debug_branches.py \
#	#--filePath           ${PAPER3_DATA}/Models/invivo/mi/la/sample${i}/stim/cs/final \
#	#--csName             cs_subendo_intramyo.vtk
#
#done




for i in 5
do
	echo "MAKING CS SAMPLE ${i} --------------------------------------------------------------------------"
	
	python ${HEART_MODELLING_CODE}/auxiliar/conductionSystem/projectSubendo_5.py \
	--data_path           ${PAPER3_DATA}/Models/invivo/mi/cx/sample${i} \
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
	
	python ${HEART_MODELLING_CODE}/auxiliar/conductionSystem/projectSubendo_5.py \
	--data_path           ${PAPER3_DATA}/Models/invivo/mi/cx/sample${i} \
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
	
	python ${HEART_MODELLING_CODE}/auxiliar/conductionSystem/projectMI_6.py \
	--data_path                 ${PAPER3_DATA}/Models/invivo/mi/cx/sample${i} \
	--cs_name                   final \
	--out_name                  cs_subendo_intramyo_mi \
	--endo_per                  40 \
	--epi_per                   25 \
	--meanMag                   5 \
	--meanNor                   15 \
	--intramyo_percentage       36 \
	--epi_percentage            13 \
	--pmjs_reduction_percentage 42
	
	python ${HEART_MODELLING_CODE}/auxiliar/conductionSystem/refine_7.py \
	--filePath           ${PAPER3_DATA}/Models/invivo/mi/cx/sample${i}/stim/cs/final \
	--csName             cs_subendo_intramyo_mi \
	--size               0.5
	
	#python ${HEART_MODELLING_CODE}/auxiliar/conductionSystem/clean_debug_branches.py \
	#--filePath           ${PAPER3_DATA}/Models/invivo/mi/cx/sample${i}/stim/cs/final \
	#--csName             cs_subendo.vtk
	#
	#python ${HEART_MODELLING_CODE}/auxiliar/conductionSystem/clean_debug_branches.py \
	#--filePath           ${PAPER3_DATA}/Models/invivo/mi/cx/sample${i}/stim/cs/final \
	#--csName             cs_subendo_intramyo.vtk

done
