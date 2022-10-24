clear; close all;
addpath('../matlabFunctions', '../libraries/iso2mesh-1.9.6');

dataPath  = "F:/HeartModeling/Data_OM_MI/sampleP21_389/";
meshInner = append(dataPath, "surfMesh.obj");
meshOuter = append(dataPath, "BioVAD/outSurfMesh.obj");
inOutMesh = append(dataPath, "BioVAD/inOutMesh.vtk");
myoPatchMesh   = append(dataPath, "BioVAD/myo_patch.vtk");


[nInner, fInner, ~] = ReadObj(meshInner);
[nOuter, fOuter, ~] = ReadObj(meshOuter);

[nComb, fComb] = mergesurf(nInner, fInner, nOuter, fOuter);
[nComb,fComb]=meshcheckrepair(nComb,fComb,[]);
% SaveSurfVtk(inOutMesh, nComb(:,1:3), fComb(:,1:3), [], []);

seedInner = surfseeds(nInner, fInner);
[idx, dist] = closestnode(nInner, nOuter(1,:));
seedOut     = nOuter(1,:) - (nOuter(1,:) - nInner(idx,:)) .* dist/3;
% seedBG      = nOuter(1,:) + (nOuter(1,:) - nInner(idx,:)) .* dist/3;
regions     = [seedOut, 0.025; seedInner 0.1];
% minBB = min(nComb) - 2;  %only required for forcebox
% maxBB = max(nComb) + 2;

tic
[nodes,elems]=surf2mesh(nComb,fComb,[],[],1,[],regions,[]);
toc
cell_data = {{'myo_cells', elems(:,5)}};
tic
SaveTetVtk(myoPatchMesh, nodes, elems(:,1:4), [], [], cell_data);
toc
% plotmesh(nodes,elems(elems(:,end)>0,:), 'x>0')







