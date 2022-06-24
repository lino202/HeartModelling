function [sigma]=AjaNE3D(I,Ws,Nb,method)

%Aja Noise estimation in 3D MR images using Aja's method 
%
% The mode of some histogram is calculated
%
%  Inputs: 
%       I: (double) image with Rayleigh background
%       Ws: Size of window to estimate local square mean (size=NxN)
%       Nb: Number of beens in the histogram
%       method:
%           1: histogram
%           2: mean
%           3: Second order moment 
%           4: Square root of second order moment
%
% Author: Santiago Aja Fernandez
% NOISE ESTIMATION IN MRI TOOLBOX 
%
% Modified: Oct 02 2008

I=double(I);
N=prod(Ws);
[Mx My Mz]=size(I);
if method ==1
     sigma=moda(I(:),Nb);
     sigma=moda(I(I<2.*sigma),Nb);
elseif method==2
    M1=localmean3D(I,Ws);
    Max=moda(M1(:),Nb);
    sigma=sqrt(2/pi).*moda(M1(M1<2.*Max),Nb);
elseif method==3
    M2=localmean3D(I.^2,Ws);
    M2=N./(N-1).*M2;
    Max=moda(M2(:),Nb);
    sigma=sqrt(0.5.*moda(M2(M2<2.*Max),Nb));
elseif method==4   
    M2=sqrt(localmean3D(I.^2,Ws));
    Max=moda(M2(:),Nb);
    sigma=sqrt(N2./(2.*N2-1))*moda(M2(M2<2.*Max),Nb); 
else
    error('Wrong method selection');
end


