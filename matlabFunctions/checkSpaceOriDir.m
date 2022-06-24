function [] = checkSpaceOriDir(mask, dxi)

% This function checks if two structs comming from ReadNrrd() have equal
% space name and approximately equal origin and direction coordinates

    isapproximatelyequal = @(x1,x2,tol) all(abs(real(x1(:)-x2(:)))<tol) & all(abs(imag(x1(:)-x2(:)))<tol);

    if ~strcmp(mask.metaData.space, dxi.metaData.space)
        error("Different mask: %s, dxi: %s spaces", mask.metaData.space, dxi.metaData.space)
    end

    origMask = textscan(mask.metaData.space_origin,'(%f,%f,%f)');
    origMask = cell2mat(origMask);
    origDxi = textscan(dxi.metaData.space_origin,'(%f,%f,%f)');
    origDxi = cell2mat(origDxi);
    
    if ~isapproximatelyequal(origMask, origDxi, 1e-5)
        error("Different mask: %s, dwi: %s origins",origMask, origDxi)
    end
    
    
    if ~isapproximatelyequal(mask.ijkToLpsTransform, dxi.ijkToLpsTransform, 1e-5)
        error("Different mask: %s, dwi: %s directions/ijk2LPS",mask.ijkToLpsTransform, dxi.ijkToLpsTransform)
    end
    
    
    
end