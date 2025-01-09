function [y, cons] = TP_ZDT3_objfun(x)
% Objective function : Test problem 'ZDT3'.
%*************************************************************************


y = [0, 0];
cons = [];


numVar = length(x);
g = 1 + 9*sum(x(2:numVar))/(numVar-1);


y(1) = x(1);
y(2) = g * ( 1-sqrt(x(1)/g) - x(1)/g*sin(10*pi*x(1)) );


