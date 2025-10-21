close  all;
clear all;
clc;

% This code computes the median beat for the EAM data.
% This code basically chops and join the segments of good moments of signal 
% acquistion
% And then applies the same algo as in main.m
% We load the beats.mat originated by the parsing script under ~/eam_analisis
% You can run the code with explore=1 and the II signal should be plot for
% inspection, then you can create a .mat file with the variable segments
% in samples for chopping the final signals

data_path = 'D:/Paper3/Experimental/Mapping/Study_13_12_2023/map2/';
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

joined_ecgs = zeros(nBeats*nSampleBeat, nLeads);
for i=1:nBeats
    for j=1:nLeads
        joined_ecgs((i-1)*nSampleBeat+1:nSampleBeat*i,j) = ecg_preprocessed(i,:,j);
    end
end

% Plot for maybe selecting a window, this seems unfeasible in EAM ECGs
% as one beat is good and the following is chopped
for i=1:nLeads
    figure; % Open a new figure
    plot(joined_ecgs(:,i)); % Example plot command
    title(num2str(i))
end

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


%% Try to get a measure for the RR
% We took the time_s which is the start of the signal and append contiguous
% signals if they exist and the anterior overlaps the posterior and we use
% the median per Lead which afterward we average.

max_discrepancy_s = 0.2; % check accurately empirically this variable with the measured
                         % computed percentage, for the EAM sample of
                         % 12/2023 the accurate value is 0.2 as it seems
                         % there is 1 beat/s, when we put 2 here the RR
                         % increased and the computed percentage was 100%
                         % as we are lacking one intermidiate beat in the
                         % middle.

rrs = zeros(1,nLeads);
computed_perc = zeros(1,nLeads);
for i=1:nLeads
    idxs = find(similar_idxs(:,i));
    contiguous_idxs = idxs((diff(idxs)==1));
    
    lead_rr = [];
    for j=1:size(contiguous_idxs,1)
        idx = contiguous_idxs(j);
        
        overlap_s = ((be_time_s(idx)+(size(ecg_preprocessed,2)/fs)) - be_time_s(idx+1)); % in seconds        
        if abs(overlap_s) < max_discrepancy_s
            [~, loc1] = max(abs(ecg_preprocessed(idx,:,i)));
            [~, loc2] = max(abs(ecg_preprocessed(idx+1,:,i)));
            rr = (be_time_s(idx+1)-be_time_s(idx)) + (loc2/fs) - (loc1/fs);
            lead_rr = [lead_rr; rr];
               
        end
        
    end
    computed_perc(i) = size(lead_rr,1)/size(contiguous_idxs,1)*100;
    rrs(i) = median(lead_rr);
    
    
end


fprintf("The rrs are:")
rrs
fprintf("The mean rr is: %.6f\n", mean(rrs))
fprintf("The computed percentage is:")
computed_perc


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

save(strcat(res_path,'median_beats.mat'),'median_beats','ECG_time','ECG_headers', 'fs', 'rrs', '-mat');