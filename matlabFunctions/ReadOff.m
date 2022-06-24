function [ nodes, faces] = ReadOff(filename)
%READSURFOBJ Summary of this function goes here
%   Detailed explanation goes here

% Check filepath's extension
[~, ~, ext] = fileparts(filename);
if (~strcmp(ext,'.off'))
    error('Given filename should have .off extension');
end

% Open the file
fid=fopen(filename, 'rt');
if (fid == -1), error(['Error openning the mesh file: ',filename]); end

ln = fgets(fid); ln = fgets(fid);
a = sscanf(ln, '%d %d 0\n');
nnum = a(1);
fnum = a(2);

nodes = zeros(nnum,3);
faces = zeros(fnum,3);

ln = fgets(fid);
% search for the keyword in the file
for i = 1:nnum
    ln = fgets(fid);
    nodes(i,:) = sscanf(ln, '%f %f %f\n');
end

for i = 1:fnum
    ln = fgets(fid);
    faces(i,:) = sscanf(ln, '3  %d %d %d\n');
    faces(i,:) = faces(i,:)+1;
end

fclose(fid);

end

