function [node_ids] = ReadBundleNodes(filename)
%READSURFOBJ Summary of this function goes here
%   Detailed explanation goes here

% Check filepath's extension
[~, ~, ext] = fileparts(filename);
if (~strcmp(ext,'.txt'))
    error('Given filename should have .txt extension');
end

% Open the file
fid=fopen(filename, 'rt');
if (fid == -1), error(['Error openning the file: ',filename]); end

% Skip the 3 lines header 
ln = fgets(fid);
ln = fgets(fid);
ln = fgets(fid);

node_ids = fscanf(fid,'%d\n',[1, inf])'+1;

fclose(fid);

end

