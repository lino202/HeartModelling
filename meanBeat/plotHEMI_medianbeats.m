close  all;
clear all;
clc;

data_path_mi = 'D:/Paper3/Experimental/Mapping/Study_13_12_2023/map2/';
load(append(data_path_mi, 'median_beats/median_beats.mat'));
ECG_time_mi = ECG_time;
fs_mi = fs;
median_beats_mi = median_beats;
data_path_he = 'D:/Paper3/Experimental/ECGs/ecg_cerdo_sano_dylan/';
load(append(data_path_he, 'median_beats/median_beats.mat'));

plot_path = append(data_path_mi, 'median_beats/');

nLeads = length(ECG_headers);

%% Initial plot

figure
for i=1:nLeads
    subplot(4,3,i)
    plot(ECG_time, median_beats(:,i))
    hold on
    plot(ECG_time_mi, median_beats_mi(:,i))
    legend('HE','MI','Location','best','FontSize',8)
    title(ECG_headers(i)), xlim tight, xlabel('time (ms)'),ylabel('Potential (mV)') 
end
 set(gcf, 'PaperUnits', 'inches');
 x_width=9 ;y_width=9;
 set(gcf, 'PaperPosition', [0 0 x_width y_width]); %
 saveas(gcf,append(plot_path,'p_qrs_t_he_mi.png'));

%% Extract ventricular
% For using this code section you need to delineate the signal with
% BiosigBrowser from https://bsicos.i3a.es/

% HE
median_beats_ventricular_he = cell(1,nLeads);
time_ventricular_he = cell(1,nLeads);
for i=1:nLeads
    single_ecg = repmat(median_beats(:,i)',[1,10]);
    single_time = repmat(ECG_time,[1,10]);
    [positionqrs]=wavedelianation_func(append(pwd,'/stable/'), data_path_he, single_ecg, fs, [0 0 0]);
    offset = round(0.010 * fs);
    median_beats_ventricular_he{i} = single_ecg(positionqrs.QRSon-offset:positionqrs.Toff+offset);
    time_ventricular_he{i} = single_time(positionqrs.QRSon-offset:positionqrs.Toff+offset);

end

% MI
median_beats_ventricular_mi = cell(1,nLeads);
time_ventricular_mi = cell(1,nLeads);
for i=1:nLeads
    single_ecg = repmat(median_beats_mi(:,i)',[1,10]);
    single_time = repmat(ECG_time_mi,[1,10]);
    [positionqrs]=wavedelianation_func(append(pwd,'/stable/'), data_path_mi, single_ecg, fs_mi, [0 0 0]);
    offset = round(0.010 * fs_mi);
    median_beats_ventricular_mi{i} = single_ecg(positionqrs.QRSon-offset:positionqrs.Toff+offset);
    time_ventricular_mi{i} = single_time(positionqrs.QRSon-offset:positionqrs.Toff+offset);

end


figure
for i=1:nLeads
    tmp_time_he = cell2mat(time_ventricular_he(i));
    tmp_time_he = tmp_time_he - min(tmp_time_he);
    tmp_time_mi = cell2mat(time_ventricular_mi(i));
    tmp_time_mi = tmp_time_mi - min(tmp_time_mi);

    data_he = cell2mat(median_beats_ventricular_he(i));
    data_mi = cell2mat(median_beats_ventricular_mi(i)); 

    subplot(4,3,i)
    plot(tmp_time_he, data_he)
    hold on
    plot(tmp_time_mi, data_mi)
    legend('HE','MI','Location','best','FontSize',8)
    title(ECG_headers(i)), xlim tight, xlabel('time (ms)'),ylabel('norm V')

end
 set(gcf, 'PaperUnits', 'inches');
 x_width=9 ;y_width=9;
 set(gcf, 'PaperPosition', [0 0 x_width y_width]); %
 saveas(gcf,append(plot_path,'qrs_t_he_mi.png'));