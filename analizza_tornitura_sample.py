import pyodbc

DATABASE = 'Sample_Toolstore_20231'
SERVERS = [r'(localdb)\ECSQLEXPRESS', r'(localdb)\.\ECSQLEXPRESSSHARED']

def main():
    conn = None
    for server in SERVERS:
        try:
            conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};' + f'SERVER={server};DATABASE={DATABASE};Trusted_Connection=yes;', timeout=5, autocommit=True)
            print('CONNESSIONE RIUSCITA:', server)
            break
        except pyodbc.Error as e:
            print('Connessione non riuscita:', server, e)
    if conn is None:
        return
    try:
        cur = conn.cursor()
        print('\nDATABASE:', DATABASE)
        cur.execute('''SELECT TL_TOOL_CATEGORY_ID, TL_TOOL_TYPE_TURN_ID, COUNT(*) FROM dbo.TS_TOOL WHERE TL_TOOL_CATEGORY_ID = 1 GROUP BY TL_TOOL_CATEGORY_ID, TL_TOOL_TYPE_TURN_ID ORDER BY TL_TOOL_CATEGORY_ID, TL_TOOL_TYPE_TURN_ID''')
        groups = cur.fetchall()
        for cat, typ, count in groups:
            print(f'\nCATEGORIA: {cat} | TIPO TORNITURA: {typ} | NUMERO UTENSILI: {count}')
            sql = 'SELECT TOP 8 TL_TOOL_ID, TL_TOOL_DESCRIPTION FROM dbo.TS_TOOL WHERE TL_TOOL_CATEGORY_ID '
            params = []
            if cat is None:
                sql += 'IS NULL'
            else:
                sql += '= ?'; params.append(cat)
            sql += ' AND TL_TOOL_TYPE_TURN_ID '
            if typ is None:
                sql += 'IS NULL'
            else:
                sql += '= ?'; params.append(typ)
            cur.execute(sql + ' ORDER BY TL_TOOL_ID', *params)
            for tid, name in cur.fetchall():
                print(f'  ID: {tid} | {name}')
        print('\nANALISI COMPLETATA - NESSUN DATABASE MODIFICATO')
    except pyodbc.Error as e:
        print('ERRORE:', e)
    finally:
        conn.close()

if __name__ == '__main__':
    main()
    input('\nPremi INVIO per uscire...')
