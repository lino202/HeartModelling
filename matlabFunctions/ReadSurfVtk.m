function [ nodes, faces, normals] = ReadSurfVtk(filename)
%READSURFOBJ Summary of this function goes here
%   Detailed explanation goes here

% Check filepath's extension
[~, ~, ext] = fileparts(filename);
if (~strcmp(ext,'.vtk'))
    error('Given filename should have .vtk extension');
end

% Open the file
fid=fopen(filename, 'rt');
if (fid == -1), error(['Error openning the mesh file: ',filename]); end

% search for the keyword in the file
ln = fgets(fid);
while ischar(ln)    
    if(contains(ln,'POINTS'))
        nodes_num = sscanf(ln, 'POINTS %d DOUBLE\n');
        nodes = fscanf(fid,'%f %f %f',[3, nodes_num])';
    end
    
    if(contains(ln,'POLYGONS'))
        faces_num = sscanf(ln, 'POLYGONS %d %d\n');
        faces_num = faces_num(1);
        faces = fscanf(fid,'%d %d %d %d',[4, faces_num])';
    end
    
    if(contains(ln,'NORMALS'))
        normals_num = nodes_num; %sscanf(ln, 'NORMALS Normals float\n');
        normals = fscanf(fid,'%f %f %f',[3, normals_num])';
    end
    
    ln = fgets(fid);
end

faces = faces(:,2:end)+1;

fclose(fid);

end

