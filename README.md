# aptos_1to1
apt install -y software-properties-common
apt-get update -y; apt upgrade -y
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update && apt-cache search python3.1
apt-get install python3.11 -y
ln -s /usr/bin/python3.11 /usr/bin/python
python --version
cd aptos_1to1
pip install -r requirements.txt
python main.py
