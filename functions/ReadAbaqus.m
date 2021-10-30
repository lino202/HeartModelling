function [nodes, elems, node_sets, cell_sets] = ReadAbaqus(inp_file)
%READABAQUS Summary of this function goes here
%   Detailed explanation goes here

% Check filepath's extension
[~, ~, ext] = fileparts(inp_file);
if (~strcmp(ext,'.inp'))
    error('Abaqus mesh filename should have .inp extension');
end


% Open the file to count nodes and elements
fid=fopen(inp_file, 'rt');
if (fid == -1), error(['Error openning the mesh file: ',inp_file]); end

ln = fgets(fid);
nodes_num = 0;
elems_num = 0;
while ischar(ln)
    
    if(contains(ln,'*Node'))
        ln = fgets(fid);
        node_dims = count(ln,' ');
        while (~contains(ln,'*'))
            nodes_num = nodes_num+1;           
            ln = fgets(fid);
        end  
    end
    
    if(contains(ln,'*Element'))        
        ln = fgets(fid);
        elem_dims = count(ln,' ');
        while (~contains(ln,'*'))
            elems_num = elems_num+1;
            ln = fgets(fid);   
        end
    end
    
    ln = fgets(fid);
    
    if nodes_num > 0 && elems_num > 0
        break;
    end
end
fclose(fid);

nodes = zeros(nodes_num, node_dims);
elems = zeros(elems_num, elem_dims);
node_sets = {};

if node_dims == 1
    node_strformat = '%f, %f\n';
elseif node_dims == 2
    node_strformat = '%f, %f, %f\n';
elseif node_dims == 3
    node_strformat = '%f, %f, %f, %f\n';
else
    error('Unknown node dimension');
end

if elem_dims == 2
    elem_strformat = '%d, %d, %d\n';
elseif elem_dims == 3
    elem_strformat = '%d, %d, %d, %d\n';
elseif elem_dims == 4
    elem_strformat = '%d, %d, %d, %d, %d\n';
elseif elem_dims == 8
    elem_strformat = '%d, %d, %d, %d, %d, %d, %d, %d, %d\n';
else
    error('Unknown element type');
end


% open again file for processing
fid=fopen(inp_file, 'rt');
ln = fgets(fid);
nid = 1; elid = 1; nsetid = 1; csetid = 1;
node_sets = []; cell_sets = [];
while ischar(ln)
    if(contains(ln,'*Node'))
        ln = fgets(fid);
        while (~contains(ln,'*'))
            A = sscanf(ln, node_strformat);
            nodes(nid,:) = A(2:end);
            nid = nid+1;
            ln = fgets(fid);
        end
    end
    
    if(contains(ln,'*Element'))       
        ln = fgets(fid);
        while (~contains(ln,'*'))
            B = sscanf(ln, elem_strformat);
            elems(elid,:) = B(2:end);
            elid = elid+1;
            ln = fgets(fid);   
        end
    end
    
    if(contains(ln,'*Nset'))
        nset_name = extractAfter(ln, "=");
        nset_nodes = [];
        
        ln = fgets(fid);
        while (~contains(ln,'*'))
            ln = strrep(ln, ',', '');
            nums = textscan(ln,'%d');
            nset_nodes = [nset_nodes ; nums{1}];
            ln = fgets(fid);       
        end
        
        node_sets{nsetid} = {nset_nodes,nset_name(1:(end-1))};
        nsetid = nsetid+1;
    end
    
    if(contains(ln,'*Elset'))
        cset_name = extractAfter(ln, "=");
        cset_elems = [];
        
        ln = fgets(fid);
        while (~contains(ln,'*'))
            ln = strrep(ln, ',', '');
            nums = textscan(ln,'%d');
            cset_elems = [cset_elems; nums{1}];
            ln = fgets(fid);       
        end
        
        cell_sets{csetid} = {cset_elems,cset_name(1:(end-1))};
        csetid = csetid+1;
    end
    
    if(~contains(ln,'*Nset') && ~contains(ln,'*Elset'))
        ln = fgets(fid);
    end
end

if sum(size(node_sets)) > 0
    node_sets = node_sets(~cellfun('isempty',node_sets));
end

if sum(size(cell_sets)) > 0
    cell_sets = cell_sets(~cellfun('isempty',cell_sets));
end

fclose(fid);

end

