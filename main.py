from multiprocessing.dummy import Pool
from os import getenv
from sys import stderr
from time import sleep

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional

import httpx
from aptos_sdk.account import Account
from aptos_sdk.client import RestClient
from loguru import logger
import random


# Initialize the logger with both console and file output
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white>"
                          " | <level>{level: <8}</level>"
                          " | <cyan>{line}</cyan>"
                          " - <white>{message}</white>")
logger.add("log.txt", rotation="10 MB", format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {line} - {message}")

NODE_URL = getenv("APTOS_NODE_URL", "https://fullnode.mainnet.aptoslabs.com/v1")
REST_CLIENT = RestClient(NODE_URL)

class App:
    def send_tokens(self,
                     private_key: str,
                     wallet: str,
                     to_wallets_value: int) -> None:
        try:
            current_account = Account.load_key(private_key)
            logger.info(f'{current_account}')
        except ValueError:
            logger.error(f'{private_key} | INVALID Private Key')
            return

        while True:
            try:
                account_address = str(current_account.address())
                logger.info(f'{account_address}')
                account_balance = int(REST_CLIENT.account_balance(account_address=account_address))
                gas_price = 10000
                if account_balance <= gas_price:
                    logger.info(f'{private_key} | Small balance: {account_balance / 100000000}')
                    return

                tx_hash = REST_CLIENT.transfer(sender=current_account,
                                               recipient=wallet,
                                               amount=to_wallets_value)
                
                send_value = to_wallets_value / 100000000
                logger.success(f'SEND {send_value} \n FROM:\n {account_address}\n Balance: {account_balance / 100000000} APT \n TO:\n {wallet} \n TX:\n {tx_hash}')

            except Exception as error:
                logger.error(f'{wallet} | {error}')

                if 'INSUFFICIENT_BALANCE_FOR_TRANSACTION_FEE' in str(error):
                    if account_balance:
                        logger.error(f'{wallet} | Small balance: {account_balance / 100000000}')
                    else:
                        logger.error(f'{wallet} | Small balance')
                    return

                elif 'SEQUENCE_NUMBER_TOO_OLD' or '"Transaction already in mempool with a different payload"' in str(error):
                    sleep(1)
                    continue

                elif '{"message":"' in str(error):
                    return
            else:
                return



# ...

def send_1_to_1(args):
    private_key, wallet, to_wallets_value = args
    App().send_tokens(private_key=private_key, wallet=wallet, to_wallets_value=to_wallets_value)
    
    # Add a random delay between transfers (e.g., 1 to 5 seconds)
    min_delay = 15  # Minimum delay in seconds
    max_delay = 30  # Maximum delay in seconds
    random_delay = random.uniform(min_delay, max_delay)
    
    for remaining in range(int(random_delay), 0, -1):
        print(f"\rNext transfer in {remaining} seconds...", end="")
        time.sleep(1)  # Sleep for 1 second

    print("\rTransferring now!\n")  # Move to the next line after the transfer

# ...


if __name__ == '__main__':
    threads = int(input('INPUT NUMBER OF Threads : '))
    user_action = int(input('1. Send APT 1 to 1\n'))

    if user_action == 1:
        with open('private_keys.txt', 'r', encoding='utf-8-sig') as file:
            private_keys = [row.strip() for row in file]

        logger.info(f'Successfull upload {len(private_keys)} private key\'s')

        with open('wallets.txt', 'r', encoding='utf-8-sig') as file:
            wallets = [row.strip() for row in file]

        logger.info(f'Successfull upload {len(wallets)} wallet\'s')

        to_wallets_values = [random.randint(100000, 299999) for _ in wallets]  # Generate random values

        args = list(zip(private_keys, wallets, to_wallets_values))

        with Pool(processes=threads) as executor:
            executor.map(send_1_to_1, args)