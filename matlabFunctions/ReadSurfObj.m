function [ nodes, faces, normals ] = ReadSurfObj( obj_file )
%READSURFOBJ Summary of this function goes here
%   Detailed explanation goes here

% Check filepath's extension
[~, ~, ext] = fileparts(obj_file);
if (~strcmp(ext,'.obj'))
    error('Given filename should have .obj extension');
end

% Open the file
fid=fopen(obj_file, 'rt');
if (fid == -1), error(['Error openning the mesh file: ',obj_file]); end

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

nodes = zeros(nodes_num,3);
normals = zeros(nodes_num,3);
faces = zeros(faces_num,3);

for i = 1:nodes_num
    ln = fgets(fid);
    normals(i,:) = sscanf(ln, 'vn %f %f %f\n')';
    ln = fgets(fid);
    nodes(i,:) = sscanf(ln, 'v %f %f %f\n')';
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

