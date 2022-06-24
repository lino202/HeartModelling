function [] = SavePolyhedraVtu(output, points, faces, cells, field_data, nsets)
%SAVEEMBGRIDTOVTK Summary of this function goes here
%   Detailed explanation goes here

if nargin < 5, nsets = {}; end
if nargin < 4, field_data = {}; end

% Check filepath's extension
[~, ~, ext] = fileparts(output);
if (~strcmp(ext,'.vtu'))
    error('Filename should have .vtu extension');
end

% Check nodes and elems format
pointnum = length(points);
cellnum = length(cells);
facenum = length(faces);


% Open output file and write header
format long g;
fID = fopen(output,'w');

fprintf('Writing to VTU file: %s ...',output);
fprintf(fID,'<?xml version="1.0"?>\n');
fprintf(fID,'<VTKFile type="UnstructuredGrid" version="0.1" byte_order="LittleEndian">\n');
fprintf(fID,'<UnstructuredGrid>\n');
fprintf(fID,'<Piece NumberOfPoints="%d" NumberOfCells="%d">\n',pointnum,cellnum);
fprintf(fID,'<Points>\n');
fprintf(fID,'<DataArray type="Float32" Name="Points" NumberOfComponents="3" format="ascii">\n');
for nn = 1:pointnum
    fprintf(fID,'%10.15f %10.15f %10.15f\n', points(nn,:));
end
fprintf(fID,'</DataArray>\n');
fprintf(fID,'</Points>\n');


cell_offsets = zeros(cellnum,1);
fprintf(fID,'<Cells>\n');
fprintf(fID,'<DataArray type="Int64" Name="connectivity" format="ascii">\n');
for cc = 1:cellnum
    if cc == 1
        cell_offsets(cc) = length(cells{cc});
    else
        cell_offsets(cc) = cell_offsets(cc-1) + length(cells{cc});
    end
    
    fprintf(fID,'%d',cells{cc}(1)-1);
    for i = 2:length(cells{cc})
        fprintf(fID,' %d',cells{cc}(i)-1);
    end
    fprintf(fID,'\n');
end
fprintf(fID,'</DataArray>\n');
fprintf(fID,'<DataArray type="Int64" Name="offsets" format="ascii">\n');
for cc = 1:cellnum
    fprintf(fID,'%d\n',cell_offsets(cc));
end
fprintf(fID,'</DataArray>\n');
fprintf(fID,'<DataArray type="UInt8" Name="types" format="ascii">\n');
for cc = 1:cellnum
    fprintf(fID,'42\n');
end

face_offsets = zeros(cellnum,1);
fprintf(fID,'</DataArray>\n');
fprintf(fID,'<DataArray type="Int64" IdType="1" Name="faces" format="ascii">\n');
for cc = 1:cellnum
    face_offsets(cc) = 1;
    if cc > 1
            face_offsets(cc) = face_offsets(cc) + face_offsets(cc-1);
    end
    fprintf(fID,'%d\n', length(cells{cc}));
    
    for i = 1:length(cells{cc})
        ff = cells{cc}(i);
        face_offsets(cc) = face_offsets(cc) + length(faces{ff}) + 1;
        fprintf(fID,'%d %d', length(faces{ff}), faces{ff}(1)-1);
        for j = 2:length(faces{ff})
            fprintf(fID,' %d', faces{ff}(j)-1);
        end
        fprintf(fID,'\n');
    end
end
fprintf(fID,'</DataArray>\n');
fprintf(fID,'<DataArray type="Int64" IdType="1" Name="faceoffsets" format="ascii">\n');
for cc = 1:cellnum
    fprintf(fID,'%d\n',face_offsets(cc));
end
fprintf(fID,'</DataArray>\n');
fprintf(fID,'</Cells>\n');
fprintf(fID,'</Piece>\n');
fprintf(fID,'</UnstructuredGrid>\n');
fprintf(fID,'</VTKFile>\n');


% nsets_num = 0;
% if ~isempty(field_data), nsets_num = nsets_num+size(field_data,2); end
% if ~isempty(nsets), nsets_num = nsets_num+size(nsets,2); end
% if nsets_num ~= 0
%     fprintf(fileID,'POINT_DATA %d\n', pnum);
%     fprintf(fileID,'FIELD FieldData %d\n', nsets_num);
% end
% 
% if ~isempty(field_data)
%     for i=1:size(field_data,2)
%         field_dims = size(field_data{i}{1},2);
%         if field_dims == 1
%             field_format = '%10.15f\n';
%         elseif field_dims == 2
%             field_format = '%10.15f %10.15f\n';
%         elseif field_dims == 3
%             field_format = '%10.15f %10.15f %10.15f\n';
%         end
%         fprintf(fileID,'%s %d %d double\n', field_data{i}{2}, field_dims, pnum);
%         for nn = 1:pnum
%             fprintf(fileID,field_format, field_data{i}{1}(nn,:));
%         end
%         fprintf(fileID,'\n');  
%     end
% end
% 
% if ~isempty(nsets)
%     for i=1:size(nsets,2)
%         
%         fprintf(fileID,'%s 1 %d int\n', nsets{i}{2}, pnum);
%         flag = zeros(pnum,1);
%         flag(nsets{i}{1}) = 1;
%         for nn = 1:pnum
%             fprintf(fileID,'%d\n',flag(nn));
%         end
%         fprintf(fileID,'\n');  
%     end
% end


% Close output file
fclose(fID);

fprintf(' DONE\n');

end