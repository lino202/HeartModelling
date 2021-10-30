function faces = Extract3dCellFaces(cells)
%% Extract3dCellFaces - Extract the faces of a 3D mesh solid mesh
%
% Input:
%   cells     - The mesh cells
%
% Output:
%   faces     - The mesh faces
%%

%% ELECTRA software - MatLAB implementation - v0.1.0
%  Software for the solution of the monodomain model
%  for cardiac electrophysiology simulation using
%  the Finite Elements method.
%
%  version: 0.1.0
%  licence: GPL v.3 [see LICENCE.txt for information]
%  author:  Konstantinos A. Mountris
%  contact: konstantinos.mountris@gmail.com
%%

[cells_num, cells_dim] = size(cells);  

if (cells_dim == 4)
    fc = [1 2 4
          1 3 2
          2 3 4
          1 4 3];
    faces = zeros(4*cells_num, 3);
    pad = 4;
elseif (cells_dim == 8)
    fc = [1 4 3 2
          5 6 7 8
          1 2 6 5
          4 8 7 3
          1 5 8 4
          2 3 7 6];
    faces = zeros(6*cells_num, 4);
    pad = 6;
end
    

poz = 1;
for kk = 1:cells_num
    el = cells(kk,:);                % get the element 
    faces(poz:poz+pad-1,:) = el(fc);    % get the faces of this element
    poz = poz + pad;
end


end