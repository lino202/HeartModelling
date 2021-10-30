function [] = DrawFace(fnodes, color, alpha)
%DRAWTRI Summary of this function goes here
%   Detailed explanation goes here

face = 1:size(fnodes,1);
     
color_mat = repmat(color,size(fnodes,1),1);
patch('Vertices',fnodes,'Faces',face,'FaceColor','flat', ...
    'FaceVertexCData', color_mat,'facealpha',alpha);

end

