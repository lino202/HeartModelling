function [area, normal] = TriangleArea(X)
%%
%TRIANGLEAREA Computes the area of a triangle in 2-dimensional space.
%
%   Input:
%       X - coordinates of the triangle coordinates.
%
%   Output:
%       area - the area of the triangle.
%
% Author:         Grand R. Joldes, Ph.D.
% Affiliation:    ISML - University of Western Australia, Australia
% Website:        -
% E-mail:         grandj@mech.uwa.edu.au
%%

% Check triangle coordinates dimensions.

u = X(2,:)-X(1,:);
v = X(3,:)-X(1,:);
% Computation of triangular element area.
normal = cross(u,v); 
area = 0.5*abs(norm(normal));

end