import connect

# TODO we don't need SimpleQuery!

class SimpleQuery:
    '''
        Provides utilities to query the database 
        using 'SELECT ... FROM ... WHERE ...'
    '''
    def __init__(self):
        self.conn = connect.DBUtil().getExternalConnection()
        self.conn.jconn.setAutoCommit(False) 
        self.complete = None

    def queryDB(self, columns:str, table:str, condition:str):
        curs = self.conn.cursor()
        sql = f'SELECT {columns} FROM {table} WHERE {condition}'
        print('executing ', sql)
        curs.execute(sql)
        res = curs.fetchall()
        return res

    def customQuery(self, query: str):
        '''
            Executes a custom query to the database
        '''
        curs = self.conn.cursor()
        curs.execute(query)
        return curs.fetchall()

    def completion(self):
        self.complete = True

    def close(self):
        if self.conn is not None:
            try:
                if self.complete:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            except Exception as e:
                print(e)
            finally:
                try:
                    self.conn.close() 
                except Exception as e:
                    print(e)

def queryDB(columns: str, table: str, condition:str) -> list[tuple] | None:
    '''
        Convenience function to execute a simple "SELECT FROM WHERE" query to the database
        param columns: columns to SELECT
        param table: table to select FROM
        param condition: WHERE condition
    '''
    query = None
    try:
        query = SimpleQuery()
        res = query.queryDB(columns, table, condition)
    except Exception as e:
        print (e)
        return None
    finally:
        query.close() # type: ignore

    return res
    # res = []
    # db = connect.DBUtil()
    # with db.getExternalConnection() as conn:
    #     with conn.cursor() as curs:
    #         curs.execute(f'SELECT {columns} FROM {table} WHERE {condition}')
    #         res = curs.fetchall()

    # return res

    # TODO remove SimpleQuery & use connect directly instead
def customQueryDB(query: str) -> list[tuple] | None:
    '''
        Convenience function to execute a single query with the database.
        The query MUST be a SELECT query
        param query: the command string to execute
    '''
    db = None
    try:
        db = SimpleQuery()
        res = db.customQuery(query)
    except Exception as e:
        print (e)
        return None
    finally:
        db.close() # type: ignore

    return res
