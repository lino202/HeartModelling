clear; close all;
addpath('../matlabFunctions', '../libraries/iso2mesh-1.9.6');

dataPath = "F:/HeartModeling/Data_OM_MI/sampleP21_389/BioVAD/";
vtk_output = append(dataPath, "tetmesh.vtk");
seg_in = append(dataPath, "Segmentation_MI_BioVAD.seg.nrrd");

seg  = ReadNrrd(seg_in);
segVol = seg.pixelData;
% segVol = smoothbinvol(seg.pixelData, 10);

clear opt;
% ssize=6;
% ang=30;
% approx=0.5;
% reratio=3;
opt.radbound  =3.;  
opt.angbound  =30;
opt.distbound =100.;
opt.reratio   =3.;
maxvol = '1=0.5:2=1.0';
% maxvol = 1.0;

tic
[nodes,elems,faces]=v2m(segVol,[1 2],opt,maxvol, 'cgalmesh');
toc
% figure, plotmesh(nodes, elems, 'x>20')


%Orientation must be checked and meshreorient.m must be use 
%I think iso2mesh orientes the tet negatively in comparison with paraview
% [newelem, evol]=meshreorient(nodes(:,1:3), elems(:,1:4));

SaveTetVtk(vtk_output, nodes(:,1:3), elems(:,1:4), []);



