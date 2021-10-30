function WriteNrrdDwi(outputFilename, img)
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
fprintf(fid,'NRRD0005\n');
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
fprintf(fid,'measurement frame: %s\n',img.metaData.measurement_frame);
fprintf(fid,'DICOM_0008_0060_Modality:=%s\n',img.metaData.DICOM_0008_0060_Modality);
fprintf(fid,'DICOM_0008_0070_Manufacturer:=%s\n',img.metaData.DICOM_0008_0070_Manufacturer);
fprintf(fid,'DICOM_0008_1090_ManufacturerModelName:=%s\n',img.metaData.DICOM_0008_1090_ManufacturerModelName);
fprintf(fid,'DICOM_0018_0022_ScanOptions:=%s\n',img.metaData.DICOM_0018_0022_ScanOptions);
fprintf(fid,'DICOM_0018_0023_MRAcquisitionType:=%s\n',img.metaData.DICOM_0018_0023_MRAcquisitionType);
fprintf(fid,'DICOM_0018_0080_RepetitionTime:=%s\n',img.metaData.DICOM_0018_0080_RepetitionTime);
fprintf(fid,'DICOM_0018_0081_EchoTime:=%s\n',img.metaData.DICOM_0018_0081_EchoTime);
fprintf(fid,'DICOM_0018_0083_NumberOfAverages:=%s\n',img.metaData.DICOM_0018_0083_NumberOfAverages);
fprintf(fid,'DICOM_0018_0087_MagneticFieldStrength:=%s\n',img.metaData.DICOM_0018_0087_MagneticFieldStrength);
fprintf(fid,'DICOM_0018_1020_SoftwareVersions:=%s\n',img.metaData.DICOM_0018_1020_SoftwareVersions);
fprintf(fid,'DICOM_0018_1314_FlipAngle:=%s\n',img.metaData.DICOM_0018_1314_FlipAngle);
fprintf(fid,'DWMRI_b-value:=%s\n',img.metaData.DWMRI_b_value);

fprintf(fid,'DWMRI_gradient_0000:=%s\n',img.metaData.DWMRI_gradient_0000);
fprintf(fid,'DWMRI_gradient_0001:=%s\n',img.metaData.DWMRI_gradient_0001);
fprintf(fid,'DWMRI_gradient_0002:=%s\n',img.metaData.DWMRI_gradient_0002);
fprintf(fid,'DWMRI_gradient_0003:=%s\n',img.metaData.DWMRI_gradient_0003);
fprintf(fid,'DWMRI_gradient_0004:=%s\n',img.metaData.DWMRI_gradient_0004);
fprintf(fid,'DWMRI_gradient_0005:=%s\n',img.metaData.DWMRI_gradient_0005);
fprintf(fid,'DWMRI_gradient_0006:=%s\n',img.metaData.DWMRI_gradient_0006);
fprintf(fid,'DWMRI_gradient_0007:=%s\n',img.metaData.DWMRI_gradient_0007);
fprintf(fid,'DWMRI_gradient_0008:=%s\n',img.metaData.DWMRI_gradient_0008);
fprintf(fid,'DWMRI_gradient_0009:=%s\n',img.metaData.DWMRI_gradient_0009);
fprintf(fid,'DWMRI_gradient_0010:=%s\n',img.metaData.DWMRI_gradient_0010);
fprintf(fid,'DWMRI_gradient_0011:=%s\n',img.metaData.DWMRI_gradient_0011);
fprintf(fid,'DWMRI_gradient_0012:=%s\n',img.metaData.DWMRI_gradient_0012);
fprintf(fid,'DWMRI_gradient_0013:=%s\n',img.metaData.DWMRI_gradient_0013);
fprintf(fid,'DWMRI_gradient_0014:=%s\n',img.metaData.DWMRI_gradient_0014);
fprintf(fid,'DWMRI_gradient_0015:=%s\n',img.metaData.DWMRI_gradient_0015);
fprintf(fid,'DWMRI_gradient_0016:=%s\n',img.metaData.DWMRI_gradient_0016);
fprintf(fid,'modality:=%s\n',img.metaData.modality);
fprintf(fid,'\n');
fwrite(fid, img.pixelData, class(img.pixelData));
fclose('all');

end
