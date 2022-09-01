clear; close all;
addpath('../matlabFunctions', '../libraries/iso2mesh-1.9.6');

vtk_output = "F:\HeartModeling\NeisserModel\tetmesh.vtk";
x = 1:20;       %10 units are 1 mm so we need to divide by 10 var nodes afterwards
y = 1:100;
z = 1:65;
vol = zeros(size(x,2), size(y,2), size(z,2));
vol(:,:,1:60) = 1;
vol(:,15:85,61:65) = 2;
vol = uint8(vol);
figure(), imshow(squeeze(vol(2,:,:)), [0 2])

clear opt;
opt(1).radbound=1; % head surface element size bound
opt(2).radbound=0.5; % brain surface element size bound
maxvol = '1=1:2=0.5'; 

tic
% [node,elem,face]=v2m(img,isovalues,opt,maxvol,method)
[nodes,elems,faces]=v2m(vol,[1 2],opt,maxvol, 'cgalmesh');
toc
figure, plotmesh(nodes, elems, 'x>20')

%Divide nodes
nodes = nodes /10;

%Orientation must be checked and meshreorient.m must be use 
%I think iso2mesh orientes the tet negatively in comparison with paraview
[newelem, evol]=meshreorient(nodes(:,1:3), elems(:,1:4));

SaveTetVtk(vtk_output, nodes(:,1:3), newelem, []);