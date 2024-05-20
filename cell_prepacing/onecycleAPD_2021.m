% Sub-function to determine APD (between max dvdt and a given percentage of
% maximum and minimum membrane potential
function [APD] = onecycleAPD_2021(t, Vm, replevel)

%  figure
  plot(t,Vm,'r')
% plot(Vm)
 hold on

% dvdt                                = (Vm(2:end) - Vm(1:end-1)) ./ (t(2:end) - t(1:end-1));
dvdt                                = diff(Vm);
[~, maxdvin]                        = max(dvdt); % max slope signal

[peak, peakin]                      = max(Vm);
[baselinelvl,~]       = min(Vm(peakin:end));


Voi = baselinelvl + (1 - replevel) * (peak - baselinelvl);
tin = find(Vm(peakin:end) < Voi);

if ~isempty(tin)
    tin = tin(1);
    if t(tin+peakin-1)>= t(maxdvin)
        APD = t(tin+peakin-1)-t(maxdvin)  
          plot(t(maxdvin),Vm(maxdvin),'og')
          plot(t(tin+peakin-1),Vm(tin+peakin-1),'og')
%         plot(maxdvin,Vm(maxdvin),'or')
%          plot(tin+peakin-1,Vm(tin+peakin-1),'or')
    else 
        APD = NaN;
    end
    
else
    APD = NaN;
end

 
end