function [his] = CreateHisBundle(rbb, lbb, his_size, middle_elevate)
%CREATEHISBUNDLE Summary of this function goes here
%   Detailed explanation goes here

if nargin<4, middle_elevate = 0; end


% Get the growing directions of right and left brances
nr = rbb.nodes(2,:) - rbb.nodes(1,:);
nr = nr./norm(nr);
nl = lbb.nodes(2,:) - lbb.nodes(1,:);
nl = nl./norm(nl);

% Estimated direction towards av node
nav = -0.5.*(nr+nl);

% Create center node merging the two brances and slightly display toward av
% node (fictitious position)
merge_node = 0.5*(rbb.nodes(1,:) + lbb.nodes(1,:)) + middle_elevate*his_size.*nav;

% av node coords
av_node = merge_node + his_size.*nav;

his.nodes = [av_node ; merge_node; rbb.nodes(1,:); lbb.nodes(1,:)];

his.elems = [1 2; 2 3 ; 2 4];

end

