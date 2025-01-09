function [y, cons] = TP_TNK_objfun(x)
% Objective function : Test problem 'TNK'.
%*************************************************************************

y = [0,0];
cons = [0,0];
y(1) = x(1);
y(2) = x(2);
if( x(2) == 0)
    c = -x(1)^2 - x(2)^2 + 1 + 0.1 * cos( 16 * atan(Inf) );
else
    c = -x(1)^2 - x(2)^2 + 1 + 0.1 * cos( 16 * atan(x(1)/x(2)) );
end

if(c>0)
    cons(1) = abs(c);
end

c = (x(1)-0.5)^2 + (x(2)-0.5)^2 - 0.5;
if(c>0)
    cons(2) = abs(c);
end
