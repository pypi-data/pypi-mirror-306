from abstract_apis import asyncPostRequest
from abstract_solana import get_rpc_dict
from .utils import getSolcatcherUrl,get_async_response
async def async_solcatcher_api_call(endpoint, *args, **kwargs):
    return await asyncPostRequest(url=getSolcatcherUrl(),endpoint=endpoint,data={'args': args, **kwargs})
def solcatcher_api_call(endpoint,*args,**kwargs):        
    return get_async_response(async_solcatcher_api_call,endpoint, *args, **kwargs)
def solcatcherSolanaDbCall(method,*args,**kwargs):
    rpc_dict =  get_rpc_dict(method,*args,**kwargs)
    return solcatcher_api_call(endpoint='api/v1/rpc_call',**rpc_dict)
