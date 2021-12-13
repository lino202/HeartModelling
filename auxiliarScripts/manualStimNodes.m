close all; clear;
format long g;
addpath('functions');


dataPath = 'F:\DTI_konstas\data\sampleLE_Control2';
inputInp = append(dataPath, "/layers/", "layers_mesh2.inp");
inputVtk = append(dataPath, "/layers/", "layers_mesh2.vtk");
stim_folder = append(dataPath, "/stim/");
output_name = "final_mesh2";

myo_flag = 1;
scar_flag = 2;
endo_flag = 3;
mid_flag = 4;
epi_flag = 5;


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
SaveAbaqus(append(dataPath, "/stim/", output_name, ".inp"), nodes, elems(:,1:4), node_sets);
SaveTetVtk(append(dataPath, "/stim/", output_name, ".vtk"), nodes, elems(:,1:4), field_data);


