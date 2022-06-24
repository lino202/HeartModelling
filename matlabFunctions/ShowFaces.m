function ShowFaces(nodes, faces, color_mat, alpha)
%SHOW   PLots the selected faces of a 3D mesh.

if nargin<4, alpha=1; end
if nargin<3, color_mat = repmat([1 0 0],size(faces,1),1); end

patch('Vertices',nodes,'Faces',faces,'FaceColor','flat', ...
      'FaceVertexCData', color_mat,'facealpha',alpha);

end