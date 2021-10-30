function [nodes, elems, end_nodes] = ReadPurkinjeVtu(filename)

% Check filepath's extension
[~, ~, ext] = fileparts(filename);
if (~strcmp(ext,'.vtu'))
    error('Paraview mesh filename should have .vtu extension');
end


% Open the file to count nodes and elements
fid=fopen(filename, 'rt');
if (fid == -1), error(['Error openning the mesh file: ',filename]); end

% Move to third line to read nodes and elements number
ln = fgets(fid); ln = fgets(fid); ln = fgets(fid);

str1 = extractBetween(ln,'Points="','"');
str2 = extractBetween(ln,'Cells="','"');

nodes_num = str2num(str1{1});
elems_num = str2num(str2{1});

nodes = zeros(nodes_num,3);
elems = zeros(elems_num,2);

% Get nodes
ln = fgets(fid); ln = fgets(fid);
nodes(1,:) = str2num(extractAfter(ln,'>'));
for i = 2:nodes_num-1
    ln = fgets(fid);
    nodes(i,:) = str2num(ln);
end
ln = fgets(fid);
nodes(end,:) = str2num(extractBefore(ln,'<'));

% Get elements
ln = fgets(fid); ln = fgets(fid); ln = fgets(fid);
elems(1,:) = str2num(extractAfter(ln,'>'))+1;
for i = 2:elems_num-1
    ln = fgets(fid);
    elems(i,:) = str2num(ln)+1;
end
ln = fgets(fid);
elems(end,:) = str2num(extractBefore(ln,'<'))+1;

fclose(fid);

% Get end nodes
end_flag = zeros(nodes_num,1);
for i = 1:nodes_num
    if length(find(elems==i)) == 1
        end_flag(i) = 1;
    end
end
end_nodes = find(end_flag==1);


end

