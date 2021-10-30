function [merged] = MergeAttachedBranches(b1, b2)
%MERGEBUNDLEBRANCHES Summary of this function goes here
%   Detailed explanation goes here

% Check that the first node of the second branch is shared with the first branch
common_node_id = -1;
for i=1:size(b1.nodes,1)
    aa = abs(b1.nodes(i,:)-b2.nodes(1,:));
    if (aa(1) < 2*eps && aa(2) < 2*eps && aa(3) < 2*eps)
        common_node_id = i;
    end
end
if common_node_id == -1, error('Second branch is not attached to the first'); end
    

% Merge the nodes of the two branches skipping the first node of the second
% branch since it appears also in the first branch
merged.nodes = [b1.nodes ; b2.nodes(2:end,:)];

% Shift connectivity of the second branch to fit the ordering of the new
% nodes
pad = size(b1.nodes,1);
b2.elems = b2.elems + pad -1;
b2.elems(1,1) = common_node_id;

merged.elems = [b1.elems ; b2.elems];

% Merge nodesets
merged.nsets = {};
if isfield(b1,'nsets')
    merged.nsets = b1.nsets;
end

if isfield(b2,'nsets')
    if ~isempty(merged.nsets)
        for ii = 1:length(b2.nsets)
            % Adjust node ids in nodeset for new nodes ordering
            nset_ids = b2.nsets{ii}{1};
            for j = 1:length(nset_ids)
                if nset_ids(j) == 1
                    nset_ids(j) = common_node_id;
                else
                    nset_ids(j) = nset_ids(j) + pad -1;
                end
            end
            % Add the nodeset in the cell array
            merged.nsets{end+1} = {nset_ids,b2.nsets{ii}{2}};
        end
    else
        merged.nsets = [merged.nsets b2.nsets];
    end
end

end

