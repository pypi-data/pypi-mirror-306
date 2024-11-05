from .solana_db_funcs import *
def get_test_run(multistring,tableName,kwargs={}):
    try:
        response = call_solcatcher_db_api(multistring,**kwargs)
        answr = ''#input('delete table?')
        if answr != '':
            data_brswr.delete_table(tableName)
    except Exception as e:
        print(f'{tableName} failed')
        return e
def get_from_defaults(column):
    fetched = fetchFromDb(tableName='defaultvalues', searchValue=column)
    if fetched is None:
        default = input(f"please input {column} default: ")
        insertintodefaultvalues(column, default,'defaultvalues')
    else:
        default = fetched[0]
    
    return default
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
