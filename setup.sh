# Install pip for python
mkdir -p pip
cd pip
wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
python get-pip.py
cd ..

# Install virtualenv for virtual environment
python -m pip install virtualenv 

# Create a virtual environment
python -m virtualenv env

# Activate the environment
source env/bin/activate

# Install numpy with pip
python -m pip install numpy

# Install argeparse with pip
python -m pip install --ignore-installed argparse

# Install pycrypto with pip
python -m pip install pycrypto
