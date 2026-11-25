import json
import re
from collections import Counter
from datetime import date, datetime, time
from decimal import Decimal
import base64
import pyodbc

def encode(v):
    if isinstance(v, (datetime, date, time)):
        return {'$type': type(v).__name__, 'value': v.isoformat()}
    if isinstance(v, Decimal):
        return {'$type': 'decimal', 'value': str(v)}
    if isinstance(v, (bytes, bytearray, memoryview)):
        return {'$type': 'bytes', 'value': base64.b64encode(v).decode('ascii')}
    raise TypeError(type(v).__name__)

def decode(v):
    if not isinstance(v, dict) or '$type' not in v: return v
    t, x = v['$type'], v['value']
    return {'datetime': datetime.fromisoformat, 'date': date.fromisoformat,
            'time': time.fromisoformat, 'decimal': Decimal,
            'bytes': base64.b64decode}[t](x)

def rows(cur, sql, *params):
    cur.execute(sql, *params)
    names = [c[0] for c in cur.description]
    return [dict(zip(names, r)) for r in cur.fetchall()]

def name_key(value):
    return value.strip().casefold() if isinstance(value, str) else ''


def existing_names(directory):
    names = set()
    for path in directory.rglob('*'):
        if not path.is_file() or path.suffix.lower() != '.json':
            continue
        try:
            data = json.loads(path.read_text(encoding='utf-8-sig'))
            tool = data.get('tool') or {}
            key = name_key(tool.get('TL_TOOL_DESCRIPTION') or data.get('nome'))
            if not key:
                raise ValueError('nome utensile mancante')
            names.add(key)
        except (OSError, ValueError, AttributeError, TypeError) as e:
            raise RuntimeError(f"Impossibile verificare i duplicati: {path}: {e}") from e
    return names


def nome_file(value):
    value = str(value or 'UTENSILE').replace('{95}', '_')
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', value).strip(' .')[:140].rstrip(' .')
    if not value:
        value = 'UTENSILE'
    if value.split('.')[0].upper() in {'CON','PRN','AUX','NUL', *[f'COM{i}' for i in range(1,10)], *[f'LPT{i}' for i in range(1,10)]}:
        value = '_' + value
    return value


TURNING = {0: 'TURN', 1: 'BORE', 2: 'INTERNAL GROOVE', 3: 'EXTERNAL GROOVE', 4: 'INTERNAL PARTING', 5: 'EXTERNAL PARTING', 6: 'INTERNAL THREAD', 7: 'EXTERNAL THREAD'}
MILLING = {0: 'END MILL', 1: 'BULL NOSE', 2: 'BALL NOSE', 3: 'SLOT DRILL', 4: 'CHAMFER MILL', 5: 'FACE MILL', 6: 'T-SLOT', 7: 'LOLLIPOP', 8: 'THREAD MILL', 9: 'CORNER ROUNDER', 10: 'DOVETAIL', 11: 'BARREL', 12: 'DOUBLE ANGLE'}
HOLE = {0: 'DRILL', 1: 'REAM', 2: 'TAP', 3: 'HOLE BORE', 4: 'COUNTERSINK', 5: 'CENTRE DRILL', 6: 'SPOT DRILL'}

SERVERS = [r'(localdb)\ECSQLEXPRESS', r'(localdb)\.\ECSQLEXPRESSSHARED']
FAMILIES = {
    'TURNING': (1, 'TL_TOOL_TYPE_TURN_ID', TURNING),
    'MILLING': (0, 'TL_TOOL_TYPE_MILL_ID', MILLING),
    'HOLE': (2, 'TL_TOOL_TYPE_HOLE_ID', HOLE),
}
pyodbc.pooling = False

def connect(database, server):
    def quote(v): return '{' + v.replace('}', '}}') + '}'
    return pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER='+quote(server)+';DATABASE='+quote(database)+';Trusted_Connection=yes;', timeout=5, autocommit=True)

