% One the patch_heart superficial mesh is cleaned we use this code to generate the tet mesh

% This code is similar to s3_genTetraMeshSurface, but here we have two
% cavities the heart and patch and we need to account that and select the
% edge length for both. Also we erased the possibility to use surf2mesh, so
% to use a windows implementation of tetgen cause using linux (WSL as well)
% yielded better results. The possibility of using the maxvol was erase as 
% its used is possible per region when using surf2mesh some extra things
% should we done for incorporate this in surf2meshWSL and it was not
% working so we erased it as the common use case of WSL + edge length is
% sufficient for generating these meshes and this is implemented here.

clear; close all; clc;

addpath('../matlabFunctions', '../libraries/iso2mesh-1.9.6');

tetgenPath    = '/home/maxi/Programs/tetgen1.6.0/tetgen';
dataPath      = 'D:/Paper4/Models/sample12/EHT2/';
meshXorSurf   = append(dataPath, "mesh/final_mipatch_surfmesh.obj");
meshScaffSurf = append(dataPath, "mesh/final_shell.obj");
meshHeartSurf = 'D:/Paper3/Models/invivo/mi/la/sample12/mesh/surfMesh.obj';
outmesh       = append(dataPath, "mesh/tetmesh");

edgeLength = [0.3, 0.13]; %0.3,0.13 for paper4, [heart, eht]

%% Read

[snodescolors, sfaces, ~] = ReadObj(meshXorSurf, true);
snodes = snodescolors(:,1:3);
colors = snodescolors(:,4:6);
[noScaff, elScaff, ~] = ReadObj(meshScaffSurf, false);
[noHeart, elHeart, ~] = ReadObj(meshHeartSurf, false);

seedHeart = surfseeds(noHeart, elHeart);
seedScaff = surfseeds(noScaff, elScaff);

%% Compute 

cmdopt = '-p -q1.414 -V -D -A -k';    %A is for labeling the cells

% we get the patch idxs from colors
idxs_heart = find(colors(:,1)==0);
regions     = [seedHeart; seedScaff];
nodes_edgelengths = ones(size(snodes,1),1) * edgeLength(2);
nodes_edgelengths(idxs_heart) = edgeLength(1);
snodes = [snodes, nodes_edgelengths];
cmdopt = append(cmdopt, ' -m');

surf2meshWSL(snodes,sfaces,[],[],1,[],regions,[],0, 'tetgen', cmdopt, outmesh, tetgenPath);

