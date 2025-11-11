echo "The Heart modelling code is under ${HEART_MODELLING_CODE}"
echo "The Data is under ${PAPER3_DATA}"



python ${HEART_MODELLING_CODE}/auxiliar/conductionSystem/projectSubendo_5.py \
--data_path           ${PAPER3_DATA}/Models/invivo/he/sample2 \
--cs_name             lva_up_lvs \
--out_name            cs_subendo_intramyo_lva_up_lvs \
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
--domainType          BiV

python ${HEART_MODELLING_CODE}/auxiliar/conductionSystem/projectSubendo_5.py \
--data_path           ${PAPER3_DATA}/Models/invivo/he/sample2 \
--cs_name             lvs \
--out_name            cs_subendo_intramyo_lvs \
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
--domainType          BiV

