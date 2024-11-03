import time,requests,json,struct,os,base58,sys,json,base64
from solana.transaction import AccountMeta, Transaction
from spl.token.instructions import create_associated_token_account, get_associated_token_address, close_account, CloseAccountParams
from solders.pubkey import Pubkey #type: ignore
from solders.instruction import Instruction #type: ignore
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price #type: ignore
from solana.rpc.types import TokenAccountOpts,TxOpts
from typing import Optional, Union
from solders.keypair import Keypair
from solders.hash import Hash
from solana.transaction import Transaction
from solana.rpc.api import Client
from abstract_utilities import get_any_value
from abstract_security import get_env_value
from .pumpFunKeys import get_pump_fun_data
from .utils import *
from ..pythonFlask.abstract_flask import getLatestBlockHash,getTokenAccountBalance,getTransaction,getTokenAccountByOwner
def load_from_private_key(env_key='AMM_P'):
    env_value = get_env_value(key=env_key)
    if env_value:
        return Keypair.from_base58_string(env_value)

def load_keypair_from_file(filename):
    curr = os.path.join(sys.path[0], 'data',  filename)
    with open(curr, 'r') as file:
        secret = json.load(file)
        secret_key = bytes(secret)
        print(base58.b58encode(secret_key))
        return Keypair.from_bytete_key()
payer_keypair = load_from_private_key()
payer_pubkey = str(payer_keypair.pubkey())
owner=Pubkey.from_string(payer_pubkey)
def get_token_balance(payer,mint_str: str):
    
    response = getTokenAccountBalance(str(payer),str(mint_str))
    response=response.get('value',response)
    ui_amount = get_any_value(response, "uiAmount") or 0
    return float(ui_amount)
def sendTransaction(txn: Transaction, payer_keypair, opts=TxOpts(skip_preflight=True)) -> dict:
    # Sign the transaction
    txn.sign(payer_keypair)
    
    # Serialize the transaction to a base64 string
    txn_base64 = base58.b58encode(txn.serialize()).decode('utf-8')
    
    # Prepare the RPC request payload
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "sendTransaction",
        "params": [txn_base64, {"skipPreflight": opts.skip_preflight, "preflightCommitment": "finalized"}]
    }
    
    # Send the transaction
    response = requests.post(
        url="https://rpc.ankr.com/solana/c3b7fd92e298d5682b6ef095eaa4e92160989a713f5ee9ac2693b4da8ff5a370",
        json=payload
    )
    
    # Parse the JSON response
    response_json = response.json()
    
    # Return the result or the entire response in case of error
    return response_json.get('result', response_json)
def get_transaction(signature):

    # Prepare the RPC request payload
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransaction",
        "params": [signature, {"maxSupportedTransactionVersion": 0}]
    }
    
    # Send the transaction
    response = requests.post(
        url="https://rpc.ankr.com/solana/c3b7fd92e298d5682b6ef095eaa4e92160989a713f5ee9ac2693b4da8ff5a370",
        json=payload
    )
    
    # Parse the JSON response
    response_json = response.json()
    
    # Return the result or the entire response in case of error
    return response_json.get('result', response_json)
def confirm_txn(txn_sig, max_retries=20, retry_interval=3):
    retries = 0
    
    while retries < max_retries:
        try:
            
            txn_res = get_transaction(signature=str(txn_sig))
            if txn_res:
                print(txn_res)
                print(f"\n\nhttps://solscan.io/tx/{str(txn_sig)}")
                break
            txn_json = safe_json_loads(txn_res.get('transaction',{}).get('meta',{}))
            error = txn_json.get('err')
            if error is None:
                print("Transaction confirmed... try count:", retries+1)
                return True
            print("Error: Transaction not confirmed. Retrying...")
            if error:
                print("Transaction failed.")
                return False
        except Exception as e:
            print("Awaiting confirmation... try count:", retries+1)
            retries += 1
            time.sleep(retry_interval)
    print("Max retries reached. Transaction confirmation failed.")
    return None
