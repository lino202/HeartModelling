function [grads] = ExtractDwiGrads(dwi_meta)
%EXTRACTDWIGRADS Summary of this function goes here
%   Detailed explanation goes here

grads=[];
fn = fieldnames(dwi_meta);
for k=1:numel(fn)
    if(contains(fn{k},'DWMRI_gradient'))
        grad = str2num(dwi_meta.(fn{k}));
        grads = [grads ; grad];
    end
end

end

