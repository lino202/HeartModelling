function [ circum_circle, mean_edge ] = TriangleCircumCircle(verts)
%TRIANGLECIRCUMCIRCLE Summary of this function goes here
%   Detailed explanation goes here

    v1 = verts(1,:);
    v2 = verts(2,:);
    v3 = verts(3,:);
    
    % Triangle edges.
    a = sqrt((v1(1)-v2(1))^2 + (v1(2)-v2(2))^2 + (v1(3)-v2(3))^2);
    b = sqrt((v1(1)-v3(1))^2 + (v1(2)-v3(2))^2 + (v1(3)-v3(3))^2);
    c = sqrt((v3(1)-v2(1))^2 + (v3(2)-v2(2))^2 + (v3(3)-v2(3))^2);
    
    circum_circle = (a*b*c) / sqrt((a+b+c)*(b+c-a)*(c+a-b)*(a+b-c));
    
    mean_edge = (a+b+c) / 3;

end

