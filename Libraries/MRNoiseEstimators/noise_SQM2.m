function [sigma]=noise_SQM2(I,N,Nb)

%NOISE_SQM2 Noise estimation in 2D MR images using Brummer-Aja's method sqrt(X^2)
%
% The function maches the PDF of the local mean of the Rayleigh background
% with the real data
%
%  Inputs: 
%       I: (double) image with Rayleigh background
%       N: Size of window to estimate local square mean (size=NxN)
%       Nb: Number of beens in the histogram
%
% Author: Santiago Aja Fernandez
% NOISE ESTIMATION IN MRI TOOLBOX 
%
% Modified: Oct 02 2008
%

N2=N.^2;
M2=sqrt(filter2(ones(N)./(N.^2),I.^2));

Max=moda(M2(:),Nb);
sigma0=sqrt(N2./(2.*N2-1)).*Max;
fc=2.*Max;


[h,x]=hist(M2(M2<fc),Nb);
h=h./sum(h)./(x(2)-x(1));


fu_x=@(y)sum((h-y(1).*x.^(2*N2-1).*exp(-x.^2.*N2./2./y(2).^2)./gamma(N2)./(2.^(2.*N2-1))./(y(2)^(2.*N2))).^2);
X=fminsearch(fu_x,[1,sigma0]);

sigma=X(2);
%sigma0=sqrt(sigma0);