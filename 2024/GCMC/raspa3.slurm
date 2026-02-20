#!/bin/bash

#SBATCH --partition=
#SBATCH --nodes=1
#SBATCH --job-name=test
#SBATCH --export=ALL

cd $SLURM_SUBMIT_DIR

module add raspa3
raspa3
