

data_path = 'D:/Paper3/Cell_sims/final/he/transmural_gaur/';
experiment_name = 'gaur_endo_he_gk1_plus15_3000s_Vm';

% load(append(data_path, experiment_name, '.mat'));
% V = vms;
% dt = 0.01;
% time = dt:dt:size(V,2)*dt;

t = readtable(append(data_path, experiment_name, '.txt'), 'ReadVariableNames', false);
V = t.Var2;
time = t.Var1;

AP_nodo                 = V;
Fs                      = 1000;                                % 1 KHz
stimPeriod              = 1000;                                % Stimulus period in ms
dt                      = 0.01;                                % ms
stimPeriod_samples      = (stimPeriod/dt);
replevel                = 0.9;                                % repolarization level - APD80

[y, locs]=findpeaks(AP_nodo,'MinPeakDistance',(stimPeriod/dt)/1.5);


timevec=locs(2:end-1);    
NC = length(timevec); 
figure
APD_array = computeAPD_2021(timevec,AP_nodo,NC,replevel,stimPeriod_samples);
figure
plot(((timevec/Fs)*1000)*dt,((APD_array/Fs)*1000) * dt,'MarkerSize',8,'Marker','o','LineStyle','--','Color',[0 0 0])
xlabel('Time (ms)','FontSize',14,'interpreter','latex');
ylabel('APD (ms)','FontSize',14,'interpreter','latex');
set(gca,'TickLabelInterpreter','latex','FontSize',14);
% set(gca,'xlim',[0 size(V,1)/100])

set(gcf, 'PaperUnits', 'inches');
x_width=9 ;y_width=9;
set(gcf, 'PaperPosition', [0 0 x_width y_width]); %
saveas(gcf,append(data_path, experiment_name, '_APD',num2str(replevel*100), '.png'));

save(append(data_path, experiment_name, ".mat"), "time" , "V", '-v7.3');