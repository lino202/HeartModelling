function ShowEdges(nodes, edges, width, plot_opt)
%SHOW   PLots the selected edges of a 2D mesh.

if nargin<4, plot_opt = 'r-'; end
if nargin<3, width = 2; end

[nnum, ndim] = size(nodes);
if ndim < 3, nodes = [nodes zeros(nnum,3-ndim)]; end
    
for e = 1:size(edges,1)
    X = nodes(edges(e,:),1)';
    Y = nodes(edges(e,:),2)';
    Z = nodes(edges(e,:),3)';
    plot3(X, Y, Z, plot_opt, 'LineWidth', width)
end
    
%     plot([ nodes(edges(:,1),1) nodes(edges(:,2),1)], ...
%       [nodes(edges(:,1),2) nodes(edges(:,2),2)], ...
%       plot_opt, 'LineWidth', width)