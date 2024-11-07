from RupineLib.dbCode import connection as conn
from RupineLib.dbCode import directDBOperation as directOP
from RupineLib.dbCode import advancedDBOperation as advOP

def connect(user,pw,host,Port,database):
    return conn.connect(user,pw,host,Port,database)

def connectURI(connectionStr):
    return conn.connectURI(connectionStr)

def fetchDataInDatabase(sql:str, params:list, connection):
    return directOP.fetchDataInDatabase(sql,params,connection)

def insertDataIntoDatabase(sql:str, params:list, connection):    
    return directOP.insertDataIntoDatabase(sql,params,connection)
   
def insertBatchDataIntoDatabase(sql:str, params:list, connection):    
    return directOP.insertBatchDataIntoDatabase(sql,params,connection)

def insertBulkDataIntoDatabase(sql:str, template:str, params:list, connection):    
    return directOP.insertBulkDataIntoDatabase(sql, template, params, connection)

def insertBulkDataIntoDatabaseByCopyManager(tableAndSchema:str, columns:tuple, params:tuple, connection):    
    return directOP.insertBulkDataIntoDatabaseByCopyManager(tableAndSchema, columns, params, connection)  

def updatetBulkDataInDatabaseByCopyManager(schemaName:str,tableName:str, columns:tuple, params:tuple, updateSql:str, connection):    
    return directOP.updatetBulkDataInDatabaseByCopyManager(schemaName,tableName, columns, params, updateSql, connection)

def POST(connection, schema, tableName:str, data:dict, onConflict:bool=False, uniqueColumnNamesForConflict:str='id'):
    return advOP.POST(connection, schema, tableName, data, onConflict, uniqueColumnNamesForConflict)

def POST_BULK(connection, schema, tableName:str, data:list, byCopy = True, onConflict:bool=False, uniqueColumnNamesForConflict:str='id'):
    return advOP.POST_BULK(connection, schema, tableName, data, byCopy, onConflict, uniqueColumnNamesForConflict)

def PUT(connection, schema, updates:dict, tableName:str, conditions:dict={}):
    return advOP.PUT(connection, schema, updates, tableName, conditions)

def PUT_BULK(connection, schema, updates:list, tableName:str, conditionColumns:list=['id']):
    return advOP.PUT_BULK(connection, schema, updates, tableName, conditionColumns)

def SELECT(connection, schema, columns:list, tableName:str, conditions:dict={}):
    return advOP.SELECT(connection, schema, columns, tableName, conditions)

def SELECT_FUNCTION(connection, schema,functionName,functionParameter:list,columns:list=[]):
    return advOP.SELECT_FUNCTION(connection, schema,functionName,functionParameter,columns)

def DELETE(connection, schema, tableName:str, conditions:dict={}):
    return advOP.DELETE(connection, schema, tableName, conditions)

# Reuse docstrings
connect.__doc__ = conn.connect.__doc__
connectURI.__doc__ = conn.connectURI.__doc__
fetchDataInDatabase.__doc__ = directOP.fetchDataInDatabase.__doc__
insertDataIntoDatabase.__doc__ = directOP.insertDataIntoDatabase.__doc__
insertBatchDataIntoDatabase.__doc__ = directOP.insertBatchDataIntoDatabase.__doc__
insertBulkDataIntoDatabase.__doc__ = directOP.insertBulkDataIntoDatabase.__doc__
insertBulkDataIntoDatabaseByCopyManager.__doc__ = directOP.insertBulkDataIntoDatabaseByCopyManager.__doc__
updatetBulkDataInDatabaseByCopyManager.__doc__ = directOP.updatetBulkDataInDatabaseByCopyManager.__doc__
POST.__doc__ = advOP.POST.__doc__
POST_BULK.__doc__ = advOP.POST_BULK.__doc__
PUT.__doc__ = advOP.PUT.__doc__
PUT_BULK.__doc__ = advOP.PUT_BULK.__doc__
SELECT.__doc__ = advOP.SELECT.__doc__
SELECT_FUNCTION.__doc__ = advOP.SELECT_FUNCTION.__doc__
DELETE.__doc__ = advOP.DELETE.__doc__