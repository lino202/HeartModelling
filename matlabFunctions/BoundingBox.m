function [ bb ] = BoundingBox( nodes )
%BOUNDINGBOX Summary of this function goes here
%   Detailed explanation goes here

minX = inf;
minY = minX;
minZ = minX;
maxX = 0;
maxY = 0;
maxZ = 0;

for i = 1:size(nodes,1)
    
    if nodes(i,1) < minX
        minX = nodes(i,1);
    end
    
    if nodes(i,1) > maxX
        maxX = nodes(i,1);
    end
    
    if nodes(i,2) < minY
        minY = nodes(i,2);
    end
    
    if nodes(i,2) > maxY
        maxY = nodes(i,2);
    end
    
    if nodes(i,3) < minZ
        minZ = nodes(i,3);
    end
    
    if nodes(i,3) > maxZ
        maxZ = nodes(i,3);
    end
    
end

bb.minX = minX-10*eps;
bb.minY = minY-10*eps;
bb.minZ = minZ-10*eps;
bb.maxX = maxX+10*eps;
bb.maxY = maxY+10*eps;
bb.maxZ = maxZ+10*eps;

end

