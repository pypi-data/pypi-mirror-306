import os
import requests
import threading
import time
from abstract_utilities import get_any_value
from abstract_bots.bot_functions import safe_get
def make_directory(file_path):
    os.makedirs(file_path,exist_ok=True)
    return file_path
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
class directoryStart(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, 'initialized'):  # Prevent reinitialization
            self.initialized = True
            self.abs_endpoint = os.path.abspath(__file__)
            self.src_dir = os.path.dirname(self.abs_endpoint)
            #data folder
            self.data_path = make_directory(os.path.join(self.src_dir, 'data'))
            #accounts
            self.rpc_call_dir = make_directory(os.path.join(self.data_path,'rpc_call'))
directory_mgr = directoryStart()
def get_client_rpc(net_type="main"):
    net_type == {"main":"mainnet-beta","dev":"devnet","test":"testnet","default":"http://192.168.1.88:8899"}.get(net_type,"mainnet-beta")
    return f"https://api.{net_type}.solana.com"
def get_unfiltered_socket_directory():
    return directory_mgr.unfiltered_socket_data_dir
def save_unfiltered_socket_data(slot,signature,data):
    socket_directory = get_unfiltered_socket_directory()
    slot_directory = make_directory(os.path.join(socket_directory,str(slot)))
    signature_file_path = os.path.join(slot_directory,f"{signature}.json")
    safe_dump_to_file(file_path = signature_file_path, data=data)
