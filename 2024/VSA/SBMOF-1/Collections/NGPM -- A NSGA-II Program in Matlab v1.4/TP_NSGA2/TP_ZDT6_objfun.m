function [y, cons] = TP_ZDT6_objfun(x)
% Objective function : Test problem 'ZDT6'.
%*************************************************************************


y = [0, 0];
cons = [];


numVar = length(x);
g = 1 + 9 * (sum(x(2:numVar))/(numVar-1))^0.25;

y(1) = 1 - exp(-4*x(1)) * sin(6*pi*x(1))^6;
y(2) = g * (1 - (y(1)/g)^2);



