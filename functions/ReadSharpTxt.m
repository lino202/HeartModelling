function data = ReadSurfVtk(filename)
%READ .txt files with # shaprs in the headers and continues data of one
%number
% Check filepath's extension
[~, ~, ext] = fileparts(filename);
if (~strcmp(ext,'.txt'))
    error('Given filename should have .vtk extension');
end

% Open the file
fid=fopen(filename, 'rt');
if (fid == -1), error(['Error openning the mesh file: ',filename]); end

data = zeros(1);
while 1    
    
    ln = fgets(fid);
    if ln == -1
        break
    elseif (contains(ln,'#'))
        continue
    else
        data = [data str2double(ln)];

    end

end
data(1)=[];
data = data';
fclose(fid);

end

