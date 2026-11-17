%% ========================================================================
%  MALLA 1D DE LA FIBRA TRANSMURAL (endo - mid - epi) CON BORDES
%
%  Configuracion del articulo del grupo: zona central transmural de 1,6 cm con
%  40 % endo, 25 % mid y 35 % epi, mas 1 cm anadido a CADA extremo para que el
%  efecto de borde no contamine la medida. El borde
%  endocardico se rellena con celulas endo y el epicardico con epi, de modo que
%  cada extremo prolonga la capa que tiene al lado.
%
%  La fibra completa mide 1 + 1,6 + 1 = 3,6 cm, pero el pseudo-ECG y los
%  biomarcadores se calculan SOLO sobre la zona central (nodeset central_nodes).
%
%  Malla 1D: una fila de nodos con elementos DC1D2 de dos nodos. El estimulo es UN solo nodo. 
%  En el JSON hay que poner "dimensions" : 1 y "cell vertices" : 2.
%
%  El estimulo va en el extremo ENDOCARDICO (x = 0) y el electrodo del
%  pseudo-ECG a 2 cm del final de la zona central. 
%
%  Salidas: el .inp de la malla, el .json de las fibras y una figura. El JSON de
%  la simulacion lo genera el .sh, como en las tandas del tejido.
% =========================================================================
clear; clc;

%% ------------------------- CONFIGURACION --------------------------------
L_CENTRAL = 1.6;          % cm, zona transmural util
L_BORDE   = 1.0;          % cm que se anaden a CADA extremo
H         = 0.01;         % cm, resolucion

% Porcentajes de la ZONA CENTRAL: endo, mid, epi. 
PORCENTAJES = [40 25 35];
% Alternativa: numero de elementos de cada capa central (deja [] para usar %)
N_ELEMENTOS = [];

NOMBRES = {'endo','mid','epi'};
CARPETA = fileparts(mfilename('fullpath'));
NOMBRE  = strrep(sprintf('fibra1D_%gcm_bordes%gcm_h%g', L_CENTRAL, L_BORDE, H), '.', 'p');

%% --------------------------- GEOMETRIA ----------------------------------
L  = L_BORDE + L_CENTRAL + L_BORDE;
nx = round(L/H);            % elementos de toda la fibra
nb = round(L_BORDE/H);      % elementos de cada borde
nc = round(L_CENTRAL/H);    % elementos de la zona central
if abs(L/H-nx)>1e-9 || abs(L_BORDE/H-nb)>1e-9
    error('L = %g cm y borde = %g cm deben ser multiplos de h = %g cm', L, L_BORDE, H);
end

% --- Reparto de la zona central entre las tres capas ---
if ~isempty(N_ELEMENTOS)
    ne = N_ELEMENTOS(:)';
    if sum(ne) ~= nc
        error('N_ELEMENTOS suma %d y la zona central tiene %d elementos', sum(ne), nc);
    end
else
    exacto = PORCENTAJES(:)'/sum(PORCENTAJES) * nc;
    ne = floor(exacto);
    r  = nc - sum(ne);
    [~, o] = sort(exacto - ne, 'descend');     % metodo del mayor resto
    ne(o(1:r)) = ne(o(1:r)) + 1;
    if any(abs(exacto-ne) > 1e-9)
        fprintf('Los porcentajes no caen exactos en la rejilla; se redondea al elemento mas proximo.\n');
    end
end

x = (0:nx)' * H;                      % nodos: uno por posicion
nn = numel(x);
elems = [(1:nx)', (2:nx+1)'];         % elementos DC1D2: dos nodos cada uno

x_c0 = L_BORDE;                       % inicio de la zona central
lim  = x_c0 + [0, cumsum(ne)*H];      % fronteras de las tres capas
x_c1 = lim(end);                      % final de la zona central

fprintf('\nFibra 1D de %.2f cm (%.1f + %.2f central + %.1f) con h = %.3f cm\n', ...
        L, L_BORDE, L_CENTRAL, L_BORDE, H);
