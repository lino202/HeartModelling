function [ nodes, faces, normals ] = ReadObj(filename, hasColor)
%READSURFOBJ Summary of this function goes here
%   Detailed explanation goes here
% You need to pass a .obj from meshlab typically where the normals where
% saved, and if you have colors remember your nodes will have 6 components
% x,y,z and r,g,b

% Check filepath's extension
[~, ~, ext] = fileparts(filename);
if (~strcmp(ext,'.obj'))
    error('Given filename should have .obj extension');
end

if nargin < 2, hasColor = false; end

% Open the file
fid=fopen(filename, 'rt');
if (fid == -1), error(['Error openning the mesh file: ',filename]); end

% search for the keyword in the file
for i = 1:11
    ln = fgets(fid);
    
    if(contains(ln,'Vertices'))
        nodes_num = sscanf(ln, '# Vertices: %d\n');
    end
    
    if(contains(ln,'Faces'))
        faces_num = sscanf(ln, '# Faces: %d\n');
    end
end

if hasColor
    nodes = zeros(nodes_num,6);
else
    nodes = zeros(nodes_num,3);
end

normals = zeros(nodes_num,3);
faces = zeros(faces_num,3);

for i = 1:nodes_num
    ln = fgets(fid);
    normals(i,:) = sscanf(ln, 'vn %f %f %f\n')';
    ln = fgets(fid);
    if hasColor
        nodes(i,:) = sscanf(ln, 'v %f %f %f %f %f %f\n')';
    else
        nodes(i,:) = sscanf(ln, 'v %f %f %f\n')';
    end
    
end
ln = fgets(fid);
ln = fgets(fid);

for i = 1:faces_num
    ln = fgets(fid);
    fc = sscanf(ln, 'f %f//%f %f//%f %f//%f\n')';
    faces(i,:) = fc(1:2:end);
end


fclose(fid);

end

