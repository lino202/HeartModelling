function [newnodes,newcells] = ReorderMesh(nodes,cells)
%SURFMESHPARTITION Summary of this function goes here
%   Detailed explanation goes here

nids = unique(cells);
nodemapflags = zeros(size(nodes,1),1);
nodemapflags(nids) = 1:size(nids,1);

newnodes = nodes(nids,:);

newcells = zeros(size(cells));
for i = 1:size(newcells,1)
    newcells(i,:) = nodemapflags(cells(i,:));
end



end

