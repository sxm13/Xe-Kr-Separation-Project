function [y, cons] = TPR_DTLZ2_objfun_5obj(x)
% Objective function : Test problem 'DTLZ2'.
%*************************************************************************


y = [0, 0, 0, 0, 0];
cons = [];

g = sum((x(5:end)-0.5).^2);

y(1) = (1+g) * cos(x(1)*pi/2) * cos(x(2)*pi/2) * cos(x(3)*pi/2) * cos(x(4)*pi/2);
y(2) = (1+g) * cos(x(1)*pi/2) * cos(x(2)*pi/2) * cos(x(3)*pi/2) * sin(x(4)*pi/2);
y(3) = (1+g) * cos(x(1)*pi/2) * cos(x(2)*pi/2) * sin(x(3)*pi/2);
y(4) = (1+g) * cos(x(1)*pi/2) * sin(x(2)*pi/2);
y(5) = (1+g) * sin(x(1)*pi/2);



