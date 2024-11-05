from ..abstract_rate_limit import makeLimitedCall
from .utils import makeParams, get_async_response,combineParamDicts
from solana.rpc.types import TokenAccountOpts,TxOpts
from solana.transaction import Transaction
import base58
async def async_getLatestBlockHash(commitment=None):
    commitment = commitment or "processed"
    method = "getLatestBlockhash"
    params = await makeParams(commitment=commitment)
    return await makeLimitedCall(method, params)

def getLatestBlockHash(commitment=None):
    return get_async_response(async_getLatestBlockHash, commitment)

async def async_getSignaturesForAddress(address, limit=None, before=None, after=None, finalized=None,encoding=None,commitment=None,errorProof=False):
    finalized = finalized or True
    method = "getSignaturesForAddress"
    params = await makeParams(address, limit=limit or 1000, before=before, after=after, finalized=finalized,encoding=encoding or 'jsonParsed',commitment=commitment or 0)
    signatureArray = await makeLimitedCall(method, await combineParamDicts(params))
    if errorProof:
        signatureArray = [signatureData for signatureData in signatureArray if signatureData.get('err') == None]
    return signatureArray

def getSignaturesForAddress(address, limit=None, before=None, after=None, finalized=None,encoding=None,commitment=None,errorProof=False):
    return get_async_response(async_getSignaturesForAddress,address, limit=limit, before=before, after=after, finalized=finalized,encoding=encoding,commitment=commitment,errorProof=errorProof)

async def async_getTransaction(signature,maxSupportedTransactionVersion=None):
    maxSupportedTransactionVersion=maxSupportedTransactionVersion or 0
    method = "getTransaction"
    params = await makeParams(signature, maxSupportedTransactionVersion=maxSupportedTransactionVersion)
    return await makeLimitedCall(method, params)

def getTransaction(signature,maxSupportedTransactionVersion=None):
    return get_async_response(async_getTransaction, signature,maxSupportedTransactionVersion=maxSupportedTransactionVersion)

async def async_getAccountInfo(account,encoding=None,commitment=None):
    encoding = encoding or "jsonParsed"
    commitment = commitment or 0
    method = "getAccountInfo"
    params = await makeParams(account, encoding=encoding,commitment=commitment)
    return await makeLimitedCall(method, params)

def getAccountInfo(account,encoding=None,commitment=None):
    return get_async_response(async_getAccountInfo, account,encoding=encoding,commitment=commitment)

async def async_getBalance(account):
    method = "getBalance"
    params = await makeParams(account)
    return await makeLimitedCall(method, params)

def getBalance(account):
    return get_async_response(async_getBalance, account)

async def async_getTokenSupply(address):
    method = "getTokenSupply"
    params = await makeParams(address)
    return await makeLimitedCall(method, params)

def getTokenSupply(address):
    return get_async_response(async_getTokenSupply, address)

async def async_getTokenAccountBalance(account,commitment=None):
    method = "getTokenAccountBalance"
    params = await makeParams(account)
    return await makeLimitedCall(method, params)

def getTokenAccountBalance(account,commitment=0):
    return get_async_response(async_getTokenAccountBalance, account,commitment=commitment)

async def async_getTokenAccountsByOwner(account,mint=None,encoding=None):
    encoding = encoding or "jsonParsed"
    method = "getTokenAccountsByOwner"
    params = await makeParams(account, mint=mint,encoding=encoding)
    return await makeLimitedCall(method, params)

def getTokenAccountsByOwner(account,mint=None,encoding=None):
    return get_async_response(async_getTokenAccountsByOwner, account,mint=mint,encoding=encoding)

async def async_sendTransaction(txn: Transaction, payer_keypair,skipPreflight=True, preflightCommitment=None):
    txn.sign(payer_keypair)
    txn_base58 = base58.b58encode(txn.serialize()).decode('utf-8')
    opts=TxOpts(skip_preflight=skipPreflight)
    preflightCommitment = preflightCommitment or "finalized"
    method = "sendTransaction"
    params = await makeParams(txn_base58, skipPreflight=opts.skipPreflight, preflightCommitment=preflightCommitment)
    return await makeLimitedCall(method, params)

def sendTransaction(txn: Transaction, payer_keypair,skipPreflight=True, preflightCommitment=None):
    return get_async_response(async_sendTransaction, txn, payer_keypair=payer_keypair, skipPreflight=skipPreflight, preflightCommitment=preflightCommitment)

async def async_simulateTransaction(txn: Transaction, payer_keypair,skipPreflight=True, preflightCommitment=None):
    txn.sign(payer_keypair)
    txn_base58 = base58.b58encode(txn.serialize()).decode('utf-8')
    opts=TxOpts(skip_preflight=skipPreflight)
    preflightCommitment = preflightCommitment or "finalized"
    method = "simulateTransaction"
    params = await makeParams(txn_base58, skipPreflight=opts.skipPreflight, preflightCommitment=preflightCommitment)
    return await makeLimitedCall(method, params)

def simulateTransaction(txn: Transaction, payer_keypair,skipPreflight=True, preflightCommitment=None):
    return get_async_response(async_simulateTransaction, txn, payer_keypair=payer_keypair, skipPreflight=skipPreflight, preflightCommitment=preflightCommitment)

def getGenesisSignature(address,before=None):
    while True:
        signatureArray = getSignaturesForAddress(address,before=before,errorProof=True)
        
