%*************************************************************************
% Test Problem : 'CONSTR'
% Description:
%   (1)constrained
%
% Reference : [1] Deb K, Pratap A, Agarwal S, et al. A fast and elitist 
%   multiobjective genetic algorithm NSGA-II[J]. Evolutionary Computation. 
%   2002, 6(2): 182-197.
%*************************************************************************


options = nsgaopt();                    % create default options structure
options.popsize = 50;                   % populaion size
options.maxGen  = 100;                  % max generation

options.numObj = 2;                     % number of objectives
options.numVar = 2;                     % number of design variables
options.numCons = 2;                    % number of constraints
options.lb = [0.1  0];                  % lower bound of x
options.ub = [1    5];                  % upper bound of x
options.objfun = @TP_CONSTR_objfun;     % objective function handle
options.plotInterval = 5;               % interval between two calls of "plotnsga". 

result = nsga2(options);                % begin the optimization!


