%*************************************************************************
% Test Problem : 'DTLZ2' ---- R-NSGA-II
% Description:
%   (1)Five objectives   (2)non-convex
%
% Reference : 
% [1] Deb K, Sundar J,  U B R N, et al. Reference point based multi-objective 
%   optimization using evolutionary algorithms[J]. International Journal of 
%   Computational Intelligence Research. 2006, 2(3): 273-286.
% [2] Deb K, Pratap A, Agarwal S, et al. A fast and elitist multiobjective
%    genetic algorithm NSGA-II[J]. Evolutionary Computation. 2002, 6(2): 182-197.
%*************************************************************************

% clear;clc;

options = nsgaopt();                    % create default options structure
options.popsize = 200;                  % populaion size
options.maxGen  = 200;                  % max generation

options.numObj = 5;                     % number of objectives
options.numVar = 14;                    % number of design variables
options.numCons = 0;                    % number of constraints
options.lb = zeros(1,14);               % lower bound of x
options.ub = ones(1,14);                % upper bound of x
options.objfun = @TPR_DTLZ2_objfun_5obj;% objective function handle

options.plotInterval = 10;              % large interval for efficiency
options.outputInterval = 10;

options.refPoints = [0.5 0.5 0.5 0.5 0.5; 0.2 0.2 0.2 0.2 0.8;];
options.refEpsilon = 0.002;


result = nsga2(options);






