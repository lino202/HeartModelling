clear; close all;
addpath('../matlabFunctions', '../libraries/iso2mesh-1.9.6');

dataPath  = "F:/HeartModeling/Data_OM_MI/sampleP21_389/";
meshXorSurf = append(dataPath, "BioVAD/final_mipatch_surfmesh.obj");
meshScaffSurf = append(dataPath, "BioVAD/final_shell.obj");
meshHeartSurf = append(dataPath, "/surfMesh.obj");
tetMesh = append(dataPath, "/heartPatch_tetmesh.vtk");


[no, el, ~] = ReadObj(meshXorSurf);
[noScaff, elScaff, ~] = ReadObj(meshScaffSurf);
[noHeart, elHeart, ~] = ReadObj(meshHeartSurf);

seedHeart = surfseeds(noHeart, elHeart);
seedScaff = surfseeds(noScaff, elScaff);

regions     = [seedHeart, 0.1; seedScaff, 0.025];
tic
[nodes,elems]=surf2mesh(no,el,[],[],1,[],regions,[]);
toc
% figure; plotmesh(node,elem,'x>-6')
cell_data = {{'myo_cells', elems(:,5)}};

tic
SaveTetVtk(tetMesh, nodes, elems(:,1:4), [], [], cell_data);
toc