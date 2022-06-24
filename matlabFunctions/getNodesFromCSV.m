
function [selected_points] = getNodesFromCSV(points, pathFile)
%getNodesFromCSV Summary of this function goes here
%   this gets nodes from a csv file from paraview, in which nodes were 
%   manually selected.
    format long g;

    selected_points = zeros(size(points,1),1);
    
    nodes_matrix = readmatrix(pathFile);
    matrix_names = detectImportOptions(pathFile);
    matrix_names = matrix_names.VariableNames;
    for i=1:size(matrix_names,2)
        if matrix_names{i}== "Points_0"
            break;
        end
    end

    nodes_coord = nodes_matrix(:,i:i+2);
    idxArr = [];
    for i=1:size(nodes_coord,1)
         idx = find(ismembertol(points,nodes_coord(i,:),1e-6, 'ByRows', true));
         idxArr = [idxArr; idx];
         if size(idx)~=1
             error("More than one stim node detected for the same row from paraview in points from vtk");
         else
            selected_points(idx,1) = 1;
         end
    end


end

