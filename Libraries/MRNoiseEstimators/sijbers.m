function sigma=sijbers(I,Nb)

sigma0=moda(I(:),1000);
fc=2.*sigma0;


[h,x]=hist(I(I<fc),Nb);
Nk=sum(h);

sx=x(2)-x(1);
xi=x+sx/2;
xi_1=x-sx/2;

fu_x=@(y)(Nk.*log(exp(-xi_1(1).^2./(2.*y.^2))-exp(-xi(end).^2./(2.*y.^2)))-sum(h.*log(exp(-xi_1.^2./(2.*y.^2))-exp(-xi.^2./(2.*y.^2)))));

X=fminsearch(fu_x,[fc]);

sigma=X;