def getKeys(coin_data,token_account,owner,buy=True):
        coin_data = get_pump_fun_data(str("AUuZnGApuL2oJr3yLsYN12pE7Mz8sQpPYt268JAepump"))
        MINT = Pubkey.from_string(coin_data['mint'])
        BONDING_CURVE = Pubkey.from_string(coin_data['bonding_curve'])
        ASSOCIATED_BONDING_CURVE = Pubkey.from_string(coin_data['associated_bonding_curve'])
        ASSOCIATED_USER = token_account
        USER = owner
        PUMP_FUN_TOKEN_PROGRAM_SWITCH = PUMP_FUN_TOKEN_PROGRAM if buy else PUMP_FUN_ASSOC_TOKEN_ACC_PROG
        PUMP_FUN_RENT_PROGRAM_SWITCH = PUMP_FUN_RENT if buy else PUMP_FUN_TOKEN_PROGRAM
        # Build account key list 
        keys = [
            AccountMeta(pubkey=PUMP_FUN_GLOBAL, is_signer=False, is_writable=False),
            AccountMeta(pubkey=USER, is_signer=False, is_writable=True),
            AccountMeta(pubkey=MINT, is_signer=False, is_writable=False),
            AccountMeta(pubkey=BONDING_CURVE, is_signer=False, is_writable=True),
            AccountMeta(pubkey=ASSOCIATED_BONDING_CURVE, is_signer=False, is_writable=True),
            AccountMeta(pubkey=ASSOCIATED_USER, is_signer=False, is_writable=True),
            AccountMeta(pubkey=USER, is_signer=True, is_writable=True),
            AccountMeta(pubkey=PUMP_FUN_SYSTEM_PROGRAM, is_signer=False, is_writable=False), 
            AccountMeta(pubkey=PUMP_FUN_TOKEN_PROGRAM_SWITCH, is_signer=False, is_writable=False),
            AccountMeta(pubkey=PUMP_FUN_RENT_PROGRAM_SWITCH, is_signer=False, is_writable=False),
            AccountMeta(pubkey=PUMP_FUN_EVENT_AUTHORITY, is_signer=False, is_writable=False),
            AccountMeta(pubkey=PUMP_FUN_PROGRAM, is_signer=False, is_writable=False)
        ]
        return keys
def get_coin_data(mint_str):
    return get_pump_fun_data(str(mint_str))



def buildTxn(mint, amount, slippage, token_account_pubkey,sol_in,token_account_instructions,buy=True):
    # Get keys for the transaction, pass the token account's pubkey instead of the AccountMeta object
    keys = getKeys(get_coin_data(mint), token_account_pubkey, owner,buy=buy)
    
    if buy:
        # Calculate max_sol_cost
        slippage_adjustment = 1 + (slippage / 100)
        sol_in_with_slippage = sol_in * slippage_adjustment
        max_sol_cost = int(sol_in_with_slippage * LAMPORTS_PER_SOL)
        print("Max Sol Cost:", sol_in_with_slippage)
        hex_data = bytes.fromhex("66063d1201daebea")
        solCost = max_sol_cost
    else:
        # Calculate minimum SOL output
        sol_out = float(token_balance) * float(token_price)
        slippage_adjustment = 1 - (slippage / 100)
        sol_out_with_slippage = sol_out * slippage_adjustment
        min_sol_output = int(sol_out_with_slippage * LAMPORTS_PER_SOL)
        print("Min Sol Output:", sol_out_with_slippage)
        hex_data = bytes.fromhex("33e685a4017f83ad")
        solCost = min_sol_output
    
    data = bytearray()
    data.extend(hex_data)
    data.extend(struct.pack('<Q', amount))
    data.extend(struct.pack('<Q', solCost))
    data = bytes(data)
    swap_instruction = Instruction(PUMP_FUN_PROGRAM, data, keys)
    blockHash = requests.post(url="https://rpc.ankr.com/solana/c3b7fd92e298d5682b6ef095eaa4e92160989a713f5ee9ac2693b4da8ff5a370",data=json.dumps({"id":1,"jsonrpc":"2.0","method":"getLatestBlockhash","params":[{"commitment":"processed"}]}))
    recent_blockhash = get_any_value(blockHash.json(),'blockhash')
    recent_blockhash = Hash.from_string(recent_blockhash)
    txn = Transaction(recent_blockhash=recent_blockhash, fee_payer=owner)
    txn.add(set_compute_unit_price(UNIT_PRICE))
    txn.add(set_compute_unit_limit(UNIT_BUDGET))
    
    if buy:
        if token_account_instructions:
            txn.add(token_account_instructions)
        txn.add(swap_instruction)
    else:
        txn.add(swap_instruction)
        if close_token_account:
            close_account_instructions = close_account(CloseAccountParams(TOKEN_PROGRAM, token_account_pubkey, owner, owner))
            txn.add(close_account_instructions)
    
    txn.sign(payer_keypair)
    # Send and confirm transaction
    txn_sig = sendTransaction(txn, payer_keypair, opts=TxOpts(skip_preflight=True))
    print("Transaction Signature", txn_sig)
    confirm = confirm_txn(txn_sig)
    print(confirm)

