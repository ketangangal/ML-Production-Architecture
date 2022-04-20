echo [$(date)]: "START"
export _VERSION_=3.9

# Enviroment Setup in Project Folder
echo [$(date)]: "CREATE CONDA ENVIRONMENT  ${_VERSION_}"
conda create --prefix ./env python=${_VERSION_} -y
source activate ./env

# Project Structure setup
mkdir Infrastructure_provisioning
mkdir model_training
mkdir model_testing
mkdir predictionApi
mkdir inference