class rpcCallManager(metaclass=SingletonMeta):
    def __init__(self,directory_mgr=None,endpoint = get_client_rpc(net_type="main")):
        if not hasattr(self, 'initialized'):  # Prevent reinitialization
            self.initialized = True
            self.endpoint = endpoint
            self.directory_mgr = directory_mgr or directoryStart()
            self.rpc_call_type_folder = self.directory_mgr.rpc_call_dir
            self.recently_checked_signature_data={}
    def get_result(self,response):
        try:
            response = response.json()
        except:
            return response.text
        if isinstance(response,dict):
            keys = response.keys()
            if 'result' in keys:
                return response['result']
        return response
    def get_conditions(self,conditions):
        # Remove None values to avoid sending them as part of the request
        return {k: v for k, v in conditions.items() if v is not None}
    def get_response(self,call_type, params):
        response = self.rpc_call(call_type, params)
        if isinstance(response,dict) and response.get('error') != None:
            return response
        data = {"call_type":call_type,"params":params,"response":response}
  
        file_path = self.get_file_name(call_type)
        safe_dump_to_file(file_path=file_path,data=data)
        return response
    def get_file_path(self,call_type,file):
        return os.path.join(self.get_call_folder(call_type),file)
    def get_call_folder(self,call_type):
        return make_directory(os.path.join(self.rpc_call_type_folder,call_type))
    def get_file_name(self, call_type):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        file_name_try = f"response_{timestamp}.json"
        rpc_call_type_folder = self.get_call_folder(call_type)
        file_path = os.path.join(rpc_call_type_folder, file_name_try)
        return file_path
    def await_statuse(self,rpc_url,headers,request_data):
        for i in range(3):
            response = requests.post(url=rpc_url, data=json.dumps(request_data), headers=headers)
            if i >1:
                print(f"response loop has gone for {i} itterations; the current response is: {response}")
            if response.status_code == 200:
                return self.get_result(response)
            elif response.status_code == 429:
                # If a 429 status code is received, wait and retry
                wait_time = int(response.headers.get("Retry-After", 5))  # Default wait time is 5 seconds
                time.sleep(wait_time)
        return response
    def rpc_call(self,method, params):
        rpc_url = rpc
        headers = {"Content-Type": "application/json"}
        request_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        }
        return self.await_statuse(self.endpoint,headers,request_data)
    def params_match(self,saved_params, current_params):
        if len(saved_params) != len(current_params):
            return False
        for saved, current in zip(saved_params, current_params):
            if type(saved) != type(current):
                return False
            if isinstance(saved, dict):
                if saved != current:
                    return False
            elif isinstance(saved, list):
                if sorted(saved) != sorted(current):
                    return False
            else:
                if saved != current:
                    return False
        return True
    def json_rpc_call(self,call_type,params):
        
        for file in os.listdir(self.get_call_folder(call_type)):
            file_path = self.get_file_path(call_type,file)
            data = safe_read_from_json(file_path)
            
            if isinstance(data,dict):
                parameters = data.get('params')
                same = self.params_match(parameters, params)
                if same:
                    if data['response']:
                        return data['response']
        return self.get_response(call_type, params)
    def get_transaction(self,slot,signature):
        signature_data = block_data_mgr.get_block_data_signature_data(slot, signature)
        if signature_data:
            return signature_data
        signature_data = self.get_response("getTransaction", [signature, {"maxSupportedTransactionVersion": 0}])
        block_data_mgr.save_block_data_signature_data(slot, signature, signature_data)
        return signature_data

    def fetch_account_data(self,account):
        account_data = self.json_rpc_call("AddressLookupTableAccount",[account, {"maxSupportedTransactionVersion": 0}])
        return account_data

    def get_signature_for_address(self, account=None, address=None, limit=10, before=None, after=None, finalized=True):
        # Prepare the conditions for the RPC call
        account = account or address
        conditions = {
            "limit": limit,
            "before": before,
            "after": after,
            "finalized": finalized,
        }
        # Remove None values to avoid sending them as part of the request
        conditions = {k: v for k, v in conditions.items() if v is not None}
        
        # Perform the RPC call
        return self.json_rpc_call("getSignaturesForAddress", [account, conditions])      
    def get_account_info(self, account=None, address=None, encoding='jsonParsed'):
        account = account or address
        conditions = {
            "encoding":encoding
            }
        return rpc_mgr.json_rpc_call("getAccountInfo",[address,self.get_conditions(conditions)])
    def get_token_account_balance(self, account=None, address=None, mint=None):
        account = account or address
        conditions = {
            "mint":mint,
            "commitment":0
            }

        return rpc_mgr.json_rpc_call("getTokenAccountBalance",[account,self.get_conditions(conditions)])
    def get_token_accounts_by_delegate(self, account=None, address=None, programId=None,encoding='jsonParsed'):
        account = account or address
        conditions = {
            "programId":programId,
            "encoding":encoding
            }
        return rpc_mgr.json_rpc_call("getTokenAccountsByDelegate",[account,self.get_conditions(conditions)])
    def get_account_info(self, account=None, address=None, encoding='jsonParsed'):
        account = account or address
        conditions = {
            "encoding":encoding
            }
        return rpc_mgr.json_rpc_call("getAccountInfo",[account,self.get_conditions(conditions)])
    def get_token_accounts_by_owner(self, account=None, address=None, mint=None,encoding='jsonParsed'):
        account = account or address
        conditons = {
            "mint":mint,
            "encoding": encoding
            }
        return rpc_mgr.json_rpc_call("getTokenAccountsByOwner",[account,self.get_conditions(conditons)])
    

    def get_token_supply(self,token):
        return self.json_rpc_call("getTokenSupply",[token])
    def get_block_time_from_slot(self,slot):
        return self.json_rpc_call("getBlockTime",[int(slot)])
def get_text_response(response):
    try:
        response = response.text
    except Exception as e:
        print(f"could not read text response: {e}")
        return
def get_json_response(response,result='result'):
    try:
        response = response.json()
        result_response = response.get(result,'null')
        if result_response != 'null':
            return result_response
        result_response = response.get(list(response.keys())[-1],'null')
        if result_response != 'null':
            return result_response
        return 'null'
    except Exception as e:
        print(f"could not read json response: {e}")
        return
