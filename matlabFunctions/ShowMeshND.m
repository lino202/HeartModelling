function ShowMeshND(nodes, cells, color_mat)
%% ShowMeshND - Show a mesh in N dimensions (N = 1, 2, 3)
%
% Input:
%   nodes     - The mesh nodes
%   cells     - The mesh cells
%   color_mat - The display color. Given as a [nc x N] matrix with nc =
%               number of cells
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

[nodes_num, node_dims]  = size(nodes);

if (node_dims == 1)
    % Set default color.
    if nargin<3, color_mat = repmat([1 0 0],size(cells,1),1); end

    nodes = [nodes, zeros(nodes_num,1)]; 
    patch('Vertices',nodes,'Faces',cells,'FaceColor','flat', 'FaceVertexCData', color_mat);
    hold on
    plot(nodes(:,1),nodes(:,2),'ro','MarkerSize',6,'MarkerFaceColor','k');
    hold off
elseif (node_dims == 2)
    % Set default color.
    if nargin<3, color_mat = repmat([1 0 0],size(cells,1),1); end
    
    patch('Vertices',nodes,'Faces',cells,'FaceColor','flat', 'FaceVertexCData', color_mat);
elseif (node_dims == 3)
    faces = Extract3dCellFaces(cells);
    
    % Set default color.
    if nargin<3, color_mat = repmat([1 0 0],size(faces,1),1); end
    
    patch('Vertices',nodes,'Faces',faces,'FaceColor','flat', 'FaceVertexCData', color_mat);
end

end