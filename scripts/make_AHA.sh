code='/mnt/d/Code/HeartModelling'


#echo "Making sample 4 ----------------------------------------------------------------"
#
#python ${code}/s4_interpolation.py \
#--dataPath1           /mnt/d/Paper3/Models/invivo/mi/cx/sample4/aha_segments/pc_aha.vtk \
#--dataPath2           /mnt/d/Paper3/Models/invivo/mi/cx/sample4/mesh_full_segmented.vtk \
#--interpType          nearest \
#--neighbours          100 \
#--nameValue           AHASegs \
#--outPath             /mnt/d/Paper3/Models/invivo/mi/cx/sample4/aha_segments/mesh.vtk
#
#python ${code}/aha_segments/AHA_getPacing.py \
#--meshIn           /mnt/d/Paper3/Models/invivo/mi/cx/sample4/aha_segments/mesh.vtk \
#--outPath          /mnt/d/Paper3/Models/invivo/mi/cx/sample4/aha_segments/mesh.vtk \
#--endoLV           /mnt/d/Paper3/Models/invivo/mi/cx/sample4/mesh/lv_endo.obj \
#--endoRV           /mnt/d/Paper3/Models/invivo/mi/cx/sample4/mesh/rv_endo.obj \
#--rvPacingCite     -34.2593 -17.2348 -8.65834
#
#python ${code}/aha_segments/AHA_getNoScar.py \
#--meshNoScarVtk   /mnt/d/Paper3/Models/invivo/mi/cx/sample4/mesh_mi_noscar.vtk \
#--meshNoScarInp   /mnt/d/Paper3/Models/invivo/mi/cx/sample4/mesh_mi_noscar.inp \
#--meshAHA         /mnt/d/Paper3/Models/invivo/mi/cx/sample4/aha_segments/mesh.vtk \
#--outPath         /mnt/d/Paper3/Models/invivo/mi/cx/sample4/aha_segments
#
#python ${code}/aha_segments/AHA_getSimInVtk.py \
#--meshIn          /mnt/d/Paper3/Models/invivo/mi/cx/sample4/aha_segments/mesh_no_scar.vtk \
#--outPath         /mnt/d/Paper3/Models/invivo/mi/cx/sample4/aha_segments/mesh_no_scar.vtk
#
#
#
#echo "Making sample 5 ----------------------------------------------------------------"
#
#python ${code}/s4_interpolation.py \
#--dataPath1           /mnt/d/Paper3/Models/invivo/mi/cx/sample5/aha_segments/pc_aha.vtk \
#--dataPath2           /mnt/d/Paper3/Models/invivo/mi/cx/sample5/mesh_full_segmented.vtk \
#--interpType          nearest \
#--neighbours          100 \
#--nameValue           AHASegs \
#--outPath             /mnt/d/Paper3/Models/invivo/mi/cx/sample5/aha_segments/mesh.vtk
#
#python ${code}/aha_segments/AHA_getPacing.py \
#--meshIn           /mnt/d/Paper3/Models/invivo/mi/cx/sample5/aha_segments/mesh.vtk \
#--outPath          /mnt/d/Paper3/Models/invivo/mi/cx/sample5/aha_segments/mesh.vtk \
#--endoLV           /mnt/d/Paper3/Models/invivo/mi/cx/sample5/mesh/lv_endo.obj \
#--endoRV           /mnt/d/Paper3/Models/invivo/mi/cx/sample5/mesh/rv_endo.obj \
#--rvPacingCite     -29.9884 -25.9971 17.9299
#
#python ${code}/aha_segments/AHA_getNoScar.py \
#--meshNoScarVtk   /mnt/d/Paper3/Models/invivo/mi/cx/sample5/mesh_mi_noscar.vtk \
#--meshNoScarInp   /mnt/d/Paper3/Models/invivo/mi/cx/sample5/mesh_mi_noscar.inp \
#--meshAHA         /mnt/d/Paper3/Models/invivo/mi/cx/sample5/aha_segments/mesh.vtk \
#--outPath         /mnt/d/Paper3/Models/invivo/mi/cx/sample5/aha_segments
#
#python ${code}/aha_segments/AHA_getSimInVtk.py \
#--meshIn          /mnt/d/Paper3/Models/invivo/mi/cx/sample5/aha_segments/mesh_no_scar.vtk \
#--outPath         /mnt/d/Paper3/Models/invivo/mi/cx/sample5/aha_segments/mesh_no_scar.vtk




