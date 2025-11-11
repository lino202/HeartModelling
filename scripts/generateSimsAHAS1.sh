#!/bin/bash

#numbers=(2 4 12 14 17)
#for num in "${numbers[@]}"; do
#	echo "Sample 4: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS1AHAFromTemplate.py \
#	--templatePath     /mnt/d/Paper4/Simulations/invivo/mi_EHT1/sample4/settings_mi_CL600_1800ms_stimAHA1_first3beats.json \
#	--stimAHA          ${num}
#	
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS1AHAFromTemplate.py \
#	--templatePath     /mnt/d/Paper4/Simulations/invivo/mi_EHT2/sample4/settings_mi_CL600_1800ms_stimAHA1_first3beats.json \
#	--stimAHA          ${num}
#done

#numbers=(3 7 12 14 17)
#for num in "${numbers[@]}"; do
#	echo "Sample 5: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS1AHAFromTemplate.py \
#	--templatePath     /mnt/d/Paper4/Simulations/invivo/mi_EHT1/sample5/settings_mi_CL600_1800ms_stimAHA1_first3beats.json \
#	--stimAHA          ${num}
#	
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS1AHAFromTemplate.py \
#	--templatePath     /mnt/d/Paper4/Simulations/invivo/mi_EHT2/sample5/settings_mi_CL600_1800ms_stimAHA1_first3beats.json \
#	--stimAHA          ${num}
#done
#
numbers=(3 13 14 17)
for num in "${numbers[@]}"; do
	echo "Sample 6_x: AHA $num"
	#python /mnt/d/Code/HeartModelling/generateSimFiles/genS1AHAFromTemplate.py \
	#--templatePath     /mnt/d/Paper4/Simulations/invivo/mi_EHT1/sample6_x/settings_mi_CL600_1800ms_stimAHA1_first3beats.json \
	#--stimAHA          ${num}
	
	python /mnt/d/Code/HeartModelling/generateSimFiles/genS1AHAFromTemplate.py \
	--templatePath     /mnt/e/Paper4/Simulations/invivo/mi_nocs/sample6_x/settings_mi_CL600_1800ms_stimAHA1_first3beats.json \
	--stimAHA          ${num}

done

numbers=(3 14 17)
for num in "${numbers[@]}"; do
	echo "Sample 7: AHA $num"
	#python /mnt/d/Code/HeartModelling/generateSimFiles/genS1AHAFromTemplate.py \
	#--templatePath     /mnt/d/Paper4/Simulations/invivo/mi_EHT1/sample7/settings_mi_CL600_1800ms_stimAHA1_first3beats.json \
	#--stimAHA          ${num}
	
	python /mnt/d/Code/HeartModelling/generateSimFiles/genS1AHAFromTemplate.py \
	--templatePath     /mnt/e/Paper4/Simulations/invivo/mi_nocs/sample7/settings_mi_CL600_1800ms_stimAHA1_first3beats.json \
	--stimAHA          ${num}

done

#numbers=(5 7 18)
#for num in "${numbers[@]}"; do
#	echo "Sample 8: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS1AHAFromTemplate.py \
#	--templatePath     /mnt/d/Paper4/Simulations/invivo/mi_EHT1/sample8/settings_mi_CL600_1800ms_stimAHA4_first3beats.json \
#	--stimAHA          ${num}
#	
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS1AHAFromTemplate.py \
#	--templatePath     /mnt/d/Paper4/Simulations/invivo/mi_EHT2/sample8/settings_mi_CL600_1800ms_stimAHA4_first3beats.json \
#	--stimAHA          ${num}
#done
#
#numbers=(8 11 14)
#for num in "${numbers[@]}"; do
#	echo "Sample 9: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS1AHAFromTemplate.py \
#	--templatePath     /mnt/d/Paper4/Simulations/invivo/mi_EHT1/sample9/settings_mi_CL600_1800ms_stimAHA5_first3beats.json \
#	--stimAHA          ${num}
#	
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS1AHAFromTemplate.py \
#	--templatePath     /mnt/d/Paper4/Simulations/invivo/mi_EHT2/sample9/settings_mi_CL600_1800ms_stimAHA5_first3beats.json \
#	--stimAHA          ${num}
#
#done
#
#numbers=(9 16 18)
#for num in "${numbers[@]}"; do
#	echo "Sample 10: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS1AHAFromTemplate.py \
#	--templatePath     /mnt/d/Paper4/Simulations/invivo/mi_EHT1/sample10/settings_mi_CL600_1800ms_stimAHA3_first3beats.json \
#	--stimAHA          ${num}
#	
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS1AHAFromTemplate.py \
#	--templatePath     /mnt/d/Paper4/Simulations/invivo/mi_EHT2/sample10/settings_mi_CL600_1800ms_stimAHA3_first3beats.json \
#	--stimAHA          ${num}
#
#done

numbers=(7 8 18)
for num in "${numbers[@]}"; do
	echo "Sample 11: AHA $num"
	#python /mnt/d/Code/HeartModelling/generateSimFiles/genS1AHAFromTemplate.py \
	#--templatePath     /mnt/d/Paper4/Simulations/invivo/mi_EHT1/sample11/settings_mi_CL600_1800ms_stimAHA5_first3beats.json \
	#--stimAHA          ${num}
	
	python /mnt/d/Code/HeartModelling/generateSimFiles/genS1AHAFromTemplate.py \
	--templatePath     /mnt/e/Paper4/Simulations/invivo/mi_nocs/sample11/settings_mi_CL600_1800ms_stimAHA5_first3beats.json \
	--stimAHA          ${num}

done

numbers=(6 7 8 12 18)
for num in "${numbers[@]}"; do
	echo "Sample 12: AHA $num"
	#python /mnt/d/Code/HeartModelling/generateSimFiles/genS1AHAFromTemplate.py \
	#--templatePath     /mnt/d/Paper4/Simulations/invivo/mi_EHT1/sample12/settings_mi_CL600_1800ms_stimAHA5_first3beats.json \
	#--stimAHA          ${num}
	
	python /mnt/d/Code/HeartModelling/generateSimFiles/genS1AHAFromTemplate.py \
	--templatePath     /mnt/e/Paper4/Simulations/invivo/mi_nocs/sample12/settings_mi_CL600_1800ms_stimAHA5_first3beats.json \
	--stimAHA          ${num}

done
