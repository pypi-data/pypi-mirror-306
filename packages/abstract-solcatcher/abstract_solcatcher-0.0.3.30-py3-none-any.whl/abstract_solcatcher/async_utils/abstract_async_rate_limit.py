from ..utils import getEndpointUrl
from abstract_apis import asyncPostRequest,asyncGetRequest

async def async_get_rate_limit_url(method='default_method'):
    return await asyncGetRequest(url=getEndpointUrl("rate_limit"),data={"method":str(method)})

async def async_log_response(method='default_method', response_data={}):
    return await asyncPostRequest(url=getEndpointUrl("log_response"),data={"method":str(method),"response_data":response_data})

async def asyncMakeLimitedCall(method=None,params=[]):
  urls = await async_get_rate_limit_url(method)
  response = await asyncPostRpcRequest(url=urls.get('url'),method=method,params=params,status_code=True,response_result='result')
  if response[1] == 429:
    response = await asyncPostRpcRequest(url=urls.get('url2'),method=method,params=params,response_result='result',status_code=True)
  response_data = 
  await async_log_response(method, response[0])
  return response[0]

def makeLimitedCall(method=None,params=[]):
  return asyncio.run(asyncMakeLimitedCall(method,params))