def discover():
    found=[]; errors=[]
    for server in SERVERS:
        try:
            c=connect('master',server)
            try: names=[r[0] for r in c.cursor().execute("SELECT name FROM sys.databases WHERE database_id>4 AND state=0 AND HAS_DBACCESS(name)=1").fetchall()]
            finally: c.close()
            for name in names:
                try:
                    c=connect(name,server)
                    try:
                        cur=c.cursor()
                        cur.execute('SELECT TOP 0 TL_TOOL_ID, TL_TOOL_DESCRIPTION, TL_TOOL_CATEGORY_ID FROM dbo.TS_TOOL')
                        cur.execute('SELECT TOP 0 MNT_TOOL_ID FROM dbo.TS_MOUNTING')
                        found.append((name,server))
                    finally: c.close()
                except Exception as e: errors.append(f'{name}: {e}')
        except Exception as e: errors.append(f'{server}: {e}')
    if not found: raise RuntimeError('Nessun ToolStore leggibile trovato.\n'+'\n'.join(errors))
    return found

def export(database, server, selected, folders, log):
    # Verifica tutte le librerie selezionate prima di scrivere.
    indexes={f:existing_names(folders[f]) for f in selected}
    c=connect(database,server)
    total_new=total_skip=total_unknown=0
    try:
        cur=c.cursor()
        if cur.execute('SELECT DB_NAME()').fetchone()[0].casefold()!=database.casefold(): raise RuntimeError('Database sorgente non corrispondente')
        for family in selected:
            cat,col,mapping=FAMILIES[family]; output=folders[family]
            tools=rows(cur,'SELECT * FROM dbo.TS_TOOL WHERE TL_TOOL_CATEGORY_ID=? ORDER BY TL_TOOL_ID',cat)
            mounts=rows(cur,'SELECT M.* FROM dbo.TS_MOUNTING M JOIN dbo.TS_TOOL T ON T.TL_TOOL_ID=M.MNT_TOOL_ID WHERE T.TL_TOOL_CATEGORY_ID=? ORDER BY M.MNT_TOOL_ID,M.MNT_MOUNTING_ID',cat)
            by_id={}
            for m in mounts: by_id.setdefault(m['MNT_TOOL_ID'],[]).append(m)
            existing=indexes[family]; new=skip=unknown=0
            for category in mapping.values(): (output/category).mkdir(parents=True,exist_ok=True)
            occupied={(p.parent,p.name.casefold()) for p in output.rglob('*') if p.is_file()}
            for t in tools:
                if col not in t: raise RuntimeError('Colonna mancante: '+col)
                category=mapping.get(t[col]); name=t['TL_TOOL_DESCRIPTION']; key=name_key(name)
                if category is None:
                    unknown+=1; log(f'ESCLUSO (sottotipo non riconosciuto): {name}'); continue
                if not key: raise ValueError(f'Utensile senza nome: {t["TL_TOOL_ID"]}')
                if key in existing: skip+=1; log(f'SALTATO (nome già presente): {name}'); continue
                tid=t['TL_TOOL_ID']; code=t.get('TL_STANDARD_CODE'); ms=by_id.get(tid,[])
                t.pop('TL_TOOL_GRAPHIC_FILE',None); t['TL_SHANK_VISIBILITY']=True
                for m in ms: m.pop('MNT_TOOL_GRAPHIC_FILE',None)
                data=dict(versione=5,database=database,esportato_il=datetime.now().isoformat(),codice=code,nome=name,id_origine=tid,tool=t,mountings=ms)
                payload=json.dumps(data,ensure_ascii=False,indent=2,default=encode,allow_nan=False)
                directory=output/category; base=nome_file(name); candidate=base; n=1
                while (directory,(candidate+'.json').casefold()) in occupied:
                    candidate=f'{base}__{n}'; n+=1
                path=directory/(candidate+'.json')
                with path.open('x',encoding='utf-8') as out: out.write(payload)
                occupied.add((directory,path.name.casefold())); existing.add(key); new+=1
                log(f'ESPORTATO: {family} / {category} / {name} | montaggi: {len(ms)}')
            log(f'{family}: nuovi {new}, duplicati {skip}, esclusi {unknown}')
            total_new+=new; total_skip+=skip; total_unknown+=unknown
    finally: c.close()
    return f'Nuovi esportati: {total_new} | Duplicati saltati: {total_skip} | Sottotipi esclusi: {total_unknown}'
