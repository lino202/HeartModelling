function [ecg_nm_f]=ecg_preprocessing_func(ecg,fs,cutoff)
%INPUT:
% ecg= ecg signal as vector
% fs= sample frequency
% cutoff= vector containing cutoff frequencies for bandpass filter
% OUTPUT:
%ecg_nm_f=preprocessd ECG

%% remove mean
ecg=ecg-mean(ecg); 

%% Filtering
fN=fs/2;
[Bfpa,Afpa]=butter(3,cutoff(1)/fN,'high'); 
[Bfpb,Afpb]=butter(3,cutoff(2)/fN,'low');  
ecg_hf=filtfilt(Bfpa,Afpa,ecg);  
ecg_nm_f= filtfilt(Bfpb,Afpb,ecg_hf); 

end