#echo "Making sample 6_x ----------------------------------------------------------------"
#
#python ${code}/s4_interpolation.py \
#--dataPath1           /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/aha_segments/pc_aha.vtk \
#--dataPath2           /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_full_segmented.vtk \
#--interpType          nearest \
#--neighbours          100 \
#--nameValue           AHASegs \
#--outPath             /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/aha_segments/mesh.vtk
#
#python ${code}/aha_segments/AHA_getPacing.py \
#--meshIn           /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/aha_segments/mesh.vtk \
#--outPath          /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/aha_segments/mesh.vtk \
#--endoLV           /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh/lv_endo.obj \
#--endoRV           /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh/rv_endo.obj \
#--rvPacingCite     -40.0159 -107.158 -12.3314
#
#python ${code}/aha_segments/AHA_getNoScar.py \
#--meshNoScarVtk   /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_mi_noscar.vtk \
#--meshNoScarInp   /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/mesh_mi_noscar.inp \
#--meshAHA         /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/aha_segments/mesh.vtk \
#--outPath         /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/aha_segments
#
#python ${code}/aha_segments/AHA_getSimInVtk.py \
#--meshIn          /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/aha_segments/mesh_no_scar.vtk \
#--outPath         /mnt/d/Paper3/Models/invivo/mi/cx/sample6_x/aha_segments/mesh_no_scar.vtk

echo "Making sample 7 ----------------------------------------------------------------"

python ${code}/s4_interpolation.py \
--dataPath1           /mnt/d/Paper3/Models/invivo/mi/cx/sample7/aha_segments/pc_aha.vtk \
--dataPath2           /mnt/d/Paper3/Models/invivo/mi/cx/sample7/mesh_full_segmented.vtk \
--interpType          nearest \
--neighbours          100 \
--nameValue           AHASegs \
--outPath             /mnt/d/Paper3/Models/invivo/mi/cx/sample7/aha_segments/mesh.vtk

python ${code}/aha_segments/AHA_getPacing.py \
--meshIn           /mnt/d/Paper3/Models/invivo/mi/cx/sample7/aha_segments/mesh.vtk \
--outPath          /mnt/d/Paper3/Models/invivo/mi/cx/sample7/aha_segments/mesh.vtk \
--endoLV           /mnt/d/Paper3/Models/invivo/mi/cx/sample7/mesh/lv_endo.obj \
--endoRV           /mnt/d/Paper3/Models/invivo/mi/cx/sample7/mesh/rv_endo.obj \
--rvPacingCite     -12.058 -14.0214 65.0603

python ${code}/aha_segments/AHA_getNoScar.py \
--meshNoScarVtk   /mnt/d/Paper3/Models/invivo/mi/cx/sample7/mesh_mi_noscar.vtk \
--meshNoScarInp   /mnt/d/Paper3/Models/invivo/mi/cx/sample7/mesh_mi_noscar.inp \
--meshAHA         /mnt/d/Paper3/Models/invivo/mi/cx/sample7/aha_segments/mesh.vtk \
--outPath         /mnt/d/Paper3/Models/invivo/mi/cx/sample7/aha_segments

python ${code}/aha_segments/AHA_getSimInVtk.py \
--meshIn          /mnt/d/Paper3/Models/invivo/mi/cx/sample7/aha_segments/mesh_no_scar.vtk \
--outPath         /mnt/d/Paper3/Models/invivo/mi/cx/sample7/aha_segments/mesh_no_scar.vtk



echo "Making sample 8 ----------------------------------------------------------------"

python ${code}/s4_interpolation.py \
--dataPath1           /mnt/d/Paper3/Models/invivo/mi/la/sample8/aha_segments/pc_aha.vtk \
--dataPath2           /mnt/d/Paper3/Models/invivo/mi/la/sample8/mesh_full_segmented.vtk \
--interpType          nearest \
--neighbours          100 \
--nameValue           AHASegs \
--outPath             /mnt/d/Paper3/Models/invivo/mi/la/sample8/aha_segments/mesh.vtk

python ${code}/aha_segments/AHA_getPacing.py \
--meshIn           /mnt/d/Paper3/Models/invivo/mi/la/sample8/aha_segments/mesh.vtk \
--outPath          /mnt/d/Paper3/Models/invivo/mi/la/sample8/aha_segments/mesh.vtk \
--endoLV           /mnt/d/Paper3/Models/invivo/mi/la/sample8/mesh/lv_endo.obj \
--endoRV           /mnt/d/Paper3/Models/invivo/mi/la/sample8/mesh/rv_endo.obj \
--rvPacingCite     -19.7729 -56.1413 27.6324

