function selection = ReadVtkCellSelection(filename)

format long g;

% Check filepath's extension
[~, ~, ext] = fileparts(filename);
if (~strcmp(ext,'.vtk'))
    error('Selection filename should have .vtk extension');
end

% Open the file to count nodes and elements
fid=fopen(filename, 'rt');
assert(fid > 0, 'Could not open file.');

while ~feof(fid)
    ln = fgetl(fid);
    
    % Read nodes
    if contains(ln,'vtkOriginalCellIds')
        str = split(ln);
        cell_num = str2num(str{3});
        selection = zeros(cell_num,1);
        ln = fgetl(fid);
        i = 1;
        while ~contains(ln,'POINT_DATA')
            % Convert indices line to numbers
            a = str2num(ln);
            % Assign indices to selection cell
            for k=1:size(a,2)
                selection(i) = a(k)+1;
                i = i+1;
            end
            
            % Read next coordinates line
            ln = fgetl(fid);
        end
    end
end


fclose(fid);


end

