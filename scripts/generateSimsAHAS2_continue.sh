#!/bin/bash


# -------------------------------------------EHT1 ----------------------------------------------------------

#numbers=(1 4 17)
#for num in "${numbers[@]}"; do
#	echo "Sample 4: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
#	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT1_highcond/sample4/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
#	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT1_highcond/sample4/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
#	--subfolder    S2_295 \
#	--simtime      1000
#done

#numbers=(3)
#for num in "${numbers[@]}"; do
#	echo "Sample 5: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
#	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT1_highcond/sample5/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
#	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT1_highcond/sample5/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
#	--subfolder    S2_295 \
#	--simtime      1000
#done
#
#numbers=(1 3 13 14 17)
#numbers=(13)
#for num in "${numbers[@]}"; do
#	echo "Sample 6_x: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
#	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT1_highcond/sample6_x/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
#	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT1_highcond/sample6_x/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
#	--subfolder    S2_295 \
#	--simtime      1000
#done
#
##numbers=(1 3 14 17)
#numbers=(17)
#for num in "${numbers[@]}"; do
#	echo "Sample 7: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
#	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT1_highcond/sample7/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
#	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT1_highcond/sample7/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
#	--subfolder    S2_295 \
#	--simtime      1000
#done
#
##numbers=(4 7 18)
#numbers=(4)
#for num in "${numbers[@]}"; do
#	echo "Sample 8: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
#	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT1_highcond/sample8/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
#	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT1_highcond/sample8/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
#	--subfolder    S2_295 \
#	--simtime      1000
#done
#
##numbers=(8 11 14)
#numbers=(11)
#for num in "${numbers[@]}"; do
#	echo "Sample 9: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
#	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT1_highcond/sample9/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
#	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT1_highcond/sample9/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
#	--subfolder    S2_295 \
#	--simtime      1000
#done
#
##numbers=(9 18)
#numbers=(9)
#for num in "${numbers[@]}"; do
#	echo "Sample 10: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
#	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT1_highcond/sample10/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
#	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT1_highcond/sample10/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
#	--subfolder    S2_295 \
#	--simtime      1000
#done
#
##numbers=(5 7 8 18)
#numbers=(5)
#for num in "${numbers[@]}"; do
#	echo "Sample 11: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
#	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT1_highcond/sample11/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
#	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT1_highcond/sample11/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
#	--subfolder    S2_295 \
#	--simtime      1000
#done
#
#numbers=(18)
#for num in "${numbers[@]}"; do
#	echo "Sample 12: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
#	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT1_highcond/sample12/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
#	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT1_highcond/sample12/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
#	--subfolder    S2_295 \
#	--simtime      1000
#done



# -------------------------------------------EHT2 ----------------------------------------------------------

#numbers=(1 4 17)
#for num in "${numbers[@]}"; do
#	echo "Sample 4: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
#	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample4/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
#	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample4/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
#	--subfolder    S2_295 \
#	--simtime      1000
#done

#numbers=(1 3 7 14)
numbers=(3)
for num in "${numbers[@]}"; do
	echo "Sample 5: AHA $num"
	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample5/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample5/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
	--subfolder    S2_295 \
	--simtime      1000
done

#numbers=(1 3 13 14 17)
numbers=(13)
for num in "${numbers[@]}"; do
	echo "Sample 6_x: AHA $num"
	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample6_x/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample6_x/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
	--subfolder    S2_295 \
	--simtime      1000
done

#numbers=(1 3 14 17)
numbers=(17)
for num in "${numbers[@]}"; do
	echo "Sample 7: AHA $num"
	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample7/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample7/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
	--subfolder    S2_295 \
	--simtime      1000
done


#numbers=(4 5 7 18)
#for num in "${numbers[@]}"; do
#	echo "Sample 8: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
#	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample8/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
#	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample8/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
#	--subfolder    S2_295 \
#	--simtime      1000
#done
#
#numbers=(8 11 14)
numbers=(11)
for num in "${numbers[@]}"; do
	echo "Sample 9: AHA $num"
	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample9/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample9/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
	--subfolder    S2_295 \
	--simtime      1000
done

#numbers=(9 18)
numbers=(9)
for num in "${numbers[@]}"; do
	echo "Sample 10: AHA $num"
	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample10/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample10/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
	--subfolder    S2_295 \
	--simtime      1000
done

#numbers=(5 7 8 18)
numbers=(5)
for num in "${numbers[@]}"; do
	echo "Sample 11: AHA $num"
	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample11/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample11/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
	--subfolder    S2_295 \
	--simtime      1000
done
#
#numbers=(8 18)
#for num in "${numbers[@]}"; do
#	echo "Sample 12: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
#	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample12/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
#	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_EHT2_highcond/sample12/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
#	--subfolder    S2_295 \
#	--simtime      1000
#done




# ---------------------------------------------------- No CS -----------------------------------------------------------------------------


#numbers=(3)
#for num in "${numbers[@]}"; do
#	echo "Sample 6_x: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
#	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_nocs/sample6_x/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
#	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_nocs/sample6_x/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
#	--subfolder    S2_295 \
#	--simtime      1000
#done
#
#numbers=(5)
#for num in "${numbers[@]}"; do
#	echo "Sample 11: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
#	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_nocs/sample11/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
#	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_nocs/sample11/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
#	--subfolder    S2_295 \
#	--simtime      1000
#done
#
#numbers=(6 8 12)
#for num in "${numbers[@]}"; do
#	echo "Sample 12: AHA $num"
#	python /mnt/d/Code/HeartModelling/generateSimFiles/genS2AHA_continue.py \
#	--filePath     /mnt/e/Paper4/Simulations/invivo/mi_nocs/sample12/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295.json \
#	--outPath      /mnt/e/Paper4/Simulations/invivo/mi_nocs/sample12/S2_295/settings_mi_CL600_1800ms_stimAHA${num}_S2_295_continue.json \
#	--subfolder    S2_295 \
#	--simtime      1000
#done
