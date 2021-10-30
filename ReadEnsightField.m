function [ field ] = ReadEnsightField(field_file)
%READENSIGHTFIELD Summary of this function goes here
%   Detailed explanation goes here

fid=fopen(field_file, 'rt');
if (fid == -1), error(['Error openning the file: ',field_file]); end

field = [];

% Skip header lines
ln = fgets(fid);
ln = fgets(fid);
ln = fgets(fid);
ln = fgets(fid);

while ischar(ln)
    A = sscanf(ln, '%f\n');
    field = [field ; A];
    ln = fgets(fid);
end 
fclose(fid);

end

