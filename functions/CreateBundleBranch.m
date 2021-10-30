function [branch] = CreateBundleBranch(endo_nodes, bb_init_nodes)
%CREATEBRANCH Summary of this function goes here
%   Detailed explanation goes here

elems_num = size(bb_init_nodes,1)-1;
branch.nodes = endo_nodes(bb_init_nodes,:);
branch.elems = [(1:elems_num)' (2:elems_num+1)'];

end

