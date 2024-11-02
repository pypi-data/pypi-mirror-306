import asyncio
from abstract_apis import get_url,make_endpoint,get_headers,get_async_response
def getSolcatcherUrl():
  return 'http://solcatcher.io'
def get_solcatcherFlaskUrl():
  return 'http://solcatcher.io/Flask'
def get_solcatcherTsUrl():
  return 'http://solcatcher.io/Typescript'
def getEndpointUrl(endpoint=None,url=None):
  url = url or getSolcatcherUrl()
  endpoint = make_endpoint(endpoint or '/')
  return get_url(url,endpoint)
def updateData(data,**kwargs):
  data.update(kwargs)
  return data
def getCallArgs(endpoint):
  return {'getMetaData': ['signature'], 'getPoolData': ['signature'], 'getTransactionData': ['signature'], 'getPoolInfo': ['signature'], 'getMarketInfo': ['signature'], 'getKeyInfo': ['signature'], 'getLpKeys': ['signature'], 'process': ['signature']}.get(get_endpoint(endpoint))
def ifListGetSection(listObj,section=0):
    if isinstance(listObj,list):
        if len(listObj)>section:
            return listObj[section]
    return listObj
