function [] = SaveEnsightField(field_file, field)
%READENSIGHTFIELD Summary of this function goes here
%   Detailed explanation goes here

[~, ~, ext] = fileparts(field_file);
if (~strcmp(ext,'.ens'))
    error('File should have .ens extension');
end

fid=fopen(field_file, 'w');
if (fid == -1), error(['Error openning the file: ',field_file]); end

fprintf(fid,'Ensight Model Post Process\npart\n  1\ncoordinates\n');

n = size(field,1);

for i = 1:n
    if(isnan(field(i)))
        fprintf(fid,'nan\n');
    else
        fprintf(fid,'%f\n', field(i));
    end
end

fclose(fid);

end