def get_status_code(response):
    try:
        status_code = response.status_code
        return status_code
    except Exception as e:
        print(f"could not get status code: {e}")
        return
def get_response(response,result='result'):
    json_response = get_json_response(response,result=result)
    if json_response != 'null':
        return json_response
    text_response = get_text_response(response)
    if text_response:
        return text_response
    return response
def make_request(url,result='result',status_code=False):
    try:
        response = requests.get(url)
    except Exception as e:
        print(f"could not get request: {e}")
        if status_code:
            return None,None
        return None
    if status_code:
        return get_response(response,result=result),get_status_code(response)
    return get_response(response,result=result)
class assetRequestManager(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, 'initialized'):  # This check is necessary to avoid reinitialization in a singleton
            self.initialized = True
            self.call_history_manager = {
                'dexscreener': {"last_call": None, 'last_call_time': 0},
                'solana': {"last_call": None, 'last_call_time': 0}
            }
            self.epoch_tracker={}
            self.default_calls_per_min = 10
            self.calls_per_min = {"dexscreener": 300, "solana": self.default_calls_per_min}
            self.lock = threading.Lock()
    def epoch_check(self,api_type):
        if api_type not in self.calls_per_min:
            self.calls_per_min[api_type] = self.default_calls_per_min
        if api_type not in self.epoch_tracker:
            self.epoch_tracker[api_type]=[]
        current_time = time.time()
        epoch_start = current_time-60
        new_epoch_tracker = []
        for i,call in enumerate(self.epoch_tracker[api_type]):
            if call >=epoch_start:
                new_epoch_tracker = self.epoch_tracker[api_type][i:]
                break
        self.epoch_tracker[api_type]=new_epoch_tracker
        if len(self.epoch_tracker[api_type])>=self.calls_per_min[api_type]:
            return 60 - (time.time() - self.epoch_tracker[api_type][0])
        return 0
    def get_rest_time(self, api_type):
        sleep_time = self.epoch_check(api_type)
        if sleep_time > 0:
            time.sleep(sleep_time)

    def dexscreener_api_call(self, url):
        base_url = os.path.basename(url)
        identifier_url = os.path.basename(os.path.dirname(url))
        with self.lock:
            if base_url not in self.call_history_manager['dexscreener']:
                self.call_history_manager['dexscreener'][base_url] = {}
            if identifier_url not in self.call_history_manager['dexscreener'][base_url]:
                self.call_history_manager['dexscreener'][base_url][identifier_url] = {'time': 0, 'response': None, 'status_code': None}
        
        thread = threading.Thread(target=self._dexscreener_api_call_thread, args=(url,))
        thread.start()
        thread.join()
        return self._get_response_from_history('dexscreener', base_url, identifier_url)

    def _dexscreener_api_call_thread(self, url):
        base_url = str(os.path.basename(url))
        initial_url = os.path.dirname(url)
        identifier_url = os.path.basename(initial_url)
        with self.lock:
            if base_url not in self.call_history_manager['dexscreener']:
                self.call_history_manager['dexscreener'][base_url] = {}
            if identifier_url not in self.call_history_manager['dexscreener'][base_url]:
                self.call_history_manager['dexscreener'][base_url][identifier_url] = {"time": 0, "url": url, "response": None, "status_code": None}
            if float(time.time()) - float(self.call_history_manager['dexscreener'][base_url][identifier_url]['time']) > 30 or self.call_history_manager['dexscreener']["last_call"] != [base_url, identifier_url]:
                self.get_rest_time('dexscreener')
                response,status_code = make_request(url,'pairs',status_code=True)
                self.epoch_tracker['dexscreener'].append(time.time())
                self.call_history_manager['dexscreener']["last_call"] = [str(base_url), str(identifier_url)]
                self.call_history_manager['dexscreener'][base_url][identifier_url]['time'] = self.epoch_tracker['dexscreener'][-1]
                self.call_history_manager['dexscreener'][base_url][identifier_url]['status_code'] = status_code
                self.call_history_manager['dexscreener'][base_url][identifier_url]['response'] = response
    def _get_response_from_history(self, api_type, base_url, identifier_url):
        with self.lock:
            return self.call_history_manager[api_type][base_url][identifier_url]['response']
