function [APD_array] = computeAPD_2021(t,Vm,NC,replevel,stimPeriod_samples)


APD_array = nan(NC,1);
for n=1:NC     
    APD             = onecycleAPD_2021(t(n)-round(stimPeriod_samples/5):t(n)+round(4*stimPeriod_samples/5), Vm(t(n)-round(stimPeriod_samples/5):t(n)+round(4*stimPeriod_samples/5)), replevel);
    APD_array(n)    = APD;
end
     

  