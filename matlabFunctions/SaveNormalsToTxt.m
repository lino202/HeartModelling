function [] = SaveNormalsToTxt(txt_output, normals)
%SAVENORMALTOTXT Summary of this function goes here
%   Detailed explanation goes here

% Check filepath's extension
[~, ~, ext] = fileparts(txt_output);
if (~strcmp(ext,'.txt'))
    error('Normals filename should have .txt extension');
end

% Check nodes and elems format
[normals_num, normals_dims] = size(normals);

if (normals_num == 0)
    error('Nodes list is empty');
elseif (normals_dims < 2 || normals_dims > 3)
    error('Unsupported normals dimensions. Required normal vectors with dimensions between 2 and 3')
end

format long g;

% Open output file and write header
fileID = fopen(txt_output,'w');
fprintf('Writing to normals to file: %s ...\n',txt_output);
fprintf(fileID,'##\n');
fprintf(fileID,'# Normal vectors for meshless grid\n');
fprintf(fileID,'# Created by: SaveNormalsToTxt.m\n');
fprintf(fileID,'# Format: Node index, Normal X coordinate, Normal Y coordinate, Normal Z coordinate\n');
fprintf(fileID,'##\n');

% Write normals
for nn = 1:normals_num
    if(normals_dims == 2)  % 2D
        fprintf(fileID,'%d, %10.15f, %10.15f\n', nn, normals(nn,:));
    else                     % 3D
        fprintf(fileID,'%d, %10.15f, %10.15f, %10.15f\n', nn, normals(nn,:));
    end
end

fprintf(fileID,'##\n');
fprintf(fileID,'# END of file\n');
fprintf(fileID,'##\n');

fclose(fileID);

end

