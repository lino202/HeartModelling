function sigma=sijbersSQM2(I,Nb,N)


M2=sqrt(filter2(ones(N)./(N.^2),I.^2));

N2=N.^2;

Max=moda(M2(:),Nb);
sigma0=sqrt(N2./(2.*N2-1))*Max;
fc=3.*Max;


[h,x]=hist(M2(M2<fc),Nb);

Nk=sum(h);

sx=x(2)-x(1);
xi=x+sx/2;
xi_1=x-sx/2;

fu_x=@(y)(Nk.*log(gammainc(N2,xi_1(1).^2.*N2/(2.*y^2),'upper')-gammainc(N2,xi(end).^2.*N2/(2.*y^2),'upper'))-sum(h.*log(gammainc(N2,xi_1.^2.*N2/(2.*y^2),'upper')-gammainc(N2,xi.^2.*N2/(2.*y^2),'upper'))));

X=fminsearch(fu_x,[sigma0]);

sigma=X;