from abstract_database import *
from abstract_solana import Client,get_insert_list
from abstract_utilities import SingletonMeta,safe_read_from_json
from abstract_apis import postRequest,getRequest,postRpcRequest,get_async_response,postRequest
from abstract_solcatcher.utils import getSolcatcherFlaskUrl,getEndpointUrl
import json,inspect,hashlib
from psycopg2.extras import Json
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from abstract_security.abstract_security import get_env_path
from db_functions import *
def generate_data_hash(insertName,value):
    # Combine values to create a unique reference
    data_string = f"{insertName}_{value}"
    return hashlib.md5(data_string.encode()).hexdigest()
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
def make_single(string):
  return string.replace('_','')
def make_multiple(string):
    nustring=''
    uppers = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    for char in string:
        if char in uppers:
            char = f"_{char.lower()}"
        nustring+=char
    return nustring



def get_rate_limit(method=None):
    return getRequest(url=getSolcatcherFlaskUrl(),endpoint='rate_limit',data={"method":method},response_result='url')
def get_log_response(method=None,response={}):
    return postRequest(url=getSolcatcherFlaskUrl(),endpoint='log_response',data={"method":method,"response":response})
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
def get_from_db(freshCall,tableName,searchValue):
    if not freshCall:
        insertValue  = fetch_from_db(tableName=tableName,searchValue=searchValue)
        if insertValue:
            return insertValue
def call_solcatcher_db_api(method,*args,**kwargs):
    variables = get_data_from_dbName('solcatcher',method)
    insertTable = variables['table']
    freshCall = insertTable.get('freshCall')
    tableName=insertTable.get('tableName')
    insertName=insertTable.get('insertName')
    if insertTable.get('rpcCall'):
        rpc_dict = get_body(method,*args,**kwargs)
        searchValue=rpc_dict.get('params')[0]
        insertValue  = get_from_db(freshCall,tableName,searchValue)
        if insertValue is None:
            insertValue = partial_call_solana(method,rpc_dict)
            get_log_response(method,insertValue)
            if isinstance(insertValue,dict) and insertValue.get('error'):
                return insertValue
            if isinstance(searchValue,dict):
                searchValue = generate_data_hash(insertName,insertValue)
            insertintodefaultvalues(key=searchValue, value=insertValue,tableName=tableName)
    else:
        searchValue= args[0] if args else None
        insertValue  = get_from_db(freshCall,tableName,searchValue)
        if insertValue is None:
            url = getEndpointUrl(endpoint=method,url=getSolcatcherFlaskUrl())
            insertValue = postRequest(url=url,data=json.dumps({"args":args,**kwargs}))
            get_log_response(method,insertValue)
            insertintodefaultvalues(key=searchValue, value=insertValue,tableName=tableName)
        #insertIntoDb(tableName=tableName,searchValue=searchValue,insertValue=insertValue)
    return insertValue    
def get_engine():
    dbVars = envManager().get_db_url('solcatcher')
    db_url = f"postgresql://{dbVars['user']}:{dbVars['password']}@{dbVars['host']}:{dbVars['port']}/{dbVars['dbname']}"
    engine = create_engine(db_url)
    return engine
def get_last_row(table_name):
    with get_engine().connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 1;"))
        last_row = result.fetchone()
        return last_row
def find_latest_index():
    df_mgr = dfManager()
    last_row = get_last_row("realestatedata")
    if last_row:
        search_address = last_row[1]
        for index, row in df_mgr.df.iterrows():
            if search_address == df_mgr.get_address_from_row(row):
                return index
    return 0
def get_test_run(multistring,tableName,kwargs={}):
    try:
        response = call_solcatcher_db_api(multistring,**kwargs)
        answr = ''#input('delete table?')
        if answr != '':
            data_brswr.delete_table(tableName)
    except Exception as e:
        print(f'{tableName} failed')
        return e
def query_table(self, query) -> None:
    """
    Delete the specified table from the database.
    
    Args:
        table_name (str): The name of the table to delete.
    
    Returns:
        None
    """
    try:
        query = text(query)
        self.session.execute(query)
        self.session.commit()

    except Exception as e:
        print(f"Error querying table ': {e}")
def get_table(tableName):
    tableName_lower=tableName.lower()
    tables = envManager().get_from_memory(dbName, variable='tables')
    table = [table for table in tables if table.get('tableName').lower() == tableName_lower]
    if table:
        table = table[0]
    return table
def get_db_url():
    dbVars = envManager().get_db_url('solcatcher')
    return f"postgresql://{dbVars['user']}:{dbVars['password']}@{dbVars['host']}:{dbVars['port']}/{dbVars['dbname']}"
def get_browser_mgr():
    dbVars = envManager().get_db_url('solcatcher')
    data_brswr = DatabaseBrowser(dbUrl=get_db_url())
    return data_brswr
def ensure_table_exists(tableName):
    table = get_table(tableName)
    query_table(get_browser_mgr(), table.get('table'))
def delete_table(tableName):
    get_browser_mgr().delete_table(tableName.replace('_','').lower())
def view_table(tableName):

    brows_mgr = get_browser_mgr()
    table_row_count = brows_mgr.session.execute(text(f"SELECT COUNT(*) FROM {tableName}")).scalar()
    if table_row_count:
        brows_mgr.view_table(tableName, table_row_count-1, table_row_count)

