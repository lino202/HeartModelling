clear; close all;
addpath('../matlabFunctions', '../libraries/iso2mesh-1.9.6');

dataPath  = "F:/HeartModeling/Data_OM_MI/sampleP21_389/";
meshXorSurf = append(dataPath, "BioVAD/xor.obj");
tetMesh = append(dataPath, "BioVAD/heartPatch_tetmesh.vtk");
seedHeart = [-1.1945, -50.49, 22.8328, 0.1];
seedScaffold = [-6.2871, -60.1, 9.93, 0.025];
seedInner = [-6.2871, -69.8, 9.93, 0.025];

[no, el, ~] = ReadObj(meshXorSurf);
regions     = [seedScaffold; seedInner; seedHeart];
tic
[nodes,elems]=surf2mesh(no,el,[],[],1,[],regions,[]);
toc
% figure; plotmesh(node,elem,'x>-6')
cell_data = {{'myo_cells', elems(:,5)}};
tic
SaveTetVtk(tetMesh, nodes, elems(:,1:4), [], [], cell_data);
toc