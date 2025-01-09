%*************************************************************************
% Test Problem : 'ZDT1' ---- R-NSGA-II
% Description:
%   (1)unconstrained   (2)convex
%
% Reference : 
% [1] Deb K, Sundar J,  U B R N, et al. Reference point based multi-objective 
%   optimization using evolutionary algorithms[J]. International Journal of 
%   Computational Intelligence Research. 2006, 2(3): 273-286.
% [2] Deb K, Pratap A, Agarwal S, et al. A fast and elitist multiobjective
%    genetic algorithm NSGA-II[J]. Evolutionary Computation. 2002, 6(2): 182-197.
%*************************************************************************

%*************************************************************************
% (1) Optimization model
%*************************************************************************
options = nsgaopt();                    % create default options structure
options.popsize = 50;                   % populaion size
options.maxGen  = 500;                  % max generation

options.numObj = 2;                     % number of objectives
options.numVar = 30;                    % number of design variables
options.numCons = 0;                    % number of constraints
options.lb = zeros(1,30);               % lower bound of x
options.ub = ones(1,30);                % upper bound of x
options.objfun = @TPR_ZDT1_objfun;      % objective function handle

options.plotInterval = 10;              % large interval for efficiency
options.outputInterval = 10;
options.outputfile = 'pop_ZDT1_whole.txt';


%*************************************************************************
% (2) Test 1 : Find the whole Pareto front.
%*************************************************************************
oldresult = nsga2(options);
fprintf('Press any key to continue test R-NSGA-II optimization, press Ctrl+C to stop...\n');
pause


%*************************************************************************
% (3) Test 2 : Find preference solutions with given reference points.
%*************************************************************************
%  R-NSGA-II parameters
options.refPoints = [0.1 0.6; 0.3 0.6; 0.5 0.2; 0.7 0.2; 0.9 0;];
% options.refWeight = [0.2 0.8];            % We do not use weights here;
options.refEpsilon = 0.001;

options.initfun = {@initpop, oldresult};   % Use the last generation of old result as initialized population
options.outputfile = 'pop_ZDT1_ref.txt';

result = nsga2(options);






