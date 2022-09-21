clear; close all;
addpath('matlabFunctions', 'libraries/iso2mesh-1.9.6');

% Input filenames
dataPath = 'F:\HeartModeling\Data_1\sampleLE_Control2\';
surfMesh = append(dataPath, 'surfMesh_Covered.obj');
vtk_output = append(dataPath, 'tetmesh_coarse_covered.vtk');
tetMaxVol = 1;

% Read heart surface mesh and normalize normals
[snodes, sfaces, snormals] = ReadObj(surfMesh); %from Meshlab
% [snodes, sfaces, snormals] = ReadSurfVtk(surfMesh);

surfSeeds=surfseeds(snodes(:,1:3),sfaces(:,1:3));
minBB = min(snodes);
maxBB = max(snodes);
fprintf('SurfSeed inside, usually only one \n %f %f %f \n', surfSeeds(1,:));
fprintf("SurfSeed holes, usually two \n %f %f %f \n %f %f %f\n", surfSeeds(2:3,:));

[nodes,elems,faces]=surf2mesh(snodes,sfaces,minBB,maxBB,1,tetMaxVol,surfSeeds(1,:),surfSeeds(2:3,:),0);
elems=removedupelem(elems);

% visualize the resulting mesh
% plotmesh(nodes,faces(:,1:3));
% axis equal;

% figure; hold on; 
% ShowFaces(nodes,faces(:,1:3),[.8 .8 .8],0.4);
% plot3(nodes(:,1),nodes(:,2),nodes(:,3),'bo','MarkerFaceColor','b','MarkerSize',5)
% hold off; daspect([1 1 1]);

SaveTetVtk(vtk_output, nodes, elems(:,1:4), []);



