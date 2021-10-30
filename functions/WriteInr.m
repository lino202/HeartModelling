function WriteInr(outputFilename, img)

% Open file for writing
fid=fopen(outputFilename, 'w');
if(fid<=0) 
  fprintf('Could not open file: %s\n', outputFilename);
end

[~, ~, ext] = fileparts(outputFilename);
if (~strcmp(ext,'.inr'))
    error('File should have .inr extension');
end

% Image dimensions
[nX,nY,nZ] = size(img.pixelData);

% Voxel size
dirs = split(img.metaData.space_directions);
dirX = textscan(dirs{1},'(%f,%f,%f)');
dirY = textscan(dirs{2},'(%f,%f,%f)');
dirZ = textscan(dirs{3},'(%f,%f,%f)');
vX = dirX{1};
vY = dirY{2};
vZ = dirZ{3};

% Image origin
orig = textscan(img.metaData.space_origin,'(%f,%f,%f)');
tX = orig{1};
tY = orig{2};
tZ = orig{3};

% Data type and voxel bits
[data_type, voxelbits] = getDataVoxelTypes(class(img.pixelData));

% Create header line
s1  = sprintf('#INRIMAGE-4#{\n');
s2  = sprintf('XDIM=%d\n',nX);
s3  = sprintf('YDIM=%d\n',nY);
s4  = sprintf('ZDIM=%d\n',nZ);
s5  = sprintf('VDIM=1\n');
s6  = sprintf('TYPE=%s\n',data_type);
s7  = sprintf('PIXSIZE=%s\n',voxelbits);
s8  = sprintf('CPU=decm\n');
s9  = sprintf('VX=%f\n',vX);
s10 = sprintf('VY=%f\n',vY);
s11 = sprintf('VZ=%f\n',vZ);
s12 = sprintf('TX=%f\n',tX);
s13 = sprintf('TY=%f\n',tY);
s14 = sprintf('TZ=%f\n',tZ);

% Write header
fprintf(fid,s1);
fprintf(fid,s2);
fprintf(fid,s3);
fprintf(fid,s4);
fprintf(fid,s5);
fprintf(fid,s6);
fprintf(fid,s7);
fprintf(fid,s8);
fprintf(fid,s9);
fprintf(fid,s10);
fprintf(fid,s11);
fprintf(fid,s12);
fprintf(fid,s13);
fprintf(fid,s14);

hdrSize = length(s1)+length(s2)+length(s3)+length(s4)+length(s5)+length(s6)+...
    length(s7)+length(s8)+length(s9)+length(s10)+length(s11)+length(s12)+length(s13)+...
    length(s14);

% Add new line chars to fill the total amount of header chars
rest = 252-hdrSize;
for i=1:rest
    fprintf(fid,'\n');
end
fprintf(fid,'##}\n');

% Write the image data
fwrite(fid, img.pixelData, class(img.pixelData));
fclose('all');

end



function [dataType, voxelBit] = getDataVoxelTypes(matlabType)
% Determine the metadata type from the Matlab type
  switch (matlabType)
   case {'int8'}
    dataType = 'signed fixed';
    voxelBit = '8 bits';  
   case {'uint8'}
    dataType = 'unsigned fixed';
    voxelBit = '8 bits';  
   case {'int16'}
    dataType = 'signed fixed';
    voxelBit = '16 bits'; 
   case {'uint16'}
    dataType = 'unsigned fixed';
    voxelBit = '16 bits'; 
   case {'int32'}
    dataType = 'signed fixed';
    voxelBit = '32 bits'; 
   case {'uint32'}
    dataType = 'unsigned fixed';
    voxelBit = '32 bits'; 
   case {'int64'}
    dataType = 'signed fixed';
    voxelBit = '64 bits'; 
   case {'uint64'}
    dataType = 'unsigned fixed';
    voxelBit = '64 bits'; 
   case {'single'}
    dataType = 'float';
    voxelBit = '32 bits'; 
   case {'double'}
    dataType = 'float';
    voxelBit = '64 bits'; 
   otherwise
    assert(false, 'Unsupported Matlab data type')
  end
end
