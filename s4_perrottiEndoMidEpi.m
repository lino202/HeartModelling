close all; clear;
format long g;
addpath('functions');


dataPath = '/home/maxi/Documents/PhD/Data/DTI_hearts/Data_Electra_DWI/sampleMA_MI1/';
transmural_pathA = append(dataPath, "/layers/", "transmural_distXV.txt");
transmural_pathB = append(dataPath, "/layers/", "transmural_distRV.txt"); 
transmural_pathC = append(dataPath, "/layers/", "transmural_distLV.txt");
% stim_nodes_path = append(dataPath, "\layers\", "stim_nodes_paraview.csv"); 
inputVtk = append(dataPath, '/electra_tetmesh.vtk');
inputInp = append(dataPath, '/electra_tetmesh.inp');
output_name = "layers_mesh_he";
algo = 2;
inf_as_healthy = 1;

myo_flag = 1;
scar_flag = 2;
endo_flag = 3;
mid_flag = 4;
epi_flag = 5;

endo_per = 40; endo_per = endo_per /100;
epi_per = 25; epi_per = epi_per /100;

phi0 = -1;
phi1 = 1;

%% Read Data


trans_distA = ReadSharpTxt(transmural_pathA);
trans_distB = ReadSharpTxt(transmural_pathB);
trans_distC = ReadSharpTxt(transmural_pathC);


% Read heart mask voxel points and fiber vectors
[points,fields] = ReadVtkPoints(inputVtk);
[nodes, elems, node_sets, cell_sets] = ReadAbaqus(inputInp);

for ff = 1:length(fields)
    if strcmp(fields{ff}{2},'endo'), endo_points = fields{ff}{1}; end
    if strcmp(fields{ff}{2},'mid'), mid_points = fields{ff}{1}; end
    if strcmp(fields{ff}{2},'epi'), epi_points = fields{ff}{1}; end
    if strcmp(fields{ff}{2},'myo'), myo_points = fields{ff}{1}; end
    if strcmp(fields{ff}{2},'scar'), scar_points = fields{ff}{1}; end
    if strcmp(fields{ff}{2},'dti-fibers'), fibs = fields{ff}{1}; end
end

if inf_as_healthy
    myo_points = ones(size(myo_points));
    scar_points = zeros(size(scar_points)); 
end
%% Calculate layers

phi_endo = (1-endo_per) * phi0 + endo_per * phi1;    % thresholds
phi_epi = epi_per * phi0 + (1-epi_per) * phi1;

transA_endo = zeros(size(points,1),1); transA_endo(trans_distA<phi_endo) = 1;
transA_epi = zeros(size(points,1),1); transA_epi(trans_distA>phi_epi) = 1;
transA_mid = zeros(size(points,1),1); transA_mid(trans_distA<=phi_epi & trans_distA>=phi_endo) = 1;
transB_endo = zeros(size(points,1),1); transB_endo(trans_distB<phi_endo) = 1;
transB_epi = zeros(size(points,1),1); transB_epi(trans_distB>phi_epi) = 1;
transB_mid = zeros(size(points,1),1); transB_mid(trans_distB<=phi_epi & trans_distB>=phi_endo) = 1;
transC_endo = zeros(size(points,1),1); transC_endo(trans_distC<phi_endo) = 1;
transC_epi = zeros(size(points,1),1); transC_epi(trans_distC>phi_epi) = 1;
transC_mid = zeros(size(points,1),1); transC_mid(trans_distC<=phi_epi & trans_distC>=phi_endo) = 1;

algo_points = zeros(size(points,1),1);
if algo == 1 
    % Algo 1 use A and B
    algo_points(logical(transA_epi)) = epi_flag;
    algo_points((transA_endo & transB_mid) | transA_mid) = mid_flag;
    algo_points(transA_endo & (transB_endo | transB_epi)) = endo_flag;
elseif algo == 2
    % Algo 2 use A, B and C
    algo_points(logical(transA_epi)) = epi_flag;
    algo_points((transA_endo | transA_mid) & (transB_mid | transB_epi) & (transC_mid | transC_epi)) = mid_flag;
    algo_points((transA_endo | transA_mid) & (transB_endo | transC_endo)) = endo_flag;
elseif algo == 3
    % Algo 3 use B and C
    algo_points(transB_epi & transC_epi) = epi_flag;
    algo_points(transB_mid | transC_mid) = mid_flag;
    algo_points(transB_endo | transC_endo) = endo_flag;
else 
    error("Unrecognised algorithm")
end

algo_points(scar_points==1) = scar_flag;
endo_points(algo_points==endo_flag) = 1;
mid_points(algo_points==mid_flag) = 1;
epi_points(algo_points==epi_flag) = 1;



%% Create nodesets and filed data for inp and vtk respectively 


% Collect field data
field_data = {{endo_points,'endo'},{mid_points,'mid'},{epi_points,'epi'},...
              {myo_points,'myo'}, {scar_points,'scar'}, {fibs,'dti-fibers'},...
              {algo_points, 'layers'}};

% Create node sets
nsets{endo_flag} = {find(endo_points),'endo_nodes'};
nsets{mid_flag} = {find(mid_points),'mid_nodes'};
nsets{epi_flag} = {find(epi_points),'epi_nodes'};
nsets{myo_flag} = {find(myo_points),'myo_nodes'};
nsets{scar_flag} = {find(scar_points),'scar_nodes'};


%% Finish saving and reporting

% Report partition percentages
fprintf('endo: %f %%\n',100*(length(find(endo_points))/length(points)));
fprintf('mid: %f %%\n',100*(length(find(mid_points))/length(points)));
fprintf('epi: %f %%\n',100*(length(find(epi_points))/length(points)));
fprintf('myo: %f %%\n',100*(length(find(myo_points))/length(points)));
fprintf('scar: %f %%\n',100*(length(find(scar_points))/length(points)));

SaveAbaqus(append(dataPath, "/layers/", output_name, ".inp"), points, elems(:,1:4), nsets);
SaveTetVtk(append(dataPath, "/layers/", output_name, ".vtk"), points, elems(:,1:4), field_data);


