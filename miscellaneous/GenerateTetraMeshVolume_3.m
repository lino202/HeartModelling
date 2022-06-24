clear; close all;
addpath('functions');
addpath('iso2mesh\iso2mesh-1.9.6');

% Input filenames
dataPath = 'F:\DTI_konstas\data\sampleControl2\';
mskName = 'Segmentation.seg.nrrd';
msk = ReadNrrd(append(dataPath, mskName));
pointsVoxelMap = load(append(dataPath, 'pointVoxelMap.mat')).pointVoxelMap;
heart_in = append(dataPath, 'dti.vtk');

% Output filenames
vtk_output = append(dataPath, 'electra_tetmesh.vtk');
inp_output = append(dataPath, 'electra_tetmesh.inp');
fibs_output = append(dataPath, 'electra_tetfibers.txt');

% Read heart surface mesh and normalize normals


minBB = min(pointsVoxelMap);
maxBB = max(pointsVoxelMap);
ix = minBB(1):maxBB(1);
iy = minBB(2):maxBB(2);
iz = minBB(3):maxBB(3);
% opt.radbound = 1;
[nodes,elems,faces,regions]=vol2mesh(msk.pixelData,ix,iy,iz,1,[],1);

plotmesh(nodes,faces);
axis equal;

% Read heart mask voxel points and fiber vectors
[points,fields] = ReadVtkPoints(heart_in);
for ff = 1:length(fields)
    if strcmp(fields{ff}{2},'endo_nodes'), endo_points = fields{ff}{1}; end
    if strcmp(fields{ff}{2},'mid_nodes'), mid_points = fields{ff}{1}; end
    if strcmp(fields{ff}{2},'epi_nodes'), epi_points = fields{ff}{1}; end
    if strcmp(fields{ff}{2},'dti_fibers'), fibs = fields{ff}{1}; end
end

endo = find(endo_points==1);
mid = find(mid_points==1);
epi = find(epi_points==1);

parts_points = zeros(size(points,1),1);
parts_points(endo) = 3;
parts_points(mid) = 2;
parts_points(epi) = 1;

neigh = knnsearch(points,nodes);

parts_tet = parts_points(neigh);
endo_tet = find(parts_tet==3);
mid_tet = find(parts_tet==2);
epi_tet = find(parts_tet==1);

endo_flags = zeros(size(nodes,1),1);
endo_flags(endo_tet) = 1;

mid_flags = zeros(size(nodes,1),1);
mid_flags(mid_tet) = 1;

epi_flags = zeros(size(nodes,1),1);
epi_flags(epi_tet) = 1;

fibs_tet = fibs(neigh,:);

% Collect field data
field_data = {{endo_flags,'endo'},{mid_flags,'mid'},{epi_flags,'epi'},...
              {fibs_tet,'dti_fibers'}};

% Create node sets
nsets{1} = {endo_tet,'endo_nodes'};
nsets{2} = {mid_tet,'mid_nodes'};
nsets{3} = {epi_tet,'epi_nodes'};

figure; hold on; 
ShowFaces(nodes,faces(:,1:3),[.8 .8 .8],0.4);
plot3(nodes(:,1),nodes(:,2),nodes(:,3),'bo','MarkerFaceColor','b','MarkerSize',5)
hold off; daspect([1 1 1]);


% Report partition percentages
fprintf('endo: %f %%\n',100*(length(endo_tet)/length(nodes)));
fprintf('mid: %f %%\n',100*(length(mid_tet)/length(nodes)));
fprintf('epi: %f %%\n',100*(length(epi_tet)/length(nodes)));


SaveAbaqus(inp_output, nodes, elems(:,1:4), nsets);
SaveTetVtk(vtk_output, nodes, elems(:,1:4), field_data);
SaveFibersToTxt(fibs_output, fibs_tet);


