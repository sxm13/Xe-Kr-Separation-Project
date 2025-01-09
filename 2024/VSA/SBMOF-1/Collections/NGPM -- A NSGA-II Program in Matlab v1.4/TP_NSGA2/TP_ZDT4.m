%*************************************************************************
% Test Problem : 'ZDT4'
% Description:
%   (1)unconstrained   (2)nonconvex  (3)multifrontality
%
% Reference : [1] Deb K, Pratap A, Agarwal S, et al. A fast and elitist 
%   multiobjective genetic algorithm NSGA-II[J]. Evolutionary Computation. 
%   2002, 6(2): 182-197.
%*************************************************************************


options = nsgaopt();                    % create default options structure
options.popsize = 50;                   % populaion size

% Large generation is required to get out of local optimum.
options.maxGen  = 1000;                 % max generation

options.numObj = 2;                     % number of objectives
options.numVar = 10;                    % number of design variables
options.numCons = 0;                    % number of constraints
options.lb = [0 -5 -5 -5 -5 -5 -5 -5 -5 -5];      % lower bound of x
options.ub = [1 5 5 5 5 5 5 5 5 5];               % upper bound of x

options.objfun = @TP_ZDT4_objfun;       % objective function handle

options.outputInterval = 10;
options.plotInterval = 50;


options.useParallel = 'no';             % parallel computation is non-essential here
options.poolsize = 1;                   % (not use) number of worker processes

result = nsga2(options);                % begin the optimization!


