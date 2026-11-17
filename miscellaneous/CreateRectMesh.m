function [nodes, cells] = CreateRectMesh(lx, ly, h)
% CREATERECTMESH  Malla estructurada de cuadrilateros sobre un rectangulo.
%
%   [nodes, cells] = CreateRectMesh(lx, ly, h)
%     lx : longitud en x (cm)
%     ly : longitud en y (cm)
%     h  : tamano de elemento deseado (cm)
%
%   Generaliza CreateQuadMesh, que solo hacia cuadrados: CreateRectMesh(l,l,h)
%   da la misma malla.
%
%   Los nodos se numeran por columnas (la y varia primero), igual que el (:)
%   de MATLAB sobre la salida de meshgrid, y los cuadrilateros se escriben en
%   sentido antihorario, como espera Abaqus para los CPE4.
%
%   Si lx o ly no son multiplos exactos de h, el numero de elementos se
%   redondea y el paso real se ajusta ligeramente para que los bordes caigan
%   exactamente en 0 y en lx / ly. El paso real se avisa por pantalla.

    if nargin < 3, error('Uso: CreateRectMesh(lx, ly, h)'); end

    % Numero de nodos por direccion (al menos 2)
    nex = max(1, round(lx/h));   nx = nex + 1;
    ney = max(1, round(ly/h));   ny = ney + 1;

    hx = lx/nex;   hy = ly/ney;
    if abs(hx-h) > 1e-12 || abs(hy-h) > 1e-12
        fprintf(['CreateRectMesh: h ajustado para que los bordes sean exactos: ' ...
                 'hx = %.6g cm, hy = %.6g cm (pedido %.6g)\n'], hx, hy, h);
    end

    % Nodos: la y varia primero (orden por columnas)
    x = linspace(0, lx, nx);
    y = linspace(0, ly, ny);
    [X, Y] = meshgrid(x, y);          % ny x nx
    nodes = [X(:), Y(:)];

    % Celdas: cada cuadrilatero en sentido antihorario
    cells = zeros(nex*ney, 4);
    id = 0;
    for j = 1:nex            % columnas (x)
        for i = 1:ney        % filas (y)
            id = id + 1;
            n1 = (j-1)*ny + i;       % (x_j,   y_i)
            n2 =  j   *ny + i;       % (x_j+1, y_i)
            n3 =  j   *ny + i + 1;   % (x_j+1, y_i+1)
            n4 = (j-1)*ny + i + 1;   % (x_j,   y_i+1)
            cells(id,:) = [n1 n2 n3 n4];
        end
    end

    fprintf('CreateRectMesh: %g x %g cm | %d x %d nodos (%d) | %d elementos\n', ...
            lx, ly, nx, ny, nx*ny, size(cells,1));
end
