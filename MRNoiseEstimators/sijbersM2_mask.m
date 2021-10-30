function sigma=sijbersM2_mask(I,Nb,N,Mk)

M2=localmean_mask((I.*Mk).^2,0,[N,N]);  
%M2=filter2(ones(N)./(N.^2),I.^2);
N2=N.^2;

Max=moda(M2(Mk>0),Nb);
sigma0=N2./(2.*(N2-1))*Max;
fc=3.*Max;

sigma0=0.5.*moda(M2(Mk>0),Nb);
fc=4.*sigma0;


[h,x]=hist(M2((Mk>0)&(M2<fc)),Nb);

Nk=sum(h);

sx=x(2)-x(1);
xi=x+sx/2;
xi_1=x-sx/2;

fu_x=@(y)(Nk.*log(gammainc(N2,xi_1(1).*N2/(2.*y),'upper')-gammainc(N2,xi(end).*N2/(2.*y),'upper'))-sum(h.*log(gammainc(N2,xi_1.*N2/(2.*y),'upper')-gammainc(N2,xi.*N2/(2.*y),'upper'))));

X=fminsearch(fu_x,[sigma0]);

sigma=sqrt(X);
