clear; close all;
addpath('../matlabFunctions', '../libraries/iso2mesh-1.9.6');

% Input filenames
dataPath = 'F:\HeartModeling\Data_1\sampleLE_Control3\';
mskName = 'Segmentation.seg.nrrd';
msk = ReadNrrd(append(dataPath, mskName));
pointsVoxelMap = load(append(dataPath, 'pointVoxelMap.mat')).pointVoxelMap;


% Output filenames
vtk_output = append(dataPath, 'tetmesh.vtk');


% Read heart surface mesh and normalize normals
minBB = min(pointsVoxelMap);
maxBB = max(pointsVoxelMap);
ix = minBB(1):maxBB(1);
iy = minBB(2):maxBB(2);
iz = minBB(3):maxBB(3);
% opt.radbound = 1;
[nodes,elems,faces,regions]=vol2mesh(msk.pixelData,ix,iy,iz,1,[],1);


% SaveTetVtk(vtk_output, nodes, elems(:,1:4), []);



