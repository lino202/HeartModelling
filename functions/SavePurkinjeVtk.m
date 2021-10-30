function [] = SavePurkinjeVtk(filename, nodes, elems, nsets)
%
%%

% Check filepath's extension
[~, ~, ext] = fileparts(filename);
if (~strcmp(ext,'.vtk'))
    error('Filename should have .vtk extension');
end

% Check nodes and elems format
[nnum, ndims] = size(nodes);
elnum = size(elems,1);

if (nnum == 0)
    error('Nodes list is empty');
elseif (ndims < 3)
    error('Unsupported nodes dimensions. Required nodes with dimensions 3')
end


format long g;

% Open output file and write header
fid = fopen(filename,'w');
fprintf('Writing to VTK file: %s ...',filename);
fprintf(fid,'# vtk DataFile Version 3.0\n');
fprintf(fid,'vtk output\n');
fprintf(fid,'ASCII\n');
fprintf(fid,'DATASET UNSTRUCTURED_GRID\n');


% Write nodes
fprintf(fid,'POINTS %d float\n',nnum);
for nn = 1:nnum
    fprintf(fid,'%10.15f %10.15f %10.15f\n', nodes(nn,:));
end

% Write elements
fprintf(fid,'CELLS %d %d\n',elnum, elnum*(size(elems,2)+1));
for el_id = 1:elnum
    fprintf(fid,'%d %d %d\n',size(elems,2), elems(el_id,:)-1);
end

fprintf(fid,'\nCELL_TYPES %d\n',elnum);
for el_id = 1:elnum
    fprintf(fid,'3\n');
end

fprintf(fid,'\n');

if (isempty(nsets) == 0)
    
    % Number of node sets
    nsets_num = length(nsets);
    
    fprintf(fid,'POINT_DATA %d\n', nnum);
    fprintf(fid,'FIELD FieldData %d\n',nsets_num);
    
    for ns = 1:nsets_num
       fprintf('Writing node set %s...\n',nsets{ns}{2}); 
       
       fprintf(fid,'%s 1 %d int\n',nsets{ns}{2}, nnum);
  
       scalar = zeros(nnum,1);
       scalar(nsets{ns}{1}) = 1;  
       for i = 1:nnum
           fprintf(fid,'%d\n', scalar(i));
       end
       fprintf(fid,'\n');
            
       fprintf('Wrote node set %s\n',nsets{ns}{2});
       
    end
    
end

fprintf('Wrote successfully Paraview mesh file: %s\n',filename);

% Close output file
fclose(fid);


end










