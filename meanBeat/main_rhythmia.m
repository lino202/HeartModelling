close  all;
clear all;
clc;

% This code computes the median beat for the rhythmia data.
% This code basically chops and join the segments of good moments of signal 
% acquistion
% And then applies the same algo as in main.m
% We load the beats.mat originated by the parsing script under ~/rhytmia_analisis
% You can run the code with explore=1 and the II signal should be plot for
% inspection, then you can create a .mat file with the variable segments
% in samples for chopping the final signals

data_path = '/home/maxi/Documents/PhD/Paper3/Study_2023_09_11_03-39/results/map2/';
res_path = append(data_path, 'median_beats/');
sample = append(data_path, 'beats.mat');
load(sample);

fs   = sampleFreq;
cutoff = [0.5, 40];

nLeads = size(be_ecg_uni_samples,3);
nBeats = size(be_ecg_uni_samples,1);
nSampleBeat = size(be_ecg_uni_samples,2);

%% Simple preprocessed
ecg_preprocessed = zeros(size(be_ecg_uni_samples));
for i=1:nBeats
    for j=1:nLeads
        ecg_preprocessed(i,:,j) = ecg_preprocessing_func(be_ecg_uni_samples(i,:,j), fs, cutoff);
    end
end

mid_sample = round(size(be_ecg_uni_samples,1)/2);
figure
for i=1:nLeads
    subplot(4,3,i)
    plot(be_ecg_uni_samples(mid_sample,:,i))
    hold on
    plot(ecg_preprocessed(mid_sample,:,i))
    title(be_ecg_uni_channels(1,i))
end
saveas(gcf,append(res_path, 'mid_beat_filtered.png'))



%% Join signals and plot for selecting or get the correlation coeff

% joined_ecgs = zeros(nBeats*nSampleBeat, nLeads);
% for i=1:nBeats
%     for j=1:nLeads
%         joined_ecgs((i-1)*nSampleBeat+1:nSampleBeat*i,j) = ecg_preprocessed(i,:,j);
%     end
% end

% Plot for maybe selecting a window, this seems unfeasible in Rhythmia ECGs
% as one beat is good and the following is chopped
% for i=1:nLeads
%     figure; % Open a new figure
%     plot(joined_ecgs(:,i)); % Example plot command
%     title(num2str(i))
% end

% Use corr instead of xcorr as the crosscorrelation is also near 1 por
% signals with different phase as in our case when we have the qrs and t or
% p and qrs only in one beat
template_sample = squeeze(ecg_preprocessed(mid_sample,:,:));
similar_idxs = zeros(nBeats,nLeads);
for i=1:nLeads
    [similar_idxs(:,i)]=compare_beats_func(template_sample(:,i),ecg_preprocessed(:,:,i), 0.8);
    fprintf("Good beats for Lead %d are %d\n", i, length(find(similar_idxs(:,i))));
end




%% Median beat or plot
% figure
% for i=1:nLeads
%     idxs = find(similar_idxs(:,i));
%     for j=1:length(idxs)
%         plot(ecg_preprocessed(idxs(j),:,i))
%         title(['The Lead is ',num2str(i),', the Beat is ',num2str(idxs(j)), ' the localBeat is ', num2str(j)])
%     end
% end

figure
median_beats = zeros(nSampleBeat,nLeads);
for i=1:nLeads
    idxs = find(similar_idxs(:,i));
    median_beats(:,i) = median(ecg_preprocessed(idxs,:,i),1);
    subplot(4,3,i)
    plot(median_beats(:,i))
    title(be_ecg_uni_channels(1,i))
end
saveas(gcf,append(res_path, 'median_beats.png'))

%% Homogeneize and save
median_beats = (median_beats - min(median_beats,[],1)) ./ (max(median_beats,[],1)-min(median_beats,[],1));
median_beats = median_beats - mean(median_beats);

figure
for i=1:nLeads
    subplot(4,3,i)
    plot(median_beats(:,i))
    title(be_ecg_uni_channels(1,i))
end
saveas(gcf,append(res_path, 'median_beats.png'))

ECG_time = 1:nSampleBeat;
ECG_time = (ECG_time / fs) * 1000;
ECG_headers = be_ecg_uni_channels(1,:);

save(strcat(res_path,'median_beats.mat'),'median_beats','ECG_time','ECG_headers', 'fs', '-mat');