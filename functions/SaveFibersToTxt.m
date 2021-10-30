function [] = SaveFibersToTxt(txt_output, fibers)
%SAVENORMALTOTXT Summary of this function goes here
%   Detailed explanation goes here

% Check filepath's extension
[~, ~, ext] = fileparts(txt_output);
if (~strcmp(ext,'.txt'))
    error('Fibers filename should have .txt extension');
end

% Check nodes and elems format
[fibers_num] = size(fibers,1);


format long g;

% Open output file and write header
fileID = fopen(txt_output,'w');
fprintf('Writing fibers to file: %s ...\n',txt_output);
fprintf(fileID,'##\n');
fprintf(fileID,'# Fibers for immersed meshless grid\n');
fprintf(fileID,'# Created by: SaveFibersToTxt.m\n');
fprintf(fileID,'# Format: Fiber X coordinate, Fiber Y coordinate, Fiber Z coordinate\n');
fprintf(fileID,'##\n');

% Write normals
for nn = 1:fibers_num
    fprintf(fileID,'[%10.15f, %10.15f, %10.15f],\n', fibers(nn,:));
end

fclose(fileID);

end