def isany_instance(value):
    for each in [dict, list, int, float]:
        if isinstance(value, each):
            return True
def insertintodefaultvalues(key=None, value=None,tableName=None):
    
    table = get_table(tableName)
    #ensure_table_exists(tableName)
    key_key = table.get('columnSearch')
    insertName=table.get('insertName')
    tableName = table.get('tableName')
    
    # Adjusted insert query using consistent parameter style
    insert_query = text(f"""
    INSERT INTO {tableName} ({key_key}, {insertName}, last_updated)
    VALUES (:{key_key}, :{insertName}, NOW())
    ON CONFLICT ({key_key}) DO UPDATE
    SET {insertName} = EXCLUDED.{insertName}, last_updated = NOW()
    WHERE {tableName}.{insertName} != EXCLUDED.{insertName};
    """)
    # Convert value toinput JSON string if it's not a JSON-compatible type
    json_value = Json(value) if isany_instance(value) else Json(f'{value}')
    key_value = str(key) if isany_instance(key) else str(f'{key}')
    # Connect to the database using SQLAlchemy
    with get_engine().connect() as conn:
        try:
            conn.execute(insert_query, {key_key: key_value, insertName: json_value})
            conn.commit()
            print(f"Inserted ({key}, {value}) as {json_value} successfully.")
        except SQLAlchemyError as e:
            print(f"Failed to insert data: {e}")
def get_from_defaults(column):
    fetched = fetchFromDb(tableName='defaultvalues', searchValue=column)
    if fetched is None:
        default = input(f"please input {column} default: ")
        insertintodefaultvalues(column, default,'defaultvalues')
    else:
        default = fetched[0]
    
    return default
def manage_db():
    manageDb(dbUrl=get_db_url())
def redo_tables():
    #get_browser_mgr().delete_table('defaultvalues'.replace('_',''))
    insertintodefaultvalues('pubkey','4BJXYkfvg37zEmBbsacZjeQDpTNx91KppxFJxRqrz48e','defaultvalues')
    insertintodefaultvalues('start_slot',298851000,'defaultvalues')
    insertintodefaultvalues('slot',298851434,'defaultvalues')
    insertintodefaultvalues('account','vines1vzrYbzLMRdu58ou5XTby4qAqVRLmqo36NKPTg','defaultvalues')
    insertintodefaultvalues('pubkeys',['vines1vzrYbzLMRdu58ou5XTby4qAqVRLmqo36NKPTg','4BJXYkfvg37zEmBbsacZjeQDpTNx91KppxFJxRqrz48e'],'defaultvalues')
    insertintodefaultvalues('usize',50,'defaultvalues')
    insertintodefaultvalues('signature','3KGLynUHZDryCQRemQ37uwgKTjP3FKVmVsKrDHHnvzPuN5jqyAvk1Ua3n4GQfWtKmDDMjkAWtotdsn2QCMDSkVbP','defaultvalues')
    insertintodefaultvalues('signatures',['3KGLynUHZDryCQRemQ37uwgKTjP3FKVmVsKrDHHnvzPuN5jqyAvk1Ua3n4GQfWtKmDDMjkAWtotdsn2QCMDSkVbP','2bTjFSEGeKcNuSS7hySEJikE9WVwqaAwY671nYMjhXyPqTG3naYWiMiezcyXFdQp5gPkL3NhTbXucVhra5MbHL4N'],'defaultvalues')
    fetched = fetchFromDb(tableName='defaultvalues',searchValue='slot')
    print(fetched)
    fetched = fetchFromDb(tableName='defaultvalues',searchValue='pubkey')
    print(fetched)
    tables = envManager().get_from_memory(dbName, variable='tables')

    data_brswr = get_browser_mgr()
    js_tally={'anyKeys':{}}
    for table in tables:
        tableName = table.get('tableName')
        view_table(tableName)
def get_all_tables():
    for table in tables:
        method = table.get('method')
        multistring = make_multiple(method)
        tableName = table.get('tableName')
        key_key = table.get('columnSearch')
        insertName=table.get('insertName')
        if tableName != 'defaultvalues':
            query = text(f"DROP TABLE IF EXISTS {tableName}")
            data_brswr.session.execute(query)
            data_brswr.session.commit()
            kwargs={}
            if multistring not in js_tally:
                js_tally[multistring]={}
            query = text(f"CREATE TABLE IF NOT EXISTS {tableName} (id SERIAL PRIMARY KEY, {key_key} VARCHAR(255) UNIQUE NOT NULL, {insertName} JSONB NOT NULL, last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
            data_brswr.session.execute(query)
            data_brswr.session.commit()
            e = get_test_run(multistring,tableName)
            if e:
                print(f"{e}")
                js_tally[multistring]['needs']=eatAll(str(e).split(':')[-1],[' ','\n','\t','']).split(',')
                js_tally[multistring]['inputs']={}
                for need in js_tally[multistring]['needs']:
                    need = need.replace('"','').replace("'",'')
                    if need not in js_tally['anyKeys']:
                        default = get_from_defaults(need)
                        js_tally['anyKeys'][need]=default
                    js_tally[multistring]['inputs'][need] = js_tally['anyKeys'][need]
                kwargs = js_tally[multistring]['inputs']
            get_test_run(multistring,tableName,kwargs)
        last_row = get_last_row(tableName)
        print('\n\n')
        view_table(tableName)
        print(f'\n\nlast row for {method} == {last_row}')