fprintf('%d nodos, %d elementos (DC1D2)\n\n', nn, size(elems,1));
fprintf('%-12s %9s %9s %11s %11s %9s\n','zona','desde','hasta','elementos','% pedido','% real');
fprintf('%-12s %9.3f %9.3f %11d %11s %9s\n','borde endo', 0, x_c0, nb, '-', '-');
for j = 1:3
    fprintf('%-12s %9.3f %9.3f %11d %10.1f %9.1f\n', NOMBRES{j}, lim(j), lim(j+1), ...
            ne(j), PORCENTAJES(j)/sum(PORCENTAJES)*100, 100*ne(j)/nc);
end
fprintf('%-12s %9.3f %9.3f %11d %11s %9s\n','borde epi', x_c1, L, nb, '-', '-');

%% ------------------------- NODESETS -------------------------------------
% ELECTRA exige que los nodesets de los modelos cubran TODOS los nodos 
% y un solapamiento no daria error pero dejaria el nodo con el tipo
% celular del ultimo nodeset. Por eso cada nodo esta en uno y solo uno: las
% fronteras se asignan a la capa de la izquierda.
% Los bordes prolongan la capa contigua: el endocardico es endo y el epicardico, epi.
tol = H/100;
ns = struct();
ns.endo_nodes = find(x <  lim(2)-tol);                    % borde endo + endo
ns.mid_nodes  = find(x >= lim(2)-tol & x < lim(3)-tol);
ns.epi_nodes  = find(x >= lim(3)-tol);                    % epi + borde epi

todos = [ns.endo_nodes; ns.mid_nodes; ns.epi_nodes];
assert(numel(todos)==nn && numel(unique(todos))==numel(todos), ...
       'Los nodesets de las capas no cubren exactamente todos los nodos');

ns.central_nodes = find(x >= x_c0-tol & x <= x_c1+tol);   % para el pseudo-ECG
ns.stim1_nodes   = find(abs(x) < tol);                    % extremo endocardico: 1 nodo
ns.ap_nodes      = (1:nn)';

fprintf('\nNodesets: endo %d | mid %d | epi %d | central %d | estimulo %d\n', ...
        numel(ns.endo_nodes), numel(ns.mid_nodes), numel(ns.epi_nodes), ...
        numel(ns.central_nodes), numel(ns.stim1_nodes));
fprintf('Zona central: x de %.2f a %.2f cm (nodos %d a %d)\n', ...
        x_c0, x_c1, ns.central_nodes(1), ns.central_nodes(end));
fprintf('Electrodo del pseudo-ECG: a 2 cm del final de la zona central, x = %.2f cm\n', x_c1+2);

%% --------------------------- ESCRITURA ----------------------------------
f_inp = fullfile(CARPETA, [NOMBRE '.inp']);
fid = fopen(f_inp, 'w');
fprintf(fid, '*Heading\n');
fprintf(fid, '** Fibra 1D transmural %.2f cm = %.1f + %.2f + %.1f, h = %.3f cm\n', ...
        L, L_BORDE, L_CENTRAL, L_BORDE, H);
fprintf(fid, '** Zona central: %d/%d/%d elementos endo/mid/epi (%.0f/%.0f/%.0f %%)\n', ...
        ne, 100*ne/nc);
fprintf(fid, '*Preprint, echo=NO, model=NO, history=NO, contact=NO\n**\n** PARTS\n**\n');
fprintf(fid, '*Part, name=part-1\n');
fprintf(fid, '*Node\n');
for i = 1:nn
    fprintf(fid, '%d, %.15f\n', i, x(i));
end
fprintf(fid, '*Element, type=DC1D2, elset=Mesh\n');
for i = 1:size(elems,1)
    fprintf(fid, '%d, %d, %d\n', i, elems(i,1), elems(i,2));
