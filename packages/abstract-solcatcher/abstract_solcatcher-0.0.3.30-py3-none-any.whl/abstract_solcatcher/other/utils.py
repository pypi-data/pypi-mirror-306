import asyncio
from ..utils import get_async_response

async def async_combineParamDicts(params):
  paramDict = {}
  nuParams=[]
  for param in params:
    if isinstance(param,dict):
      paramDict.update(param)
    else:
      nuParams.append(param)
  nuParams.append(paramDict)
  return nuParams

# Synchronous wrapper for makeParams
def combineParamDicts(*args, **kwargs):
    return get_async_response(async_combineParamDicts, *args, **kwargs)

# Asynchronous version of makeParams
async def async_makeParams(*args, **kwargs):
    args = list(args)
    args+=[{k: v} for k, v in kwargs.items() if v is not None]
    return args

# Synchronous wrapper for makeParams
def makeParams(*args, **kwargs):
    return get_async_response(async_makeParams, *args, **kwargs)

def safeArrayGet(listObj,i,wholeReturn=True):
    if len(listObj) > abs(i):
        return listObj[i]
    if wholeReturn:
        return listObj
def safeGet(dictObj,key,returnObj=None,wholeReturn=False):
  if isinstance(dictObj,dict):
    return dictObj.get(key,returnObj)
  if wholeReturn:
    return dictObj
