function [nodes, fields] = ReadVtkPoints(filename)

format long g;

% Check filepath's extension
[~, ~, ext] = fileparts(filename);
if (~strcmp(ext,'.vtk'))
    error('Paraview mesh filename should have .vtk extension');
end

% Open the file to count nodes and elements
fid=fopen(filename, 'rt');
if (fid == -1), error(['Error openning the mesh file: ',filename]); end

while ~feof(fid)
    ln = fgetl(fid);
    
    % Read nodes
    if contains(ln,'POINTS')
        str = split(ln);
        nodes_num = str2num(str{2});
        nodes = zeros(nodes_num,3);
        ln = fgetl(fid);
        i = 1; j = 1;
        while ~contains(ln,'POLYGONS') && ~contains(ln,'CELLS') 
            % Convert coordinates line to numbers
            a = str2num(ln);
            % Assign coordinates to nodes
            for k=1:size(a,2)
                nodes(i,j) = a(k);
                if j == 3
                    i = i+1;
                    j = 1;
                else
                    j = j+1;
                end
            end
            
            % Read next coordinates line
            ln = fgetl(fid);
        end
    end
    
    % Read fields
    if contains(ln,'POINT_DATA')
        ln = fgets(fid);
        temp = split(ln);
        
        if isempty(temp{end})
            fields_num = str2num(temp{end-1});
        else
            fields_num = str2num(temp{end});
        end
        
        fields = cell(fields_num,1);
        
        for ff=1:fields_num
           while ~contains(ln,num2str(size(nodes,1)))
               ln = fgets(fid);
           end
           
           temp = split(ln);
           field_name = temp{1};
           field_dims = str2num(temp{2});
           if field_dims == 1
               data_format = '%f\n';
           elseif field_dims == 2
               data_format = '%f %f\n';
           elseif field_dims == 3
               data_format = '%f %f %f\n';
           end
           field_data = zeros(size(nodes,1),field_dims);
           for n=1:size(nodes,1)
               ln = fgets(fid);
               field_data(n,:) = sscanf(ln, data_format);
           end
           
           fields{ff} = {field_data,field_name};
            
        end
    end
end


fclose(fid);


end

