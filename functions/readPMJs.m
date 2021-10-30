
function [A] = readPMJs(filename)
%READPMJS Summary of this function goes here
%   Detailed explanation goes here


% Open the file
fid=fopen(filename, 'rt');
if (fid == -1), error(['Error openning the file: ',filename]); end

A = {};
ln = fgetl(fid);
i = 1;
while ischar(ln)
    if (sum(size(ln)) > 0)
        A{i} = str2double(strsplit(ln(1:end-1))) + 1;
        i = i+1;
    end
    ln = fgetl(fid);
end
fclose(fid);


end