def pump_fun_buy(mint_str: str, sol_in: float = 0.001, slippage: int = 25) -> bool:
    mint_str = str(mint_str)
    mint = Pubkey.from_string(mint_str)
    
    # Get coin data
    coin_data = get_coin_data(mint_str)
    print(coin_data)

    if not coin_data:
        print("Failed to retrieve coin data...")
        return False

    token_account_pubkey = None
    try:
        # Attempt to retrieve token account
        account_data = getTokenAccountByOwner(str(owner), str(mint))
        account_data = account_data.get('value', account_data)
        # Assuming account_data is a list or a similar structure containing the account address
        token_account_pubkey = Pubkey.from_string(account_data[0])  # Accessing the first element if it's a list
    except Exception as e:
        print(f"Error retrieving token account: {e}")
        # Create associated token account if it doesn't exist
        token_account_instructions = create_associated_token_account(
            Pubkey.from_bytes(bytes(owner)),
            Pubkey.from_string(str(owner)),
            Pubkey.from_string(str(mint))
        )
        # Extract the pubkey from the instruction
        token_account_pubkey = token_account_instructions.accounts[1].pubkey  # Assuming accounts[1] is the target account

    # Ensure the token_account is a valid Pubkey
    if not isinstance(token_account_pubkey, Pubkey):
        print("Failed to create or retrieve a valid token account Pubkey...")
        return False

    # Calculate amount
    virtual_sol_reserves = coin_data['virtual_sol_reserves']
    virtual_token_reserves = coin_data['virtual_token_reserves']
    sol_in_lamports = sol_in * LAMPORTS_PER_SOL
    amount = int(sol_in_lamports * virtual_token_reserves / virtual_sol_reserves)
    
    # Build the transaction
    buildTxn(mint, amount, slippage, token_account_pubkey,sol_in,token_account_instructions, buy=True)
    return True


def pump_fun_sell(mint_str: str, token_balance: Optional[Union[int, float]] = None,  slippage: int = 25, close_token_account: bool = True) -> bool:
    try:
        # Get coin data
        coin_data = get_coin_data(mint_str)
        print(coin_data)
        if not coin_data:
            print("Failed to retrieve coin data...")
            return
        
        mint=Pubkey.from_string(mint)
        # Get token account
        token_account = get_token_balance(owner, mint)
        # Calculate token price
        sol_decimal = 10**9
        token_decimal = 10**6
        virtual_sol_reserves = coin_data['virtual_sol_reserves'] / sol_decimal
        virtual_token_reserves = coin_data['virtual_token_reserves'] / token_decimal
        token_price = virtual_sol_reserves / virtual_token_reserves
        print(f"Token Price: {token_price:.20f} SOL")

        # Get token balance
        if token_balance == None:
            token_balance = get_token_balance(mint_str)
        print("Token Balance:", token_balance)    
        if token_balance == 0:
            return
        # Calculate amount
        amount = int(token_balance * token_decimal)
        buildTxn(amount,slippage,buy=False)
    except Exception as e:
        print(e)

def get_token_price(mint_str: str) -> float:
    try:
        # Get coin data
        coin_data = get_coin_data(mint_str)
        if not coin_data:
            print("Failed to retrieve coin data...")
            return None
        virtual_sol_reserves = coin_data['virtual_sol_reserves'] / 10**9
        virtual_token_reserves = coin_data['virtual_token_reserves'] / 10**6
        token_price = virtual_sol_reserves / virtual_token_reserves
        print(f"Token Price: {token_price:.20f} SOL")
        return token_price
    except Exception as e:
        print(f"Error calculating token price: {e}")
        return None
