close  all;
clear all;
clc;

% This code is the simplest for getting the median beat of a fairly correct
% ECG signal

%% Dylan Leuven
data_path = 'D:\Paper3\Experimental\ECGs\ecg_cerdo_sano_dylan/';
res_path = append(data_path, 'median_beats/');
sample = append(data_path, 'NL4816_12lead_ECG.mat');

fs   = 2000;
cutoff = [0.5, 40];

load(sample);

%% Data comming with other format (Lund neurys)
% data_path = 'D:/Pigs PTCA/Lund_03_05_10_9_24_base/';
% res_path  = append(data_path, 'median_beats/');
% sample    = append(data_path, 'Lund_03_05_10_9_24_base.mat');
% 
% load(sample);
% 
% fs     = heasig.freq; %samples/s
% cutoff = [0.5, 40];
% crop   = [20,120]; %s, because time is in seconds.
% crop   = crop*fs;
% 
% tmp = heasig.desc(:,size(heasig.desc,2)-2:size(heasig.desc,2)-2+2);
% ECG_headers = cell(1,12);
% for i=1:size(tmp,1)
%    ECG_headers{i}  = convertCharsToStrings(tmp(i,:));
% end
% ECG_data    = signal(:,crop(1):crop(2))';
% ECG_time    = t(crop(1):crop(2));
% 
% % ECG_data    = signal';
% % ECG_time    = t;

%% Common
if ~exist(res_path, 'dir')
    mkdir(res_path)
end
%% Show signals

figure
for i=1:length(ECG_headers)
    subplot(4,3,i)
    plot(ECG_time, ECG_data(:,i))
    title(ECG_headers(i))
end

%% Simple preprocessed
ecg_preprocessed = zeros(size(ECG_data));
figure
for i=1:length(ECG_headers)
    ecg_preprocessed(:,i) = ecg_preprocessing_func(ECG_data(:,i), fs, cutoff);
    subplot(4,3,i)
    plot(ECG_time, ECG_data(:,i))
    hold on
    plot(ECG_time, ecg_preprocessed(:,i))
    title(ECG_headers(i))
end
saveas(gcf,append(res_path, 'filtered.png'))

%% Get the qrs positions - findpeaks
% qrslocs = cell(1,length(ECG_headers));
% figure
% for i=1:length(ECG_headers)
%     [pks, locs] = findpeaks(abs(ecg_preprocessed(:,i)), "MinPeakDistance", 1000);
%     subplot(4,3,i)
%     plot(ECG_time, abs(ecg_preprocessed(:,i)))
%     hold on
%     plot(ECG_time(locs), pks, 'o')
%     title(ECG_headers(i))
%     qrslocs{i} = locs;
% end

%% Get the qrs positions - wavedet 
% For using this code section you need to delineate the signal with
% BiosigBrowser from https://bsicos.i3a.es/
% In this specific case you can use findpeaks as shown above
qrslocs = cell(1,length(ECG_headers));
rrs     = zeros(1,12);
figure
for i=1:length(ECG_headers)
    [positionqrs]=wavedelianation_func(append(pwd,'/stable/'), res_path,ecg_preprocessed(:,i), fs, [2 0 0]);
    subplot(4,3,i)
    plot(ECG_time, ecg_preprocessed(:,i))
    hold on
    plot(ECG_time(positionqrs.qrs), ecg_preprocessed(positionqrs.qrs,i), 'o')
    title(ECG_headers(i))
    qrslocs{i} = positionqrs.qrs;
    rrs(i)     = mean(diff(qrslocs{i})/fs * 1000);
end
saveas(gcf,append(res_path, 'qrs_delination.png'))

%% Get median beats
median_beats = cell(1,length(ECG_headers));
median_beats_sizes = zeros(1,length(ECG_headers));
for i=1:length(ECG_headers)
    median_beat = median_beat_func(cell2mat(qrslocs(i)),ecg_preprocessed(:,i), fs);
    median_beats{i} = median_beat;
    median_beats_sizes(i) = length(median_beat);
end

%% Homogeneize and save
max_size = max(median_beats_sizes);
final_beats = zeros(max_size,length(ECG_headers));
for i=1:length(ECG_headers)
    single_beat = cell2mat(median_beats(i));
    if length(single_beat)< max_size
        final_chunk = ones(1,max_size-length(single_beat)) * single_beat(length(single_beat));
        final_beats(:,i) = [single_beat; final_chunk'];
    else
        final_beats(:,i) = single_beat;
    end
end

median_beats = final_beats;
median_beats = (median_beats - min(median_beats,[],1)) ./ (max(median_beats,[],1)-min(median_beats,[],1));
median_beats = median_beats - median_beats(1,:);

figure
for i=1:length(ECG_headers)
    subplot(4,3,i)
    plot(median_beats(:,i))
    title(ECG_headers(i)),xlim tight, xlabel('time (ms)'),ylabel('norm V')
end
saveas(gcf,append(res_path, 'median_beats.png'))

ECG_time = 1:max_size;
ECG_time = (ECG_time / fs) * 1000;

save(strcat(res_path,'median_beats.mat'),'median_beats','ECG_time','ECG_headers', 'fs','-mat');