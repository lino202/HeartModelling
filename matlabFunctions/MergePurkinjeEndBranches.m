function [merged] = MergePurkinjeEndBranches(bundle, purki, bridge_nid)
%MERGEBUNDLEBRANCHES Summary of this function goes here
%   Detailed explanation goes here

% Check that the first node of the second branch is shared with the first branch
common_node_id = -1;
for i=1:size(purki.nodes,1)
    aa = abs(bundle.nodes(bridge_nid,:)-purki.nodes(i,:));
    if (aa(1) < 2*eps && aa(2) < 2*eps && aa(3) < 2*eps)
        common_node_id = i;
        break;
    end
end
if common_node_id == -1, error('Second branch is not attached to the first'); end
    

% Merge the nodes of the two branches skipping the first node of the second
% branch since it appears also in the first branch
purki.nodes(common_node_id,:) = [];
merged.nodes = [bundle.nodes ; purki.nodes];

% Shift connectivity of the second branch to fit the ordering of the new
% nodes
switch_pos = find(purki.elems(:,1)==common_node_id);
pad = size(bundle.nodes,1);
purki.elems = purki.elems + pad -1;
purki.elems(switch_pos,1) = bridge_nid;

merged.elems = [bundle.elems ; purki.elems];

% Merge nodesets
merged.nsets = {};
if isfield(bundle,'nsets')
    merged.nsets = bundle.nsets;
end

if isfield(purki,'nsets')
    if ~isempty(merged.nsets)
        for ii = 1:length(purki.nsets)
            % Adjust node ids in nodeset for new nodes ordering
            nset_ids = purki.nsets{ii}{1};
            for j = 1:length(nset_ids)
                if nset_ids(j) == 1
                    nset_ids(j) = common_node_id;
                else
                    nset_ids(j) = nset_ids(j) + pad -1;
                end
            end
            % Add the nodeset in the cell array
            merged.nsets{end+1} = {nset_ids,purki.nsets{ii}{2}};
        end
    else
        merged.nsets = [merged.nsets purki.nsets];
    end
end

end

