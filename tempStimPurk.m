close all; clear;
format long g;
addpath('functions');


dataPath = 'F:\DTI_konstas\data\sampleMA_Control2\';
inputInp = append(dataPath, "\layers\", "basal2_tetmesh.inp");
inputInp2 = append(dataPath, "final_mesh.inp");
output_name = "final_mesh";


%% Read Data

% Read heart mask voxel points and fiber vectors
[nodes, elems, node_sets, cell_sets] = ReadAbaqus(inputInp);
[nodes2, elems2, node_sets2, cell_sets2] = ReadAbaqus(inputInp2);

%% Create nodesets and filed data for inp and vtk respectively 


% Collect field data
stim_data = {};
stim_nodes = [];
cont = 1;
myendo = node_sets2{3}{1};
for i=1:size(node_sets,2)
    tmp = node_sets{1,i};
    idx = tmp{1,1};
    find(idx==0)
    name = tmp{1,2};
    
    if ~(name == "endo_nodes" || name == "mid_nodes" || name == "epi_nodes")
        spatial_stim_points = nodes(idx,:);
        neigh = knnsearch(nodes2, spatial_stim_points);
        neigh = unique(neigh);
        neigh(ismember(neigh,stim_nodes)) = [];
        neigh = neigh(ismember(neigh,myendo));
        
        stim_nodes = [stim_nodes; neigh];
        stim_data{cont} = {neigh,name};
        
        cont = cont +1;
    end
    
end

limit = size(node_sets2,2);
for i=1:size(stim_data,2)
    node_sets2{limit+i} = stim_data{i};
    
end

field_data = {};
for i=1:size(node_sets2,2)
    points = zeros(size(nodes2,1),1);
    points(node_sets2{i}{1}) = 1;
    field_data{i} = {points, node_sets2{i}{2}};
end

%% Finish saving
SaveAbaqus(append(dataPath, "layers/", output_name, "_my.inp"), nodes2, elems2(:,1:4), node_sets2);
SaveTetVtk(append(dataPath, "layers/", output_name, "_my.vtk"), nodes2, elems2(:,1:4), field_data);


