function WriteNrrdDti(outputFilename, img)
% Write image and metadata to a NRRD file (see http://teem.sourceforge.net/nrrd/format.html)
%   img.pixelData: pixel data array
%   img.ijkToLpsTransform: pixel (IJK) to physical (LPS, assuming 'space' is 'left-posterior-superior')
%     coordinate system transformation, the origin of the IJK coordinate system is (1,1,1) to match Matlab matrix indexing
%   img.metaData: Contains all the descriptive information in the image header. The following fields are ignored:
%     sizes: computed to match size of img.pixelData
%     type: computed to match type of img.pixelData
%     kinds: computed to match dimension of img.pixelData
%     dimension: computed to match dimension of img.pixelData
%     space_directions: ignored if img.ijkToLpsTransform is defined
%     space_origin: ignored if img.ijkToLpsTransform is defined
%   img.metaData: Contains the list of full NRRD field names for each
%     metaData field name. All fields should be listed here that have a
%     special character in their name (such as dot or space).
%   img.metaDataFieldNames: Contains full names of metadata fields that cannot be used as Matlab field names because they contains
%     special characters (space, dot, etc). Full field names are used for determining the field name to be used in the NRRD file
%     from the Matlab metadata field name.
%
% Supports writing of 3D and 4D volumes.
% 2D pixelData is written as single-slice 3D volume.
%
% Examples:
%
% 1. Using output from nrrdread: 
%
%   img = nrrdread('testData\MRHeadRot.nrrd')
%   nrrdwrite('testOutput.nrrd', img)
%    
% 2. Creating volume from scratch - minimal example
%
%   [x,y,z] = meshgrid([-10:10],[-12:15],[-8:6]);
%   img.pixelData = x/3+y/4+z/2;
%
%   nrrdwrite('testOutput.nrrd', img);
%  
% 3. Creating volume from scratch
%
%   % Set pixel data
%   [x,y,z] = meshgrid([-10:10],[-12:15],[-8:6]);
%   img.pixelData = x/3+y/4+z/2;
%
%   % Define origin, spacing, axis directions by a homogeneous transformation matrix:
%   img.ijkToLpsTransform = [ 1.2 0 0 10; 0 1.2 0 12; 0 0 3.0 -22; 0 0 0 1];
%
%   % Enable compression
%   img.metaData.encoding='gzip';
%
%   nrrdwrite('testOutput.nrrd', img);
%

% Open file for writing
fid=fopen(outputFilename, 'w');
if(fid<=0) 
  fprintf('Could not open file: %s\n', outputFilename);
end


% Write header
fprintf(fid,'NRRD0004\n');
fprintf(fid,'# Complete NRRD file format specification at:\n');
fprintf(fid,'# http://teem.sourceforge.net/nrrd/format.html\n');

% Write 
fprintf(fid,'type: %s\n',img.metaData.type);
fprintf(fid,'dimension: %s\n',img.metaData.dimension);
fprintf(fid,'space: %s\n',img.metaData.space);
fprintf(fid,'sizes: %s\n',img.metaData.sizes);
fprintf(fid,'space directions: %s\n',img.metaData.space_directions);
fprintf(fid,'kinds: %s\n',img.metaData.kinds);
fprintf(fid,'endian: %s\n',img.metaData.endian);
fprintf(fid,'encoding: %s\n',img.metaData.encoding);
fprintf(fid,'space origin: %s\n',img.metaData.space_origin);
fprintf(fid,'\n');
fwrite(fid, img.pixelData, class(img.pixelData));
fclose('all');

end