python ${code}/aha_segments/AHA_getNoScar.py \
--meshNoScarVtk   /mnt/d/Paper3/Models/invivo/mi/la/sample8/mesh_mi_noscar.vtk \
--meshNoScarInp   /mnt/d/Paper3/Models/invivo/mi/la/sample8/mesh_mi_noscar.inp \
--meshAHA         /mnt/d/Paper3/Models/invivo/mi/la/sample8/aha_segments/mesh.vtk \
--outPath         /mnt/d/Paper3/Models/invivo/mi/la/sample8/aha_segments

python ${code}/aha_segments/AHA_getSimInVtk.py \
--meshIn          /mnt/d/Paper3/Models/invivo/mi/la/sample8/aha_segments/mesh_no_scar.vtk \
--outPath         /mnt/d/Paper3/Models/invivo/mi/la/sample8/aha_segments/mesh_no_scar.vtk



echo "Making sample 9 ----------------------------------------------------------------"

python ${code}/s4_interpolation.py \
--dataPath1           /mnt/d/Paper3/Models/invivo/mi/la/sample9/aha_segments/pc_aha.vtk \
--dataPath2           /mnt/d/Paper3/Models/invivo/mi/la/sample9/mesh_full_segmented.vtk \
--interpType          nearest \
--neighbours          100 \
--nameValue           AHASegs \
--outPath             /mnt/d/Paper3/Models/invivo/mi/la/sample9/aha_segments/mesh.vtk

python ${code}/aha_segments/AHA_getPacing.py \
--meshIn           /mnt/d/Paper3/Models/invivo/mi/la/sample9/aha_segments/mesh.vtk \
--outPath          /mnt/d/Paper3/Models/invivo/mi/la/sample9/aha_segments/mesh.vtk \
--endoLV           /mnt/d/Paper3/Models/invivo/mi/la/sample9/mesh/lv_endo.obj \
--endoRV           /mnt/d/Paper3/Models/invivo/mi/la/sample9/mesh/rv_endo.obj \
--rvPacingCite     -29.0193 -59.1455 40.6825

python ${code}/aha_segments/AHA_getNoScar.py \
--meshNoScarVtk   /mnt/d/Paper3/Models/invivo/mi/la/sample9/mesh_mi_noscar.vtk \
--meshNoScarInp   /mnt/d/Paper3/Models/invivo/mi/la/sample9/mesh_mi_noscar.inp \
--meshAHA         /mnt/d/Paper3/Models/invivo/mi/la/sample9/aha_segments/mesh.vtk \
--outPath         /mnt/d/Paper3/Models/invivo/mi/la/sample9/aha_segments

python ${code}/aha_segments/AHA_getSimInVtk.py \
--meshIn          /mnt/d/Paper3/Models/invivo/mi/la/sample9/aha_segments/mesh_no_scar.vtk \
--outPath         /mnt/d/Paper3/Models/invivo/mi/la/sample9/aha_segments/mesh_no_scar.vtk




echo "Making sample 10 ----------------------------------------------------------------"

python ${code}/s4_interpolation.py \
--dataPath1           /mnt/d/Paper3/Models/invivo/mi/la/sample10/aha_segments/pc_aha.vtk \
--dataPath2           /mnt/d/Paper3/Models/invivo/mi/la/sample10/mesh_full_segmented.vtk \
--interpType          nearest \
--neighbours          100 \
--nameValue           AHASegs \
--outPath             /mnt/d/Paper3/Models/invivo/mi/la/sample10/aha_segments/mesh.vtk

python ${code}/aha_segments/AHA_getPacing.py \
--meshIn           /mnt/d/Paper3/Models/invivo/mi/la/sample10/aha_segments/mesh.vtk \
--outPath          /mnt/d/Paper3/Models/invivo/mi/la/sample10/aha_segments/mesh.vtk \
--endoLV           /mnt/d/Paper3/Models/invivo/mi/la/sample10/mesh/lv_endo.obj \
--endoRV           /mnt/d/Paper3/Models/invivo/mi/la/sample10/mesh/rv_endo.obj \
--rvPacingCite     -22.4013 -50.3101 47.2136

python ${code}/aha_segments/AHA_getNoScar.py \
--meshNoScarVtk   /mnt/d/Paper3/Models/invivo/mi/la/sample10/mesh_mi_noscar.vtk \
--meshNoScarInp   /mnt/d/Paper3/Models/invivo/mi/la/sample10/mesh_mi_noscar.inp \
--meshAHA         /mnt/d/Paper3/Models/invivo/mi/la/sample10/aha_segments/mesh.vtk \
--outPath         /mnt/d/Paper3/Models/invivo/mi/la/sample10/aha_segments

