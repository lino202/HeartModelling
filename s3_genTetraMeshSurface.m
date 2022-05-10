clear; close all;
addpath('functions');
addpath('iso2mesh/iso2mesh-1.9.6');

% Input filenames
dataPath = 'F:/HeartModeling/Data/sampleLE_Control2/';
surfMesh = append(dataPath, 'surfMesh.obj');
heart_in = append(dataPath, 'dti.vtk');
myo_flag = 1;
scar_flag = 2;
endo_flag = 3;
mid_flag = 4;
epi_flag = 5;

% Output filenames
vtk_output = append(dataPath, 'electra_tetmesh_coarse.vtk');
inp_output = append(dataPath, 'electra_tetmesh_coarse.inp');
fibs_output = append(dataPath, 'electra_tetfibers_coarse.txt');

% Read heart surface mesh and normalize normals
[snodes, sfaces, snormals] = ReadObj(surfMesh); %from Meshlab
% [snodes, sfaces, snormals] = ReadSurfVtk(surfMesh);

surfSeeds=surfseeds(snodes(:,1:3),sfaces(:,1:3));
minBB = min(snodes);
maxBB = max(snodes);
[nodes,elems,faces]=surf2mesh(snodes,sfaces,minBB,maxBB,1,1,surfSeeds,[],0);
elems=removedupelem(elems);

% visualize the resulting mesh
% plotmesh(nodes,faces(:,1:3));
% axis equal;

% Read heart mask voxel points and fiber vectors
[points,fields] = ReadVtkPoints(heart_in);
for ff = 1:length(fields)
    if strcmp(fields{ff}{2},'endo_nodes'), endo_points = fields{ff}{1}; end
    if strcmp(fields{ff}{2},'mid_nodes'), mid_points = fields{ff}{1}; end
    if strcmp(fields{ff}{2},'epi_nodes'), epi_points = fields{ff}{1}; end
    if strcmp(fields{ff}{2},'myo_nodes'), myo_points = fields{ff}{1}; end
    if strcmp(fields{ff}{2},'scar_nodes'), scar_points = fields{ff}{1}; end
    if strcmp(fields{ff}{2},'dti-fibers'), fibs = fields{ff}{1}; end
end

endo = find(endo_points==1);
mid = find(mid_points==1);
epi = find(epi_points==1);
myo = find(myo_points==1);
scar = find(scar_points==1);

parts_points = zeros(size(points,1),1);
parts_points(endo) = endo_flag;
parts_points(mid) = mid_flag;
parts_points(epi) = epi_flag;
parts_points(myo) = myo_flag;
parts_points(scar) = scar_flag;

neigh = knnsearch(points,nodes);

parts_tet = parts_points(neigh);
endo_tet = find(parts_tet==endo_flag);
mid_tet = find(parts_tet==mid_flag);
epi_tet = find(parts_tet==epi_flag);
myo_tet = find(parts_tet==myo_flag);
scar_tet = find(parts_tet==scar_flag);

endo_flags = zeros(size(nodes,1),1);
endo_flags(endo_tet) = 1;

mid_flags = zeros(size(nodes,1),1);
mid_flags(mid_tet) = 1;

epi_flags = zeros(size(nodes,1),1);
epi_flags(epi_tet) = 1;

myo_flags = zeros(size(nodes,1),1);
myo_flags(myo_tet) = 1;

scar_flags = zeros(size(nodes,1),1);
scar_flags(scar_tet) = 1;

fibs_tet = fibs(neigh,:);

% Collect field data
field_data = {{endo_flags,'endo'},{mid_flags,'mid'},{epi_flags,'epi'},...
              {myo_flags,'myo'}, {scar_flags,'scar'}, {fibs_tet,'dti-fibers'}};

% Create node sets
nsets{endo_flag} = {endo_tet,'endo_nodes'};
nsets{mid_flag} = {mid_tet,'mid_nodes'};
nsets{epi_flag} = {epi_tet,'epi_nodes'};
nsets{myo_flag} = {myo_tet,'myo_nodes'};
nsets{scar_flag} = {scar_tet,'scar_nodes'};

% figure; hold on; 
% ShowFaces(nodes,faces(:,1:3),[.8 .8 .8],0.4);
% plot3(nodes(:,1),nodes(:,2),nodes(:,3),'bo','MarkerFaceColor','b','MarkerSize',5)
% hold off; daspect([1 1 1]);


% Report partition percentages
fprintf('endo: %f %%\n',100*(length(endo_tet)/length(nodes)));
fprintf('mid: %f %%\n',100*(length(mid_tet)/length(nodes)));
fprintf('epi: %f %%\n',100*(length(epi_tet)/length(nodes)));
fprintf('myo: %f %%\n',100*(length(myo_tet)/length(nodes)));
fprintf('scar: %f %%\n',100*(length(scar_tet)/length(nodes)));

SaveAbaqus(inp_output, nodes, elems(:,1:4), nsets);
SaveTetVtk(vtk_output, nodes, elems(:,1:4), field_data);
SaveFibersToTxt(fibs_output, fibs_tet);


