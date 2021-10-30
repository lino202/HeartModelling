function [bb_nodes, bb_elems, bb_nsets] = MergeBundleBranches(his_nodes, his_elems, rbb_nodes, rbb_elems, lbba_nodes,lbba_elems, lbba_map, lbbp_nodes, lbbp_elems, lbbp_map)
%MERGEBUNDLEBRANCHES Summary of this function goes here
%   Detailed explanation goes here

% We keep the first two unique nodes of the his bundle and we add the rest
% bundle braches, we skip the first node of the lbbp_nodes because it is
% common with the lbba_nodes
bb_nodes = [his_nodes(1:2,:) ; rbb_nodes ; lbba_nodes ; lbbp_nodes(2:end,:)];

% Rbb connectivity is shifted by two to account for the his bundle nodes
rbb_elems = rbb_elems + 2;

% Lbba connectivity is shifted by two + rbb nodes number respectively
lbba_elems = lbba_elems + size(rbb_nodes,1) + 2;

% Lbbp connectivity is shifted by two + rbb nodes number + lbba nodes
% number -1.
lbbp_elems = lbbp_elems + size(rbb_nodes,1) + size(lbba_nodes,1) + 1;

% Find the position of the first node of lbbp in the lbba nodes
lbb_common_node_id = find(lbba_map(:,2) == lbbp_map(1,2));
lbbp_elems(1,1) = lbb_common_node_id + size(rbb_nodes,1) + 2;

% Reset connectivity of his bundle
his_elems(2,2) = rbb_elems(1,1);
his_elems(3,2) = lbba_elems(1,1);

bb_elems = [his_elems ; rbb_elems ; lbba_elems ; lbbp_elems];

% Collect nodesets
bb_nsets = {{(1:size(bb_nodes,1))','bb_nodes'}, {rbb_elems(:),'rbb_nodes'}, ...
            {lbba_elems(:),'anterior_lbb_nodes'}, {lbbp_elems(:),'posterior_lbb_nodes'}, {[1;2],'his_nodes'}, ...
            {1,'av_node'}, {rbb_elems(end,2),'rbb_end_node'}, {lbba_elems(end,2),'anterior_lbb_end_node'}, ...
            {lbbp_elems(end,2),'posterior_lbb_end_node'}};

end

