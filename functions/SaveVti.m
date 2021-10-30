function [] = SaveVti(vti_output, image_data, spacing, origin, dataname, datatype)
%SAVEEMBGRIDTOVTK Summary of this function goes here
%   Detailed explanation goes here

% Check filepath's extension
[~, ~, ext] = fileparts(vti_output);
if (~strcmp(ext,'.vti'))
    error('Filename should have .vti extension');
end

imageDims = size(image_data);
dimx = imageDims(1);
dimy = imageDims(2); 
dimz = imageDims(3);

dx = spacing(1);
dy = spacing(2);
dz = spacing(3);

ox = origin(1);
oy = origin(2);
oz = origin(3);

% Open output file and write header
fID = fopen(vti_output,'w');
fprintf('Writing to VTI file: %s ...',vti_output);
fprintf(fID,'<?xml version="1.0"?>\n');
fprintf(fID,'<VTKFile type="ImageData" version="0.1" byte_order="LittleEndian">\n');
fprintf(fID,'<ImageData WholeExtent="0 %d 0 %d 0 %d" Origin="%f %f %f" Spacing="%d %d %d">\n',dimx,dimy,dimz,ox,oy,oz,dx,dy,dz);
fprintf(fID,'<Piece Extent="0 %d 0 %d 0 %d">\n',dimx,dimy,dimz);
fprintf(fID,'<CellData Scalars="%s">\n',dataname);
fprintf(fID,'<DataArray type="%s" Name="%s" format="ascii">\n',datatype,dataname);

cnt = 0;
for k=1:dimz
    for j=1:dimy
        for i=1:dimx
            fprintf(fID,'%f',image_data(i,j,k));
            cnt = cnt+1;
            if cnt == 20 || (i==dimx && j==dimy && k==dimz)
                fprintf(fID,'\n');
                cnt = 0;
            else
                fprintf(fID,' ');
            end
        end
    end
end
            
fprintf(fID,'</DataArray>\n');
fprintf(fID,'</CellData>\n');
fprintf(fID,'</Piece>\n');
fprintf(fID,'</ImageData>\n');
fprintf(fID,'</VTKFile>\n');


% Close output file
fclose(fID);

fprintf(' DONE\n');

end

