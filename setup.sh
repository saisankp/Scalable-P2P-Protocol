# Install python 3.8.12
mkdir python
cd python
wget https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tgz
tar -xzvf Python-3.8.12.tgz
cd Python-3.8.12
./configure --prefix=$HOME/python-3.8.12
make
make install
export PATH=$HOME/python-3.8.12/bin:$PATH

# Install virtualenv for virtual environment
python -m pip install virtualenv 

# Activate the environment
source env/bin/activate

