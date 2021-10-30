function [] = SaveEmbGridToVtk(vtk_output, nodes, elems, field_data, nsets)
%SAVEEMBGRIDTOVTK Summary of this function goes here
%   Detailed explanation goes here

if nargin < 4, nsets = {}; end
if nargin < 3, field_data = {}; end

% Check filepath's extension
[~, ~, ext] = fileparts(vtk_output);
if (~strcmp(ext,'.vtk'))
    error('VTK embedded grid filename should have .vtk extension');
end

% Check nodes and elems format
[nodes_num, nodes_dims] = size(nodes);
[elems_num, elems_dims] = size(elems);

if (nodes_num == 0)
    error('Nodes list is empty');
elseif (nodes_dims < 1 || nodes_dims > 3)
    error('Unsupported nodes dimensions. Required nodes with dimensions between 1 and 3')
end

if (elems_num == 0)
    error('Elements list is empty')
end

format long g;

% Open output file and write header
fileID = fopen(vtk_output,'w');
fprintf('Writing to VTK embedded grid file: %s ...',vtk_output);
fprintf(fileID,'# vtk DataFile Version 3.0\n');
fprintf(fileID,'vtk output\n');
fprintf(fileID,'ASCII\n');
fprintf(fileID,'DATASET UNSTRUCTURED_GRID\n');


% Write nodes
fprintf(fileID,'POINTS %d float\n',nodes_num);
for nn = 1:nodes_num
    if(nodes_dims == 1)      % 1D
        fprintf(fileID,'%10.15 0.0000 0.0000f\n', nodes(nn,:));
    elseif(nodes_dims == 2)  % 2D
        fprintf(fileID,'%10.15f %10.15f 0.0000\n', nodes(nn,:));
    else                     % 3D
        fprintf(fileID,'%10.15f %10.15f %10.15f\n', nodes(nn,:));
    end
end


surf_nodes_num = max(max(elems));
inter_nodes_num = nodes_num-surf_nodes_num;

% Write elements
fprintf(fileID,'CELLS %d %d\n',elems_num+inter_nodes_num, elems_num*(size(elems,2)+1) + inter_nodes_num*2);
for el_id = 1:elems_num
    if(elems_dims == 2)        % Line element
        fprintf(fileID,'%d %d %d\n',size(elems,2), elems(el_id,:)-1);
    elseif(elems_dims == 3)    % Triangle element
        fprintf(fileID,'%d %d %d %d\n',size(elems,2), elems(el_id,:)-1);
    elseif(elems_dims == 4)    % Quadrilateral element
        fprintf(fileID,'%d %d %d %d %d\n',size(elems,2), elems(el_id,:)-1);
    else
        error('Unsupported element type');
    end
end
for p_id = 1:inter_nodes_num
   id = surf_nodes_num + p_id - 1;
   fprintf(fileID,'%d %d\n', 1, id);
end

fprintf(fileID,'\nCELL_TYPES %d\n',elems_num+inter_nodes_num);
for el_id = 1:elems_num
    if(elems_dims == 2)        % Line element
        fprintf(fileID,'3\n');
    elseif(elems_dims == 3)    % Triangle element
        fprintf(fileID,'5\n');
    elseif(nodes_dims == 2 && elems_dims == 4)    % Quadrilateral element
        fprintf(fileID,'9\n');
    end
end
for p_id = 1:inter_nodes_num
   fprintf(fileID,'1\n');
end
fprintf(fileID,'\n');

nsets_num = 2;
if ~isempty(field_data), nsets_num = nsets_num+size(field_data,2); end
if ~isempty(nsets), nsets_num = nsets_num+size(nsets,2); end

fprintf(fileID,'POINT_DATA %d\n', nodes_num);
fprintf(fileID,'FIELD FieldData %d\n', nsets_num);
    
% Surface nodes nodeset
surf_nodes_flag = zeros(nodes_num,1);
surf_nodes_flag(1:max(max(elems))) = 1;
fprintf(fileID,'%s 1 %d int\n','SurfaceNodes', nodes_num);
for nn = 1:nodes_num
    fprintf(fileID,'%d\n', surf_nodes_flag(nn,:));
end
fprintf(fileID,'\n');

% Interior nodes nodeset
inter_nodes_flag = zeros(nodes_num,1);
inter_nodes_flag(max(max(elems))+1:end) = 1;
fprintf(fileID,'%s 1 %d int\n','InteriorNodes', nodes_num);
for nn = 1:nodes_num
    fprintf(fileID,'%d\n', inter_nodes_flag(nn,:));
end
fprintf(fileID,'\n');


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

