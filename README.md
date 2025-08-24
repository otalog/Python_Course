# Environment Setup ----

# Conda Environment Setup Instructions ----
#  - Using an environment.yml file with conda
#  - Key Terminal Commands:
# 
#    conda env create -f 000_environment_setup/01_conda_environment.yml
#    conda env update --file 000_environment_setup/01_conda_environment.yml --prune
#    conda env export --name ds4b_101p > envname.yml
#    conda env remove --name ds4b_101p
#    conda env list
#
# Alternative Using pip & virtual environments:
#  - Create empty virtual environment:
#      Mac: python3 -m venv ds4b_101_p
#      Windows: python -m venv ds4b_101_p
#  - Activate env:
#      source ds4b_101_p activate
#      (if this doesn't work, use Command Palette > Select Python Interpreter > ds4b_101_p)
#  - Install the requirements.txt
#      pip install -r 000_environment_setup/requirements.txt
#  - Adding packages from requirements.txt
#      Mac: where python
#      Windows: which python
#      path/to/python -m pip install
#  - Freezing dependencies
#      pip freeze > requirements.txt
