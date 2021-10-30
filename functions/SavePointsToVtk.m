function [] = SavePointsToVtk(vtk_output, nodes, field_data, nsets)
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
[nnum, ndims] = size(nodes);

if (nnum == 0)
    error('Nodes list is empty');
elseif (ndims < 1 || ndims > 3)
    error('Unsupported nodes dimensions. Required nodes with dimensions between 1 and 3')
end

format long g;

% Open output file and write header
fileID = fopen(vtk_output,'w');
fprintf(fileID,'# vtk DataFile Version 3.0\n');
fprintf(fileID,'vtk output\n');
fprintf(fileID,'ASCII\n');
fprintf(fileID,'DATASET UNSTRUCTURED_GRID\n');


% Write nodes
fprintf(fileID,'POINTS %d float\n',nnum);
for nn = 1:nnum
    if(ndims == 1)      % 1D
        fprintf(fileID,'%10.15 0.0000 0.0000f\n', nodes(nn,:));
    elseif(ndims == 2)  % 2D
        fprintf(fileID,'%10.15f %10.15f 0.0000\n', nodes(nn,:));
    else                     % 3D
        fprintf(fileID,'%10.15f %10.15f %10.15f\n', nodes(nn,:));
    end
end


% Write cells
fprintf(fileID,'CELLS %d %d\n',nnum, 2*nnum);
for id = 1:nnum
   fprintf(fileID,'%d %d\n', 1, id-1);
end

fprintf(fileID,'\nCELL_TYPES %d\n',nnum);
for id = 1:nnum
   fprintf(fileID,'1\n');
end
fprintf(fileID,'\n');

nsets_num = 0;
if ~isempty(field_data), nsets_num = nsets_num+size(field_data,2); end
if ~isempty(nsets), nsets_num = nsets_num+size(nsets,2); end

fprintf(fileID,'POINT_DATA %d\n', nnum);
fprintf(fileID,'FIELD FieldData %d\n', nsets_num);
    
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
        fprintf(fileID,'%s %d %d double\n', field_data{i}{2}, field_dims, nnum);
        for nn = 1:nnum
            fprintf(fileID,field_format, field_data{i}{1}(nn,:));
        end
        fprintf(fileID,'\n');  
    end
end

if ~isempty(nsets)
    for i=1:size(nsets,2)
        
        fprintf(fileID,'%s 1 %d int\n', nsets{i}{2}, nnum);
        flag = zeros(nnum,1);
        flag(nsets{i}{1}) = 1;
        for nn = 1:nnum
            fprintf(fileID,'%d\n',flag(nn));
        end
        fprintf(fileID,'\n');  
    end
end


% Close output file
fclose(fileID);

fprintf(' DONE\n');

end

