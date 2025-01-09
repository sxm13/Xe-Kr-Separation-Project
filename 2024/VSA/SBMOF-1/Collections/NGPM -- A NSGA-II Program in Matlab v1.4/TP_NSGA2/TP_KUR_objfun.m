function [y, cons] = TP_KUR_objfun(x)
% Objective function : Test problem 'KUR'.
%*************************************************************************

y = [0,0];
cons = [];
for i=1:2
    y(1) = y(1) - 10 * exp(-0.2*sqrt(x(i)^2 + x(i+1)^2) );
end
for i=1:3
    y(2) = y(2) + abs(x(i))^0.8 + 5* sin(x(i)^3);
end


