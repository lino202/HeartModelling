function [median_beat]=median_beat_func(positionqrs,ecg_nm_f, fs)
    
    % Define RR-dependent interval around R peak
    R = positionqrs;
    R(isnan(R))=[];
    RR=diff(R);
    mRR=round(median(RR)); % if there are several nans is better the median rather than mean
    no=(240/1000)*fs;
    if (mRR/fs)*1000 <=720
        ne=round((2/3)*mRR);
    else
        ne=min([(684/1000)*fs,mRR-(240/1000)*fs]);
    end
    
    % cardiac beat template
    mat = zeros(no+ne+1,length(R)-2);
    for k=2:1:length(R)-1
        mat(:,k-1) = ecg_nm_f(R(k)-no:R(k)+ne); %cardiac beats in columns
    end
    C = corrcoef(mat);
    Csum=[sum(C);1:1:length(C)];
    B=sortrows(Csum',1,'descend');
    template_beat=mat(:,B(1,2))';
    
    % compute median cardiac beat (median of cardiac beats with a correlation greater than 0.9 with the template)  
    K = zeros(1,length(R)-2);
    for i=1:1:length(R)-2
        if corr(mat(:,i),template_beat') >=0.9
            K(i)= i;
        end
    end

    median_beat = median(mat(:,K(K>0)),2);

end