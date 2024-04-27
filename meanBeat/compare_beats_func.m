function [similar_idxs]=compare_beats_func(template, ecg_signals, thresCorr)
    
    % Normalization for having both signals between 0 and 1
    template = (template - min(template)) ./ (max(template) - min(template));
    ecg_signals  = (ecg_signals - min(ecg_signals, [], 2)) ./ (max(ecg_signals,[],2) - min(ecg_signals,[],2));
    similar_idxs = zeros(1,size(ecg_signals,1));
    for i=1:size(ecg_signals,1)

        beat_corr = corr(ecg_signals(i,:)', template);
        if  max(abs(beat_corr)) > thresCorr
            similar_idxs(i) = 1;
        end
          
    end

end