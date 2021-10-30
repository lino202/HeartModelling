function [] = SaveSurfVtk(vtk_output, nodes, faces, field_data, nsets)
%SAVEEMBGRIDTOVTK Summary of this function goes here
%   Detailed explanation goes here

if nargin < 5, nsets = {}; end
if nargin < 4, field_data = {}; end

% Check filepath's extension
[~, ~, ext] = fileparts(vtk_output);
if (~strcmp(ext,'.vtk'))
    error('Filename should have .vtk extension');
end

% Check nodes and elems format
[nodes_num, nodes_dims] = size(nodes);
elems_num = size(faces,1);

if (nodes_num == 0)
    error('Nodes list is empty');
elseif (nodes_dims < 3)
    error('Unsupported nodes dimensions. Required nodes with dimensions 3')
end

if (elems_num == 0)
    error('Elements list is empty')
end

format long g;

% Open output file and write header
fileID = fopen(vtk_output,'w');
fprintf('Writing to VTK file: %s ...',vtk_output);
fprintf(fileID,'# vtk DataFile Version 3.0\n');
fprintf(fileID,'vtk output\n');
fprintf(fileID,'ASCII\n');
fprintf(fileID,'DATASET UNSTRUCTURED_GRID\n');


% Write nodes
fprintf(fileID,'POINTS %d float\n',nodes_num);
for nn = 1:nodes_num
    fprintf(fileID,'%10.15f %10.15f %10.15f\n', nodes(nn,:));
end

% Write elements
fprintf(fileID,'CELLS %d %d\n',elems_num, elems_num*(size(faces,2)+1));
for el_id = 1:elems_num
    fprintf(fileID,'%d %d %d %d\n',size(faces,2), faces(el_id,:)-1);
end

fprintf(fileID,'\nCELL_TYPES %d\n',elems_num);
for el_id = 1:elems_num
    fprintf(fileID,'5\n');
end

fprintf(fileID,'\n');

nsets_num = 0;
if ~isempty(field_data), nsets_num = nsets_num+size(field_data,2); end
if ~isempty(nsets), nsets_num = nsets_num+size(nsets,2); end
if nsets_num ~= 0
    fprintf(fileID,'POINT_DATA %d\n', nodes_num);
    fprintf(fileID,'FIELD FieldData %d\n', nsets_num);
end

if ~isempty(field_data)
    for i=1:size(field_data,2)
        field_dims = size(field_data{i}{1},2);
        if field_dims == 1
            field_format = '%10.15f\n';
        elseif field_dims == 2
            field_format = '%10.15f %10.15f\n';
        elseif field_dims == 3
            field_format = '%10.15f %10.15f %10.15f\n';
        end
        fprintf(fileID,'%s %d %d double\n', field_data{i}{2}, field_dims, nodes_num);
        for nn = 1:nodes_num
            fprintf(fileID,field_format, field_data{i}{1}(nn,:));
        end
        fprintf(fileID,'\n');  
    end
end

if ~isempty(nsets)
    for i=1:size(nsets,2)
        
        fprintf(fileID,'%s 1 %d int\n', nsets{i}{2}, nodes_num);
        flag = zeros(nodes_num,1);
        flag(nsets{i}{1}) = 1;
        for nn = 1:nodes_num
            fprintf(fileID,'%d\n',flag(nn));
        end
        fprintf(fileID,'\n');  
    end
end


% Close output file
fclose(fileID);

fprintf(' DONE\n');

end

