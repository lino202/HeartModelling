function [bb] = RefineBundleBranch(bb, edge_size)
%REFINEBUNDLEBRANCH Summary of this function goes here
%   Detailed explanation goes here

[bb] = recursive_refinement(bb, edge_size, 0);

end


function [bb] = recursive_refinement(bb, edge_size, required)

[n_num, n_dim] = size(bb.nodes);
[el_num, el_dim] = size(bb.elems);

% Check if there is any element to be refined.
for i = 1:el_num
    n1 = bb.nodes(bb.elems(i,1),:);
    n2 = bb.nodes(bb.elems(i,2),:);
    dist = sqrt(sum((n2-n1).^2));
    if dist > edge_size
        required = 1;
        break;
    end
end

% Refine mesh recursively.
if required
    
    extra_nodes = zeros(el_num, n_dim);
    new_elems = zeros(2*el_num, el_dim);

    % For new nodeset
    extra_nsets = cell(size(bb.nsets));
    for ii = 1:length(bb.nsets)
        extra_nsets{ii} = {zeros(el_num, 1),bb.nsets{ii}{2}};
    end
%     extra_rbb = zeros(el_num, 1);
%     extra_lbba = zeros(el_num, 1);
%     extra_lbbp = zeros(el_num, 1);
%     extra_his = zeros(el_num, 1);
    
    % Pointer to the last node index
    npad = n_num;
    
    % Counter of the new elements and extra nodes
    nel_cnt = 0;
    en_cnt = 1;
    
    % Refine each element that requires refinement
    for i = 1:el_num
        n1 = bb.nodes(bb.elems(i,1),:);
        n2 = bb.nodes(bb.elems(i,2),:);
        dist = sqrt(sum((n2-n1).^2));
        if dist > edge_size
            % Split the element in two
            extra_nodes(en_cnt,:) = 0.5*(n1 + n2);
            npad = npad+1;
            
            new_elems(nel_cnt+1,:) = [bb.elems(i,1), npad];
            new_elems(nel_cnt+2,:) = [npad, bb.elems(i,2)];
            
            % Check in which nodeset the new node belongs, it shares the same
            % nodeset with the end node of the parent element
            for ii = 1:length(bb.nsets)
                nodeids = bb.nsets{ii}{1};
                if ismember(bb.elems(i,2), nodeids)
                    extra_nsets{ii}{1}(en_cnt) = npad;
                    break;
                end
            end
            
            % Increase counters
            nel_cnt = nel_cnt + 2;
            en_cnt = en_cnt+1;
            
        else
            % Store the element as it is
            new_elems(nel_cnt+1,:) = [bb.elems(i,1), bb.elems(i,2)];
            nel_cnt = nel_cnt + 1;
        end
    end
    
    % Remove empty entries from matrices
    extra_nodes = extra_nodes(any(extra_nodes,2),:);
    new_elems = new_elems(any(new_elems,2),:);
    for ii = 1:length(bb.nsets)
        extra_nsets{ii}{1} = extra_nsets{ii}{1}(any(extra_nsets{ii}{1},2),:);
        bb.nsets{ii}{1} = [bb.nsets{ii}{1} ; extra_nsets{ii}{1}];
    end
    
    bb.nodes = [bb.nodes ; extra_nodes];
    bb.elems = new_elems;

        
    % Assume that the mesh is completely refined. 
    % Check the assumption in recursion.
    required = 0;
    [bb] = recursive_refinement(bb, edge_size, required);
        
end


end
