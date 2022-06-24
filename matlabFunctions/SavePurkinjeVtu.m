function [] = SavePurkinjeVtu(output_meshfile, nodes, elems)
%
%%


% Check if filepath is string
if ((ischar(output_meshfile) == 0) && (isstring(output_meshfile) == 0))
    error('File path input required');
end

% Check filepath's extension
[~, ~, ext] = fileparts(output_meshfile);
if (~strcmp(ext,'.vtu'))
    error('Paraview mesh filename should have .vtu extension');
end

% Check nodes and elems format
nodes_num = size(nodes,1);
elems_num = size(elems,1);

format long g;

% Open output file and write header
fileID = fopen(output_meshfile,'w');
fprintf('Writing to Paraview mesh file: %s\n',output_meshfile);

fprintf(fileID,'<VTKFile type="UnstructuredGrid" version="0.1" byte_order="BigEndian">\n');
fprintf(fileID,'<UnstructuredGrid>\n');
fprintf(fileID,'<Piece NumberOfPoints="%d" NumberOfCells="%d">\n',nodes_num, elems_num);
fprintf(fileID,'<Points>\n');
fprintf(fileID,'<DataArray type="Float32" NumberOfComponents="3" Format="ascii">');

% Write nodes
for nn = 1:nodes_num-1
    fprintf(fileID,'%10.15f %10.15f %10.15f\n',nodes(nn,:));
end
fprintf(fileID,'%10.15f %10.15f %10.15f</DataArray>\n',nodes(end,:));

% Write elements
fprintf(fileID,'</Points>\n');
fprintf(fileID,'<Cells>\n');
fprintf(fileID,'<DataArray type="Int32" Name="connectivity" Format="ascii">');
for i = 1:elems_num-1
    fprintf(fileID,'%d %d\n', elems(i,:)-1);
end
fprintf(fileID,'%d %d</DataArray>\n', elems(end,:)-1);

fprintf(fileID,'<DataArray Name="types" Format="ascii" type="Int32">');
for i = 1:elems_num-1
    fprintf(fileID,'3\n');
end
fprintf(fileID,'3</DataArray>\n');

fprintf(fileID,'<DataArray Name="offsets" type="Int32" Format="ascii">');
for i = 1:elems_num-1
    fprintf(fileID,'%d\n',i*2);
end
fprintf(fileID,'%d</DataArray>\n', elems_num*2);
fprintf(fileID,'</Cells>\n');


fprintf(fileID,'</Piece>\n');
fprintf(fileID,'</UnstructuredGrid>\n');
fprintf(fileID,'</VTKFile>\n');

fprintf('Wrote successfully Paraview mesh file: %s\n',output_meshfile);

% Close output file
fclose(fileID);


end