rpc_mgr = rpcCallManager()
asset_mgr = assetRequestManager()
def api_call_token(token):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{token}"
    return asset_mgr.dexscreener_api_call(url)
def api_call_pairs(token):
    url = f"https://api.dexscreener.com/latest/dex/pairs/solana/{token}"
    return asset_mgr.dexscreener_api_call(url)
def call_token(address):
    token_info = api_call_token(address)
    if token_info:
        return 'token',token_info
    return 'token',None
def call_pair(address):
    token_info = api_call_pairs(address)
    if token_info:
        return 'pair',token_info
    return 'pair',None
def get_token_info(address,address_type='token'):
    address_type = {'pair':'pair','token':'token'}.get(address_type,'token')
    call = [address_type,{'pair':'token','token':'pair'}.get(address_type)]
    for call_type in call:
        if call_type == 'pair':
            address_type,address_info = call_pair(address)
        elif call_type == 'token':
            address_type,address_info = call_token(address)
        if address_info:
            return address_type,address_info
    return 'address',address_info
def get_list_obj(obj):
    if obj and isinstance(obj,list):
        obj=obj[0]
    return obj
def get_pair_address(address):
    info = api_call_token(address)
    info=get_list_obj(info)
    return info
def get_baseToken(address):
    info = api_call_token(address)
    info=get_list_obj(info)
    return info.get('baseToken')
def get_quoteToken(address):
    info = api_call_token(address)
    info=get_list_obj(info)
    return info.get('quoteToken')
def get_token_info(address):
    return get_list_obj(api_call_pairs(address) or api_call_token(address) or get_quoteToken(address))
def search_type(address,token_info=None):
    token_info = token_info or get_token_info(address)
    for each in [['pairAddress'],['baseToken','address'],['quoteToken','address']]:
        if address == safe_get(token_info, each):
            return each[0]
def just_get_the_token_info(address,info_type=None):
    token_info = get_token_info(address)
    if info_type:
        return get_any_value(token_info,info_type) or get_any_value(token_info,search_type(address,token_info))
    return token_info
def get_token_pecs(address):
    pair_address = just_get_the_token_info(address,'pairAddress')
    return {"pair_address":pair_address,'baseToken':just_get_the_token_info(pair_address,'baseToken'),'quoteToken': just_get_the_token_info(pair_address,'quoteToken')}
def get_symbols(address):
    return safe_get(get_token_pecs(address),['baseToken','symbol']),safe_get(get_token_pecs(address),['quoteToken','symbol'])
