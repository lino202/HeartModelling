clear; close all;
addpath('../matlabFunctions', '../libraries/iso2mesh-1.9.6');

surfMesh = "F:\HeartModeling\Fassina\fassina_perfectsquare\surface.obj";
vtk_output = "F:\HeartModeling\Fassina\fassina_perfectsquare\tetmesh.vtk";
dx = 0.01;
myothickness = 6;
edgeLengthMyo = 0.1;
edgeLengthPatch = 0.025;

[snodes, sfaces, ~] = ReadObj(surfMesh); %from Meshlab


patchNodeIdxsUp = find(snodes(:,3)>myothickness-dx);
patchNodeIdxsLeft = find(snodes(:,2)>1.5-dx);
patchNodeIdxsRight = find(snodes(:,2)<8.5+dx);
patchNodeIdxs = intersect(patchNodeIdxsLeft, patchNodeIdxsRight);
patchNodeIdxs = intersect(patchNodeIdxs, patchNodeIdxsUp);

snodes = [snodes, zeros(size(snodes,1),1)];
snodes(patchNodeIdxs,4) = 0.1;
snodes(snodes(:,4)==0,4) = 0.1;

regions     = [1,5,3; 1,5,6.25];
tic
[nodes,elems,faces]=surf2mesh(snodes,sfaces,[],[],1,[],regions,[]);
toc 

figure, plotmesh(nodes, elems, 'x>1')

cell_data = {{'myo_cells', elems(:,5)}};
tic
SaveTetVtk(vtk_output, nodes, elems(:,1:4), [], [], cell_data);
toc


%% Refinement

patchNodeIdxs = unique(elems(elems(:,5)==2,1:4));
opt = ones(size(nodes,1),1) * edgeLengthMyo;
opt(patchNodeIdxs) = edgeLengthPatch;
[newnode,newelem,newface]=meshrefine(nodes,elems,opt);

cell_data = {{'myo_cells', newelem(:,5)}};
tic
SaveTetVtk(vtk_output, newnode, newelem(:,1:4), [], [], cell_data);
toc
