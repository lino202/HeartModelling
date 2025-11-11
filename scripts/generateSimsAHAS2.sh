#!/bin/bash

#numbers=(1 2 4 12 14 17)
numbers=(4)
for num in "${numbers[@]}"; do
	echo "Sample 4: AHA $num"
	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA.py \
	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample4/settings_mi_CL600_1800ms_stimAHA${num}_first3beats.json \
	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample4/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
	--S2_time      295
done

#numbers=(1 3 7 12 14 17)
numbers=(3)
for num in "${numbers[@]}"; do
	echo "Sample 5: AHA $num"
	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA.py \
	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample5/settings_mi_CL600_1800ms_stimAHA${num}_first3beats.json \
	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample5/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
	--S2_time      295
done

#numbers=(1 3 13 14 17)
numbers=(13)
for num in "${numbers[@]}"; do
	echo "Sample 6_x: AHA $num"
	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA.py \
	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample6_x/settings_mi_CL600_1800ms_stimAHA${num}_first3beats.json \
	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample6_x/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
	--S2_time      295
done

#numbers=(1 3 14 17)
numbers=(17)
for num in "${numbers[@]}"; do
	echo "Sample 7: AHA $num"
	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA.py \
	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample7/settings_mi_CL600_1800ms_stimAHA${num}_first3beats.json \
	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample7/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
	--S2_time      295
done

#numbers=(4 5 7 18)
numbers=(4)
for num in "${numbers[@]}"; do
	echo "Sample 8: AHA $num"
	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA.py \
	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample8/settings_mi_CL600_1800ms_stimAHA${num}_first3beats.json \
	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample8/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
	--S2_time      295
done

#numbers=(5 8 11 14)
numbers=(11)
for num in "${numbers[@]}"; do
	echo "Sample 9: AHA $num"
	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA.py \
	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample9/settings_mi_CL600_1800ms_stimAHA${num}_first3beats.json \
	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample9/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
	--S2_time      295
done

#numbers=(3 9 16 18)
numbers=(9)
for num in "${numbers[@]}"; do
	echo "Sample 10: AHA $num"
	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA.py \
	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample10/settings_mi_CL600_1800ms_stimAHA${num}_first3beats.json \
	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample10/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
	--S2_time      295
done

#numbers=(5 7 8 18)
numbers=(5)
for num in "${numbers[@]}"; do
	echo "Sample 11: AHA $num"
	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA.py \
	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample11/settings_mi_CL600_1800ms_stimAHA${num}_first3beats.json \
	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample11/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
	--S2_time      295
done

#numbers=(5 6 7 8 12 18)
numbers=(7)
for num in "${numbers[@]}"; do
	echo "Sample 12: AHA $num"
	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA.py \
	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample12/settings_mi_CL600_1800ms_stimAHA${num}_first3beats.json \
	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample12/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
	--S2_time      295
done
