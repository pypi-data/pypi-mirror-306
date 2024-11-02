from ..abstract_rate_limit import makeLimitedCall
from .utils import make_params, get_async_response
async def async_getLatestBlockHash(commitment=None):
    commitment = commitment or "processed"
    method = "getlatestblockhash"
    params = await makeParams(commitment=commitment)
    return await makeLimitedCall(method, params)

def getLatestBlockHash(commitment=None):
    return get_async_response(async_getLatestBlockHash, commitment)
