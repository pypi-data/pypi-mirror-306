from ..db_utils import *
from abstract_solana import Client,get_insert_list
from abstract_apis import postRequest,getRequest,postRpcRequest,get_async_response,postRequest
from abstract_solcatcher.utils import getSolcatcherFlaskUrl,getEndpointUrl
class clientMgr(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, 'initialized'):  # Prevent reinitialization
            self.initialized = True
            self.client = Client()
            self.functions = {}

    def get_client_function(self, method):
        if method not in self.functions:
            self.functions[method] = getattr(self.client, method, None)
        return self.functions.get(method)
    def inspect_function(self, method_name):
        try:
            if hasattr(self.client, method_name):
                func = self.get_client_function(method)
               
                
                if func and callable(func):
                    try:
                        # Retrieve the signature without calling the method
                        signature = inspect.getargspec(func).args
                        parameters = list(signature.parameters.keys())

                        
                        return parameters
                    except ValueError:
                        return f"Could not retrieve signature for method {method_name}."
                else:
                    return f"{method_name} not found or not callable."
            else:
                return f"{method_name} not found in client."
        except:
            return f"couldnt get the signature for {method_name}"
    def get_body(self,method,*args,**kwargs):
        function = self.get_client_function(method)
        return function(*args,**kwargs)
    def get_partial_call(self,method,body):
        url = get_rate_limit(method)
        response = postRpcRequest(url,**body)
        get_log_response(method, response)
        return response
    def call_solana(self,method,*args,**kwargs):
        body = self.get_body(method,*args,**kwargs)
        response = self.get_partial_call(method,body)
        return response
async def getSolcatcherPost(endpoint, *args, **kwargs):
    # Ensure that the arguments are fully resolved and not coroutines
    resolved_args = [await arg if asyncio.iscoroutine(arg) else arg for arg in args]
    
    # Check for coroutines in kwargs and resolve them without reusing
    resolved_kwargs = {}
    for k, v in kwargs.items():
        if asyncio.iscoroutine(v):
            resolved_kwargs[k] = await v
        else:
            resolved_kwargs[k] = v
    
    # Now pass resolved data into the request
    return await asyncPostRequest(
        url=getSolcatcherFlaskUrl(),
        endpoint=endpoint,
        data={"args": resolved_args, **resolved_kwargs}
    )
def get_variable_tables():
  return safe_read_from_json(os.path.join(os.path.dirname(os.path.abspath(__file__)),'solana_db_tables.json'))
def fetch_from_db(*args,**kwargs):
    return get_async_response(getSolcatcherPost,'fetch_from_db',*args,**kwargs)
def get_rate_limit(method=None):
    return getRequest(url=getSolcatcherFlaskUrl(),endpoint='rate_limit',data={"method":method},response_result='url')
def get_log_response(method=None,response={}):
    return postRequest(url=getSolcatcherFlaskUrl(),endpoint='log_response',data={"method":method,"response":response})
def call_solana(method,*args,**kwargs):
  return clientMgr().call_solana(method,*args,**kwargs)
def get_body(method,*args,**kwargs):
  return clientMgr().get_body(method,*args,**kwargs)
def partial_call_solana(method,body):
  return clientMgr().get_partial_call(method,body)
def insert_db(*args,**kwargs):
    return get_async_response(getSolcatcherPost,'insert_into_db',*args,**kwargs)
def fetch_from_db(*args,**kwargs):
    return get_async_response(getSolcatcherPost,'fetch_from_db',*args,**kwargs)
def call_solcatcher_api(*args,**kwargs):
    return get_async_response(getSolcatcherPost,'/api/v1/rpc_call',*args,**kwargs)
def call_solcatcher_db_api(dbName,method,*args,**kwargs):
    insertTable = get_table(method,get_variable_tables())
    freshCall = insertTable.get('freshCall')
    tableName=insertTable.get('tableName')
    insertName=insertTable.get('insertName')
    if insertTable.get('rpcCall'):
        rpc_dict = get_body(method,*args,**kwargs)
        searchValue=rpc_dict.get('params')[0]
        insertValue  = get_from_db(freshCall,tableName,searchValue,fetch_from_db)
        if insertValue is None:
            insertValue = partial_call_solana(method,rpc_dict)
            get_log_response(method,insertValue)
            if isinstance(insertValue,dict) and insertValue.get('error'):
                return insertValue
            if isinstance(searchValue,dict):
                searchValue = generate_data_hash(insertName,insertValue)
            insertintodefaultvalues(dbName,insertTable,key=searchValue, value=insertValue,tableName=tableName)
    else:
        searchValue= args[0] if args else None
        insertValue  = get_from_db(freshCall,tableName,searchValue)
        if insertValue is None:
            url = getEndpointUrl(endpoint=method,url=getSolcatcherFlaskUrl())
            insertValue = postRequest(url=url,data=json.dumps({"args":args,**kwargs}))
            get_log_response(method,insertValue)
            insertintodefaultvalues(dbName,insertTable,key=searchValue, value=insertValue,tableName=tableName)
        #insertIntoDb(tableName=tableName,searchValue=searchValue,insertValue=insertValue)
    return insertValue