import json
txn = json.loads("{\"blockTime\":1711923458,\"meta\":{\"computeUnitsConsumed\":30783,\"err\":{\"InstructionError\":[4,{\"Custom\":49}]},\"fee\":3000000,\"innerInstructions\":[{\"index\":4,\"instructions\":[{\"parsed\":{\"info\":{\"destination\":\"7YttLkHDoNj9wyDur5pM1ejNaAvT9X4eqaYcHQqtj2G5\",\"lamports\":400000000,\"source\":\"9X6Sf3CCfFAfMCJcnAFnKgCDujkyb1Vu94HU94ZZ9zot\"},\"type\":\"transfer\"},\"program\":\"system\",\"programId\":\"11111111111111111111111111111111\",\"stackHeight\":2},{\"parsed\":{\"info\":{\"account\":\"7YttLkHDoNj9wyDur5pM1ejNaAvT9X4eqaYcHQqtj2G5\"},\"type\":\"syncNative\"},\"program\":\"spl-token\",\"programId\":\"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA\",\"stackHeight\":2}]}],\"logMessages\":[\"Program ComputeBudget111111111111111111111111111111 invoke [1]\",\"Program ComputeBudget111111111111111111111111111111 success\",\"Program ComputeBudget111111111111111111111111111111 invoke [1]\",\"Program ComputeBudget111111111111111111111111111111 success\",\"Program 11111111111111111111111111111111 invoke [1]\",\"Program 11111111111111111111111111111111 success\",\"Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [1]\",\"Program log: Instruction: InitializeAccount\",\"Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 3443 of 299881 compute units\",\"Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success\",\"Program 675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8 invoke [1]\",\"Program log: initialize2: InitializeInstruction2 { nonce: 254, open_time: 1711923436, init_pc_amount: 7000000000, init_coin_amount: 89000000000000 }\",\"Program 11111111111111111111111111111111 invoke [2]\",\"Program 11111111111111111111111111111111 success\",\"Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA invoke [2]\",\"Program log: Instruction: SyncNative\",\"Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA consumed 3045 of 280522 compute units\",\"Program TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA success\",\"Program log: 7cbVEBpRc6WP2gGhSFFhHRJ4AukDYkjSQ8dtLucFQ884\",\"Program log: Error: RepeatCreateAmm\",\"Program 675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8 consumed 26890 of 296438 compute units\",\"Program 675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8 failed: custom program error: 0x31\"],\"postBalances\":[16135517379,0,16258560,88985804860720,2039280,2039280,2039280,1461600,6124800,2257554,23357760,1,2451005820,1141440,3591360,4677120,731913600,1,1461600,515830187572,1141440,1009200,934087680],\"postTokenBalances\":[{\"accountIndex\":3,\"mint\":\"So11111111111111111111111111111111111111112\",\"owner\":\"GThUX1Atko4tqhN2NaiTazWSeFWMuiUvfFnyJyUghFMJ\",\"programId\":\"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA\",\"uiTokenAmount\":{\"amount\":\"88985802821440\",\"decimals\":9,\"uiAmount\":88985.80282144,\"uiAmountString\":\"88985.80282144\"}},{\"accountIndex\":4,\"mint\":\"EgQrt9pGPCgCQCyhj28owYPjR2YpZ9JNkpz379Amhrxc\",\"owner\":\"9X6Sf3CCfFAfMCJcnAFnKgCDujkyb1Vu94HU94ZZ9zot\",\"programId\":\"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA\",\"uiTokenAmount\":{\"amount\":\"1490426\",\"decimals\":6,\"uiAmount\":1.490426,\"uiAmountString\":\"1.490426\"}},{\"accountIndex\":5,\"mint\":\"hJkRHwmMGeSJZrjzGaK2ZGgwJSEzWHvYTBt1EhWUrjB\",\"owner\":\"9X6Sf3CCfFAfMCJcnAFnKgCDujkyb1Vu94HU94ZZ9zot\",\"programId\":\"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA\",\"uiTokenAmount\":{\"amount\":\"96963988153539\",\"decimals\":6,\"uiAmount\":96963988.153539,\"uiAmountString\":\"96963988.153539\"}},{\"accountIndex\":6,\"mint\":\"hJkRHwmMGeSJZrjzGaK2ZGgwJSEzWHvYTBt1EhWUrjB\",\"owner\":\"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1\",\"programId\":\"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA\",\"uiTokenAmount\":{\"amount\":\"310849064\",\"decimals\":6,\"uiAmount\":310.849064,\"uiAmountString\":\"310.849064\"}},{\"accountIndex\":9,\"mint\":\"So11111111111111111111111111111111111111112\",\"owner\":\"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1\",\"programId\":\"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA\",\"uiTokenAmount\":{\"amount\":\"218274\",\"decimals\":9,\"uiAmount\":0.000218274,\"uiAmountString\":\"0.000218274\"}}],\"preBalances\":[16138517379,0,16258560,88985804860720,2039280,2039280,2039280,1461600,6124800,2257554,23357760,1,2451005820,1141440,3591360,4677120,731913600,1,1461600,515830187572,1141440,1009200,934087680],\"preTokenBalances\":[{\"accountIndex\":3,\"mint\":\"So11111111111111111111111111111111111111112\",\"owner\":\"GThUX1Atko4tqhN2NaiTazWSeFWMuiUvfFnyJyUghFMJ\",\"programId\":\"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA\",\"uiTokenAmount\":{\"amount\":\"88985802821440\",\"decimals\":9,\"uiAmount\":88985.80282144,\"uiAmountString\":\"88985.80282144\"}},{\"accountIndex\":4,\"mint\":\"EgQrt9pGPCgCQCyhj28owYPjR2YpZ9JNkpz379Amhrxc\",\"owner\":\"9X6Sf3CCfFAfMCJcnAFnKgCDujkyb1Vu94HU94ZZ9zot\",\"programId\":\"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA\",\"uiTokenAmount\":{\"amount\":\"1490426\",\"decimals\":6,\"uiAmount\":1.490426,\"uiAmountString\":\"1.490426\"}},{\"accountIndex\":5,\"mint\":\"hJkRHwmMGeSJZrjzGaK2ZGgwJSEzWHvYTBt1EhWUrjB\",\"owner\":\"9X6Sf3CCfFAfMCJcnAFnKgCDujkyb1Vu94HU94ZZ9zot\",\"programId\":\"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA\",\"uiTokenAmount\":{\"amount\":\"96963988153539\",\"decimals\":6,\"uiAmount\":96963988.153539,\"uiAmountString\":\"96963988.153539\"}},{\"accountIndex\":6,\"mint\":\"hJkRHwmMGeSJZrjzGaK2ZGgwJSEzWHvYTBt1EhWUrjB\",\"owner\":\"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1\",\"programId\":\"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA\",\"uiTokenAmount\":{\"amount\":\"310849064\",\"decimals\":6,\"uiAmount\":310.849064,\"uiAmountString\":\"310.849064\"}},{\"accountIndex\":9,\"mint\":\"So11111111111111111111111111111111111111112\",\"owner\":\"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1\",\"programId\":\"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA\",\"uiTokenAmount\":{\"amount\":\"218274\",\"decimals\":9,\"uiAmount\":0.000218274,\"uiAmountString\":\"0.000218274\"}}],\"rewards\":[],\"status\":{\"Err\":{\"InstructionError\":[4,{\"Custom\":49}]}}},\"slot\":257620008,\"transaction\":{\"message\":{\"accountKeys\":[{\"pubkey\":\"9X6Sf3CCfFAfMCJcnAFnKgCDujkyb1Vu94HU94ZZ9zot\",\"signer\":true,\"source\":\"transaction\",\"writable\":true},{\"pubkey\":\"4m45eqzd4bLiDA75CJArRDs6VLgrbNn2NtND2dCEvsMm\",\"signer\":false,\"source\":\"transaction\",\"writable\":true},{\"pubkey\":\"7cbVEBpRc6WP2gGhSFFhHRJ4AukDYkjSQ8dtLucFQ884\",\"signer\":false,\"source\":\"transaction\",\"writable\":true},{\"pubkey\":\"7YttLkHDoNj9wyDur5pM1ejNaAvT9X4eqaYcHQqtj2G5\",\"signer\":false,\"source\":\"transaction\",\"writable\":true},{\"pubkey\":\"9xhiwhtnRps6CLTPX7r78TNAajoepjBd4gCJR7RWEeqz\",\"signer\":false,\"source\":\"transaction\",\"writable\":true},{\"pubkey\":\"BLCfjXQiXV2E75eCMAk2tpRQYmtej2zMK9PGUbn6fJHF\",\"signer\":false,\"source\":\"transaction\",\"writable\":true},{\"pubkey\":\"DWaN95nLKTZhJEWtU7Q8JDigcoXtCUPZcbaRrENibiNs\",\"signer\":false,\"source\":\"transaction\",\"writable\":true},{\"pubkey\":\"EgQrt9pGPCgCQCyhj28owYPjR2YpZ9JNkpz379Amhrxc\",\"signer\":false,\"source\":\"transaction\",\"writable\":true},{\"pubkey\":\"EjYMZgWhaETYCoxZ28cuPgzmEwLN2mGjqyWqx7beB1wf\",\"signer\":false,\"source\":\"transaction\",\"writable\":true},{\"pubkey\":\"EzG9423XMkow45Fe3XaDerAKzQrJKyNic2NxAnPPr1Kf\",\"signer\":false,\"source\":\"transaction\",\"writable\":true},{\"pubkey\":\"VWWRQudSAuQ6jRb8kUh1SL5qezczHH67uZwGKTdRHqz\",\"signer\":false,\"source\":\"transaction\",\"writable\":true},{\"pubkey\":\"11111111111111111111111111111111\",\"signer\":false,\"source\":\"transaction\",\"writable\":false},{\"pubkey\":\"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1\",\"signer\":false,\"source\":\"transaction\",\"writable\":false},{\"pubkey\":\"675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8\",\"signer\":false,\"source\":\"transaction\",\"writable\":false},{\"pubkey\":\"8Wobfz55bpB8orA824sKpM9Kk6ipcjvCZ5qCYGfu5vfM\",\"signer\":false,\"source\":\"transaction\",\"writable\":false},{\"pubkey\":\"9DCxsMizn3H1hprZ7xWe6LDzeUeZBksYFpBWBtSf1PQX\",\"signer\":false,\"source\":\"transaction\",\"writable\":false},{\"pubkey\":\"ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL\",\"signer\":false,\"source\":\"transaction\",\"writable\":false},{\"pubkey\":\"ComputeBudget111111111111111111111111111111\",\"signer\":false,\"source\":\"transaction\",\"writable\":false},{\"pubkey\":\"hJkRHwmMGeSJZrjzGaK2ZGgwJSEzWHvYTBt1EhWUrjB\",\"signer\":false,\"source\":\"transaction\",\"writable\":false},{\"pubkey\":\"So11111111111111111111111111111111111111112\",\"signer\":false,\"source\":\"transaction\",\"writable\":false},{\"pubkey\":\"srmqPvymJeFKQ4zGQed1GFppgkRHL9kaELCbyksJtPX\",\"signer\":false,\"source\":\"transaction\",\"writable\":false},{\"pubkey\":\"SysvarRent111111111111111111111111111111111\",\"signer\":false,\"source\":\"transaction\",\"writable\":false},{\"pubkey\":\"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA\",\"signer\":false,\"source\":\"transaction\",\"writable\":false}],\"instructions\":[{\"accounts\":[],\"data\":\"3XDWX3BEZhX5\",\"programId\":\"ComputeBudget111111111111111111111111111111\",\"stackHeight\":null},{\"accounts\":[],\"data\":\"FCgBTm\",\"programId\":\"ComputeBudget111111111111111111111111111111\",\"stackHeight\":null},{\"parsed\":{\"info\":{\"base\":\"9X6Sf3CCfFAfMCJcnAFnKgCDujkyb1Vu94HU94ZZ9zot\",\"lamports\":7002039280,\"newAccount\":\"4m45eqzd4bLiDA75CJArRDs6VLgrbNn2NtND2dCEvsMm\",\"owner\":\"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA\",\"seed\":\"GNkicAJDgLLfrFu1gbSNNMGyvghbJE2Z\",\"source\":\"9X6Sf3CCfFAfMCJcnAFnKgCDujkyb1Vu94HU94ZZ9zot\",\"space\":165},\"type\":\"createAccountWithSeed\"},\"program\":\"system\",\"programId\":\"11111111111111111111111111111111\",\"stackHeight\":null},{\"parsed\":{\"info\":{\"account\":\"4m45eqzd4bLiDA75CJArRDs6VLgrbNn2NtND2dCEvsMm\",\"mint\":\"So11111111111111111111111111111111111111112\",\"owner\":\"9X6Sf3CCfFAfMCJcnAFnKgCDujkyb1Vu94HU94ZZ9zot\",\"rentSysvar\":\"SysvarRent111111111111111111111111111111111\"},\"type\":\"initializeAccount\"},\"program\":\"spl-token\",\"programId\":\"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA\",\"stackHeight\":null},{\"accounts\":[\"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA\",\"ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL\",\"11111111111111111111111111111111\",\"SysvarRent111111111111111111111111111111111\",\"EjYMZgWhaETYCoxZ28cuPgzmEwLN2mGjqyWqx7beB1wf\",\"5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1\",\"VWWRQudSAuQ6jRb8kUh1SL5qezczHH67uZwGKTdRHqz\",\"EgQrt9pGPCgCQCyhj28owYPjR2YpZ9JNkpz379Amhrxc\",\"hJkRHwmMGeSJZrjzGaK2ZGgwJSEzWHvYTBt1EhWUrjB\",\"So11111111111111111111111111111111111111112\",\"DWaN95nLKTZhJEWtU7Q8JDigcoXtCUPZcbaRrENibiNs\",\"EzG9423XMkow45Fe3XaDerAKzQrJKyNic2NxAnPPr1Kf\",\"7cbVEBpRc6WP2gGhSFFhHRJ4AukDYkjSQ8dtLucFQ884\",\"9DCxsMizn3H1hprZ7xWe6LDzeUeZBksYFpBWBtSf1PQX\",\"7YttLkHDoNj9wyDur5pM1ejNaAvT9X4eqaYcHQqtj2G5\",\"srmqPvymJeFKQ4zGQed1GFppgkRHL9kaELCbyksJtPX\",\"8Wobfz55bpB8orA824sKpM9Kk6ipcjvCZ5qCYGfu5vfM\",\"9X6Sf3CCfFAfMCJcnAFnKgCDujkyb1Vu94HU94ZZ9zot\",\"BLCfjXQiXV2E75eCMAk2tpRQYmtej2zMK9PGUbn6fJHF\",\"4m45eqzd4bLiDA75CJArRDs6VLgrbNn2NtND2dCEvsMm\",\"9xhiwhtnRps6CLTPX7r78TNAajoepjBd4gCJR7RWEeqz\"],\"data\":\"4Yay71zj3ieHxdA37cXDR4QmMQjs2Dn3S3h\",\"programId\":\"675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8\",\"stackHeight\":null},{\"parsed\":{\"info\":{\"account\":\"4m45eqzd4bLiDA75CJArRDs6VLgrbNn2NtND2dCEvsMm\",\"destination\":\"9X6Sf3CCfFAfMCJcnAFnKgCDujkyb1Vu94HU94ZZ9zot\",\"owner\":\"9X6Sf3CCfFAfMCJcnAFnKgCDujkyb1Vu94HU94ZZ9zot\"},\"type\":\"closeAccount\"},\"program\":\"spl-token\",\"programId\":\"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA\",\"stackHeight\":null}],\"recentBlockhash\":\"68aKqvfY5cQdjjCcQyT23VdGGyP8Nr2i9UZLu9DbNgo9\"},\"signatures\":[\"3CqW9BpKfmkYqZ1jrDUn82i79vL6RPyPpBKwX2pdG42bx4Z4TGBmvfK1arbaJBam8AXsCeL7BUze1PKWHuCerpCQ\"]},\"version\":\"legacy\"}")

rpcMgr=rpcCallManager()
for each in get_any_value(txn,'owner'):
    input(rpcMgr.get_account_info(each[0]))
input(txn)