end
campos = fieldnames(ns);
for k = 1:numel(campos)
    fprintf(fid, '*Nset, nset=%s\n', campos{k});
    v = ns.(campos{k});
    for i = 1:15:numel(v)
        bloque = v(i:min(i+14, numel(v)));
        fprintf(fid, '%d, ', bloque(1:end-1));
        fprintf(fid, '%d\n', bloque(end));
    end
end
fprintf(fid, '*End Part\n**\n**\n** ASSEMBLY\n**\n');
fprintf(fid, '*Assembly, name=Assembly\n**\n*Instance, name=Part-1-1, part=Part-1\n');
fprintf(fid, '*End Instance\n**\n*End Assembly\n');
fclose(fid);

% --- Fibras: un vector por NODO. En 1D solo hay una direccion posible, asi que
% el vector es [1]. Mismo formato que el fichero del tejido.
f_fib = fullfile(CARPETA, [NOMBRE '_fibras.json']);
fid = fopen(f_fib, 'w');
fprintf(fid, '{\n\t"fibers": [\n');
for i = 1:nn
    if i < nn, coma = ','; else, coma = ''; end
    fprintf(fid, '\t\t[1.000000000000000]%s\n', coma);
end
fprintf(fid, '\t]\n}\n');
fclose(fid);

fprintf('\nMalla:  %s\nFibras: %s\n', f_inp, f_fib);
fprintf(['\nAVISO: en 1D el vector de fibra es [1]. Comprueba en la malla de tu ' ...
         'companera\n       si su JSON usa un fichero de fibras o lo omite; si lo ' ...
         'omite, no hace falta.\n']);
fprintf(['En el JSON de la simulacion: "dimensions" : 1 y "cell vertices" : 2.\n']);

%% ----------------------- COMPROBACION VISUAL ----------------------------
figure('Color','w','Position',[80 80 1100 320]);

subplot(2,1,1); hold on
col = [0.00 0.45 0.74; 0.85 0.33 0.10; 0.36 0.55 0.18];
for j = 1:3
    v = ns.([NOMBRES{j} '_nodes']);
    plot(x(v), zeros(size(v)), '.', 'Color', col(j,:), 'MarkerSize', 12, ...
         'DisplayName', NOMBRES{j});
end
plot([x_c0 x_c0], [-1 1], 'k--', 'LineWidth', 1.2, 'DisplayName','zona central');
plot([x_c1 x_c1], [-1 1], 'k--', 'LineWidth', 1.2, 'HandleVisibility','off');
plot(x(ns.stim1_nodes), 0, 'ks', 'MarkerFaceColor','k', 'DisplayName','estimulo');
text(L_BORDE/2, 0.6, 'borde', 'HorizontalAlignment','center', 'Color',[0.4 0.4 0.4]);
text((x_c0+x_c1)/2, 0.6, 'zona central (pseudo-ECG)', 'HorizontalAlignment','center');
text(x_c1+L_BORDE/2, 0.6, 'borde', 'HorizontalAlignment','center', 'Color',[0.4 0.4 0.4]);
ylim([-1 1]); xlim([-0.05 L+0.05]); set(gca,'YTick',[]);
xlabel('x (cm)'); title(sprintf('Fibra 1D de %.2f cm (%d nodos, h = %.3f cm)', L, nn, H));
legend('Location','eastoutside');

subplot(2,1,2); hold on
for j = 1:3
    rectangle('Position',[lim(j) 0 ne(j)*H 1], 'FaceColor', col(j,:), 'EdgeColor','none');
    text(lim(j)+ne(j)*H/2, 0.5, sprintf('%s\n%.0f %%', NOMBRES{j}, 100*ne(j)/nc), ...
         'HorizontalAlignment','center', 'Color','w', 'FontWeight','bold');
end
xlim([x_c0 x_c1]); ylim([0 1]); set(gca,'YTick',[]);
xlabel('x (cm)'); title('Zona central: reparto de las capas');
