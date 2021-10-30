function [sigma]=noise_M2_mask(I,N,Nb,Mk)

%NOISE_M2 Noise estimation in 2D MR images using Brummer-Aja's method (X^2)
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
%M2=filter2(ones(N)./(N.^2),I.^2);
M2=localmean_mask((I.*Mk).^2,0,[N,N]);  

Max=moda(M2(Mk>0),Nb);
sigma0=(N2-1)./N2.*0.5.*moda(M2(Mk>0),Nb);
fc=2.*Max;


[h,x]=hist(M2((Mk>0)&M2<fc),Nb);
h=h./sum(h)./(x(2)-x(1));


fu_x=@(y)sum((h-y(1).*x.^(N2-1).*exp(-x.*N2./2./y(2))./gamma(N2)./(2.*y(2)./(N2)).^(N2)).^2);
X=fminsearch(fu_x,[1,sigma0]);

sigma=sqrt(X(2));
%sigma0=sqrt(sigma0);
