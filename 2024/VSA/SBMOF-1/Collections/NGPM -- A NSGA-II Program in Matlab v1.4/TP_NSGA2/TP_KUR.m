%*************************************************************************
% Test Problem : 'KUR'
% Description:
%   (1)unconstrained  (2)nonconvex  (3)disconnected
%
% Reference : [1] Deb K, Pratap A, Agarwal S, et al. A fast and elitist 
%   multiobjective genetic algorithm NSGA-II[J]. Evolutionary Computation. 
%   2002, 6(2): 182-197.
%*************************************************************************

options = nsgaopt();                    % create default options structure
options.popsize = 50;                   % populaion size
options.maxGen  = 100;                  % max generation

options.numObj = 2;                     % number of objectives
options.numVar = 3;                     % number of design variables
options.numCons = 0;                    % number of constraints
options.lb = [-5 -5 -5];                % lower bound of x
options.ub = [5  5 5];                  % upper bound of x

options.objfun = @TP_KUR_objfun;        % objective function handle


options.useParallel = 'no';             % parallel computation is non-essential here
options.poolsize = 2;                   % (not use) number of worker processes

result = nsga2(options);                % begin the optimization!


