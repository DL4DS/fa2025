#!/bin/bash -l

# submit this as a batch job with the command "qsub qsub-example.sh"

# SCC documentation
#
# https://www.bu.edu/tech/support/research/system-usage/running-jobs/submitting-jobs/
# https://www.bu.edu/tech/support/research/software-and-programming/gpu-computing/

# the following lines are directives controlling the batch system.

#$ -pe omp 4     # request 4 CPU cores
#$ -l gpus=1     # request 1 GPU
#$ -l gpu_c=7.0  # request GPU version 7.0 or better
#$ -P ds542      # Specify the SCC project name you want to use
#$ -N example    # Give job a name

############################################################

set -e # stop script on error

# load python environment

module load miniconda academic-ml/fall-2025
conda activate fall-2025-pyt

############################################################
# beginning of job-specific changes
############################################################

# change to your working directory
cd /projectnb/ds542/admin/jconsidi

nvidia-smi

jupyter nbconvert --to notebook --execute qsub-example.ipynb --output qsub-example-output.ipynb

############################################################
# mandatory blank line at end of script
# https://www.bu.edu/tech/support/research/system-usage/running-jobs/submitting-jobs/
############################################################

