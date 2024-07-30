clear all;
clc;
close all;

data_path = 'D:/Paper3/Cell_sims/final/he/Gaur/transmural_gaur/meijbord/';
experiment_name = 'gaur_gk1_0135_650CL_1300s_Vm';

% matlab_scripts
% load(append(data_path, experiment_name, '.mat'));
% V = vms;

% eletra_cell
t = readtable(append(data_path, experiment_name, '.txt'), 'ReadVariableNames', false);
V = t.Var2;
time = t.Var1;

% opencarp - bench
% t = readtable(append(data_path, experiment_name, '.dat'), 'ReadVariableNames', false);
% t = table2array(t);
% V = t(:,end);


dt                      = 0.01;                                % ms
stimPeriod              = 769;                               % Stimulus period in ms
stimPeriod_samples      = (stimPeriod/dt);
replevel                = 0.9;                                % repolarization level - APD80

total_sim_time          = 2307; %s
total_samples           = total_sim_time*1000/dt;

V = V(1:total_samples)';
time = dt:dt:size(V,2)*dt;

AP_nodo                 = V;

[y, locs]=findpeaks(AP_nodo,'MinPeakDistance', stimPeriod_samples/1.5);


timevec=locs(2:end-1);    
NC = length(timevec); 
figure
APD_array = computeAPD_2021(timevec,AP_nodo,NC,replevel,stimPeriod_samples);
figure
plot(timevec*dt,APD_array*dt,'MarkerSize',8,'Marker','o','LineStyle','--','Color',[0 0 0])
xlabel('Time (ms)','FontSize',14,'interpreter','latex');
ylabel('APD (ms)','FontSize',14,'interpreter','latex');
set(gca,'TickLabelInterpreter','latex','FontSize',14);
% set(gca,'xlim',[0 size(V,1)/100])

set(gcf, 'PaperUnits', 'inches');
x_width=9 ;y_width=9;
set(gcf, 'PaperPosition', [0 0 x_width y_width]); %
saveas(gcf,append(data_path, experiment_name, '_APD',num2str(replevel*100), '.png'));

save(append(data_path, experiment_name, ".mat"), "time" , "V", '-v7.3');