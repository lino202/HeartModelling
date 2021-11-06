function img = checkLPSOrientation(img)
% this function recieves a struct from ReadNrrd and check if space in
% metaData is LPS, if not, it would change the ijktoLPStransform and space
% name, origin and directions, returning the correct LPS struct

    if img.metaData.space == "right-anterior-superior"
        ras_to_lps = diag([-1 -1 1 1]);
        img.ijkToLpsTransform = ras_to_lps*img.ijkToLpsTransform;
        img.metaData.space = "left-posterior-superior";
        
        directions = append( 'none ', mat2str(img.ijkToLpsTransform(1:3,1)), ' ' , ...
            mat2str(img.ijkToLpsTransform(1:3,2)), ' ', ...
            mat2str(img.ijkToLpsTransform(1:3,3)));
        directions = strrep(directions, '[', '(');
        directions = strrep(directions, ']', ')');
        img.metaData.space_directions = strrep(directions, ';', ',');
    
        
        
        origin = textscan(img.metaData.space_origin,'(%f,%f,%f)');
        origin = cell2mat(origin);
        origin(1) = -origin(1);
        origin(2) = -origin(2);
        origin = mat2str(origin');
        
        origin = strrep(origin, '[', '(');
        origin = strrep(origin, ']', ')');
        img.metaData.space_origin = strrep(origin, ';', ',');

    elseif img.metaData.space ~= "left-posterior-superior"
        error("Wrong orientation %s",img.metaData.space)
    end
end