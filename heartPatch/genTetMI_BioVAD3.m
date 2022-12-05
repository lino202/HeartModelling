clear; close all;
addpath('../matlabFunctions', '../libraries/iso2mesh-1.9.6');

dataPath  = "F:/HeartModeling/Data_OM_MI/sampleP21_389/";
meshSurf = append(dataPath, "BioVAD/union.obj");
tetMesh = append(dataPath, "BioVAD/union_tetmesh.vtk");

[no, el, ~] = ReadObj(meshSurf);

seedHeart = surfseeds(no, el);
regions     = [seedHeart, 0.1];
tic
[nodes,elems]=surf2mesh(no,el,[],[],1,[],regions,[]);
toc
% figure; plotmesh(node,elem,'x>-6')
% cell_data = {{'myo_cells', elems(:,5)}};

tic
SaveTetVtk(tetMesh, nodes, elems(:,1:4), [], [], []);
toc