close all; clear;
format long g;
addpath('../functions');


dataPath = 'F:\Electra\electra_sims\Heart\Purkinje\sampleMA_Control2\';
inputInp = append(dataPath, "layers_mesh_he.inp");
inputVtk = append(dataPath, "layers_mesh_he.vtk");
stim_folder = dataPath;
output_name = "fibrilation_mesh";


%% Read Data

[points,fields] = ReadVtkPoints(inputVtk);
[nodes, elems, node_sets, cell_sets] = ReadAbaqus(inputInp);


%% Read stimulation files

stim_field_data = {};
Files=dir(append(stim_folder, '*.csv'));
for k=1:length(Files)
   fileName = Files(k).name;
   stim_points = getNodesFromCSV(points, append(stim_folder, fileName));
   fileName = split(fileName,'.');
   stim_field_data{k} = {stim_points, fileName{1} };
end



%% Add if needed stim nodessets and field data
field_data = fields';
          
limit = size(field_data,2);
for i = 1:size(stim_field_data,2)
    field_data{limit+i} = {stim_field_data{i}{1},stim_field_data{i}{2}};
end

limit = size(node_sets,2);
for i = 1:size(stim_field_data,2)
    node_sets{limit+i} = {find(stim_field_data{i}{1}),stim_field_data{i}{2}};
end


%% Finish saving
SaveAbaqus(append(dataPath, output_name, ".inp"), nodes, elems(:,1:4), node_sets);
SaveTetVtk(append(dataPath, output_name, ".vtk"), nodes, elems(:,1:4), field_data);


