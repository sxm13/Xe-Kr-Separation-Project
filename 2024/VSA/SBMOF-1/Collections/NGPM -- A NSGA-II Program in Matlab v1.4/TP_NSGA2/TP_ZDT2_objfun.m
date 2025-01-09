function [y, cons] = TP_ZDT2_objfun(x)
% Objective function : Test problem 'ZDT2'.
%*************************************************************************


y = [0, 0];
cons = [];


numVar = length(x);
g = 1 + 9*sum(x(2:numVar))/(numVar-1);


y(1) = x(1);
y(2) = g * ( 1-(x(1)/g)^2);


