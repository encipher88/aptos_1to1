# aptos_1to1
```
apt install -y software-properties-common
apt-get update -y; apt upgrade -y
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update && apt-cache search python3.1
apt-get install python3.11 -y
ln -s /usr/bin/python3.11 /usr/bin/python
python --version

cd aptos_1to1
pip install -r requirements.txt
sudo sed -i 's/"function": "0x1::coin::transfer",/"function": "0x1::aptos_account::transfer",/g' /usr/local/lib/python3.11/dist-packages/aptos_sdk/client.py
sudo sed -i 's/"type_arguments": \[.*\],/"type_arguments": [],/g' /usr/local/lib/python3.11/dist-packages/aptos_sdk/client.py
python main.py
```


add private keys and wallet

setup delay and amount in main.py
