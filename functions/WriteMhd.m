function WriteMhd(mhd_filename, img)

% construct file names
raw_filename = strcat(mhd_filename(1:end-4), '.raw');

% write mhd file
fid=fopen(mhd_filename, 'w');
assert(fid>0,'Impossible to open file %s\n', mhd_filename);

fprintf(fid,'ObjectType = Image\n');
fprintf(fid,'NDims = %s\n', img.metaData.dimension);
fprintf(fid,'BinaryData = True\n');
fprintf(fid,'BinaryDataByteOrderMSB = False\n');
fprintf(fid,'CompressedData = False\n');
fprintf(fid,'TransformMatrix = 1 0 0 0 1 0 0 0 1\n');

% Get origin
orig = textscan(img.metaData.space_origin,'(%f,%f,%f)');
tX = orig{1};
tY = orig{2};
tZ = orig{3};
fprintf(fid,'Offset = %f %f %f\n',tX,tY,tZ);

fprintf(fid,'CenterOfRotation = 0 0 0\n');
fprintf(fid,'AnatomicalOrientation = %s\n',getOrientation(img.metaData.space));

% Get spacing
dirs = split(img.metaData.space_directions);
dirX = textscan(dirs{1},'(%f,%f,%f)');
dirY = textscan(dirs{2},'(%f,%f,%f)');
dirZ = textscan(dirs{3},'(%f,%f,%f)');
sX = dirX{1};
sY = dirY{2};
sZ = dirZ{3};
fprintf(fid,'ElementSpacing = %f %f %f\n',sX,sY,sZ);

% Get dimensions
[nX,nY,nZ] = size(img.pixelData);
fprintf(fid,'DimSize = %d %d %d\n',nX,nY,nZ);

fprintf(fid, 'ElementType = %s\n',getDataType(class(img.pixelData)));
[~,name]=fileparts(mhd_filename);
fprintf(fid, 'ElementDataFile = %s\n', strcat(name, '.raw'));
fclose(fid);


% write raw file
fid=fopen(raw_filename, 'w');
assert(fid>0, 'Impossible to open file %s\n', raw_filename);

fwrite(fid, img.pixelData, class(img.pixelData));
fclose(fid);

end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function orientation = getOrientation(space)
   switch (space)
   case {'left-posterior-superior'}
    orientation = 'LPS'; 
   case {'right-anterior-inferior'}
    orientation = 'RAI'; 
   otherwise
    assert(false, 'Unsupported Matlab data type')
  end

end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function dataType = getDataType(matlabType)
% Determine the metadata type from the Matlab type
  switch (matlabType)
   case {'int8'}
    dataType = 'MET_CHAR';  
   case {'uint8'}
    dataType = 'MET_UCHAR'; 
   case {'int16'}
    dataType = 'MET_SHORT'; 
   case {'uint16'}
    dataType = 'MET_USHORT'; 
   case {'int32'}
    dataType = 'MET_INT';
   case {'uint32'}
    dataType = 'MET_UINT'; 
   case {'single'}
    dataType = 'MET_FLOAT';
   case {'double'}
    dataType = 'MET_DOUBLE'; 
   otherwise
    assert(false, 'Unsupported Matlab data type')
  end
end