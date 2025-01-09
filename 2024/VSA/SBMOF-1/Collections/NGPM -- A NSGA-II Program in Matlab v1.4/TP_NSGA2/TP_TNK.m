%*************************************************************************
% Test Problem : 'TNK'
% Description:
%   (1)constrained   (2)disconnected
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
options.lb = [0 0];                     % lower bound of x
options.ub = [pi pi];                   % upper bound of x
options.nameObj = {'f1=x1','f2=x2'};    % the objective names are showed in GUI window.
options.objfun = @TP_TNK_objfun;        % objective function handle

options.useParallel = 'no';            % parallel computation is non-essential here
options.poolsize = 2;                   % (not use) number of worker processes

result = nsga2(options);                % begin the optimization!