python ${code}/aha_segments/AHA_getSimInVtk.py \
--meshIn          /mnt/d/Paper3/Models/invivo/mi/la/sample10/aha_segments/mesh_no_scar.vtk \
--outPath         /mnt/d/Paper3/Models/invivo/mi/la/sample10/aha_segments/mesh_no_scar.vtk






echo "Making sample 11 ----------------------------------------------------------------"

python ${code}/s4_interpolation.py \
--dataPath1           /mnt/d/Paper3/Models/invivo/mi/la/sample11/aha_segments/pc_aha.vtk \
--dataPath2           /mnt/d/Paper3/Models/invivo/mi/la/sample11/mesh_full_segmented.vtk \
--interpType          nearest \
--neighbours          100 \
--nameValue           AHASegs \
--outPath             /mnt/d/Paper3/Models/invivo/mi/la/sample11/aha_segments/mesh.vtk

python ${code}/aha_segments/AHA_getPacing.py \
--meshIn           /mnt/d/Paper3/Models/invivo/mi/la/sample11/aha_segments/mesh.vtk \
--outPath          /mnt/d/Paper3/Models/invivo/mi/la/sample11/aha_segments/mesh.vtk \
--endoLV           /mnt/d/Paper3/Models/invivo/mi/la/sample11/mesh/lv_endo.obj \
--endoRV           /mnt/d/Paper3/Models/invivo/mi/la/sample11/mesh/rv_endo.obj \
--rvPacingCite     -46.1922 -54.0619 72.3802

python ${code}/aha_segments/AHA_getNoScar.py \
--meshNoScarVtk   /mnt/d/Paper3/Models/invivo/mi/la/sample11/mesh_mi_noscar.vtk \
--meshNoScarInp   /mnt/d/Paper3/Models/invivo/mi/la/sample11/mesh_mi_noscar.inp \
--meshAHA         /mnt/d/Paper3/Models/invivo/mi/la/sample11/aha_segments/mesh.vtk \
--outPath         /mnt/d/Paper3/Models/invivo/mi/la/sample11/aha_segments

python ${code}/aha_segments/AHA_getSimInVtk.py \
--meshIn          /mnt/d/Paper3/Models/invivo/mi/la/sample11/aha_segments/mesh_no_scar.vtk \
--outPath         /mnt/d/Paper3/Models/invivo/mi/la/sample11/aha_segments/mesh_no_scar.vtk




echo "Making sample 12 ----------------------------------------------------------------"

python ${code}/s4_interpolation.py \
--dataPath1           /mnt/d/Paper3/Models/invivo/mi/la/sample12/aha_segments/pc_aha.vtk \
--dataPath2           /mnt/d/Paper3/Models/invivo/mi/la/sample12/mesh_full_segmented.vtk \
--interpType          nearest \
--neighbours          100 \
--nameValue           AHASegs \
--outPath             /mnt/d/Paper3/Models/invivo/mi/la/sample12/aha_segments/mesh.vtk

python ${code}/aha_segments/AHA_getPacing.py \
--meshIn           /mnt/d/Paper3/Models/invivo/mi/la/sample12/aha_segments/mesh.vtk \
--outPath          /mnt/d/Paper3/Models/invivo/mi/la/sample12/aha_segments/mesh.vtk \
--endoLV           /mnt/d/Paper3/Models/invivo/mi/la/sample12/mesh/lv_endo.obj \
--endoRV           /mnt/d/Paper3/Models/invivo/mi/la/sample12/mesh/rv_endo.obj \
--rvPacingCite     -19.3215 -52.2102 76.5862

python ${code}/aha_segments/AHA_getNoScar.py \
--meshNoScarVtk   /mnt/d/Paper3/Models/invivo/mi/la/sample12/mesh_mi_noscar.vtk \
--meshNoScarInp   /mnt/d/Paper3/Models/invivo/mi/la/sample12/mesh_mi_noscar.inp \
--meshAHA         /mnt/d/Paper3/Models/invivo/mi/la/sample12/aha_segments/mesh.vtk \
--outPath         /mnt/d/Paper3/Models/invivo/mi/la/sample12/aha_segments

python ${code}/aha_segments/AHA_getSimInVtk.py \
--meshIn          /mnt/d/Paper3/Models/invivo/mi/la/sample12/aha_segments/mesh_no_scar.vtk \
--outPath         /mnt/d/Paper3/Models/invivo/mi/la/sample12/aha_segments/mesh_no_scar.vtk
