"""Esporta esclusivamente utensili HOLE ToolStore senza modificare SQL Server."""
import json
import re
from collections import Counter
from pathlib import Path
from datetime import date, datetime, time
from decimal import Decimal
import base64
import pyodbc

DATABASE = 'Sample_Toolstore_20231'
SERVERS = [r'(localdb)\ECSQLEXPRESS', r'(localdb)\.\ECSQLEXPRESSSHARED']
OUTPUT = Path(__file__).resolve().parent / 'LIBRERIA_UTENSILI' / 'LIBRERIA_FORATURA'

def connect():
    errors = []
    for server in SERVERS:
        try:
            c = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};'
                f'SERVER={server};DATABASE={DATABASE};Trusted_Connection=yes;', timeout=5)
            if c.cursor().execute('SELECT DB_NAME()').fetchone()[0].upper() != DATABASE.upper():
                c.close(); raise RuntimeError('Database non autorizzato')
            return c, server
        except pyodbc.Error as e:
            errors.append(f'{server}: {e}')
    raise RuntimeError('\n'.join(errors))

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

HOLE = {0: 'DRILL', 1: 'REAM', 2: 'TAP', 3: 'HOLE BORE', 4: 'COUNTERSINK', 5: 'CENTRE DRILL', 6: 'SPOT DRILL'}

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


def export():
    conn, server = connect()
    try:
        cur = conn.cursor()
        tools = rows(cur, '''SELECT * FROM dbo.TS_TOOL
            WHERE TL_TOOL_CATEGORY_ID = 2 AND TL_TOOL_TYPE_HOLE_ID BETWEEN 0 AND 6
            ORDER BY TL_STANDARD_CODE, TL_TOOL_ID''')
        mounts = rows(cur, '''SELECT M.* FROM dbo.TS_MOUNTING M
            JOIN dbo.TS_TOOL T ON T.TL_TOOL_ID=M.MNT_TOOL_ID
            WHERE T.TL_TOOL_CATEGORY_ID = 2 AND T.TL_TOOL_TYPE_HOLE_ID BETWEEN 0 AND 6
            ORDER BY M.MNT_TOOL_ID, M.MNT_MOUNTING_ID''')
        by_id = {}
        for m in mounts: by_id.setdefault(m['MNT_TOOL_ID'], []).append(m)
        models = [{'codice': t['TL_STANDARD_CODE'], 'nome': t['TL_TOOL_DESCRIPTION'],
                   'id_origine': t['TL_TOOL_ID'], 'tool': t,
                   'mountings': by_id.get(t['TL_TOOL_ID'], [])} for t in tools]
        # I modelli non devono contenere percorsi grafici del PC sorgente.
        for model in models:
            model['tool'].pop('TL_TOOL_GRAPHIC_FILE', None)
            model['tool']['TL_SHANK_VISIBILITY'] = True
            for mounting in model['mountings']:
                mounting.pop('MNT_TOOL_GRAPHIC_FILE', None)
        if not models:
            raise RuntimeError('Nessun utensile trovato. Libreria precedente non modificata.')
        OUTPUT.mkdir(parents=True, exist_ok=True)
        bases = [nome_file(m['codice'] or m['nome']) for m in models]
        categories = [HOLE[m['tool']['TL_TOOL_TYPE_HOLE_ID']] for m in models]
        for folder in HOLE.values():
            (OUTPUT / folder).mkdir(parents=True, exist_ok=True)
        print("Riepilogo categorie:", dict(Counter(categories)))
        counts = Counter((c, b.casefold()) for c,b in zip(categories,bases))
        existing = existing_names(OUTPUT)
        occupied = {(p.parent, p.name.casefold()) for p in OUTPUT.rglob('*') if p.is_file()}
        exported = skipped = 0
        for m, base, category in zip(models, bases, categories):
            key = name_key(m['nome'])
            if not key:
                raise ValueError(f"Utensile senza nome: ID {m['id_origine']}")
            if key in existing:
                skipped += 1
                print(f"SALTATO (nome già presente): {m['nome']}")
                continue
            directory = OUTPUT / category
            directory.mkdir(parents=True, exist_ok=True)
            if counts[(category, base.casefold())] > 1:
                base += f"__ID{m['id_origine']}"
            candidate = base
            n = 1
            while (directory, (candidate + '.json').casefold()) in occupied:
                candidate = f"{base}__{n}"
                n += 1
            path = directory / (candidate + '.json')
            data = {'versione': 4, 'database': DATABASE,
                    'esportato_il': datetime.now().isoformat(), **m}
            payload = json.dumps(data, ensure_ascii=False, indent=2,
                                 default=encode, allow_nan=False)
            # Modalità esclusiva: mai sovrascrivere un file esistente.
            with path.open('x', encoding='utf-8') as out:
                out.write(payload)
            occupied.add((directory, path.name.casefold()))
            existing.add(key)
            exported += 1
            print(f"{path.relative_to(OUTPUT)} | ID {m['id_origine']} | tipo: {category} | montaggi: {len(m['mountings'])}")
        print(f"Nuovi esportati: {exported} | Duplicati saltati: {skipped}")
        print(f"Server: {server}\nDatabase: {DATABASE}\nUtensili: {len(models)}\nMontaggi: {len(mounts)}\nCartella: {OUTPUT}")
        print('Grafica originale esclusa dai JSON esportati.')
        print('Database non modificato. Eventuali vecchi file non vengono cancellati.')
    finally:
        conn.close()

def nome_file(value):
    value = str(value or 'UTENSILE').replace('{95}', '_')
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', value).strip(' .')[:140].rstrip(' .')
    if not value:
        value = 'UTENSILE'
    if value.split('.')[0].upper() in {'CON','PRN','AUX','NUL', *[f'COM{i}' for i in range(1,10)], *[f'LPT{i}' for i in range(1,10)]}:
        value = '_' + value
    return value


def carica_modello(nome):
    path = (OUTPUT / nome).resolve()
    if not path.is_relative_to(OUTPUT.resolve()):
        raise ValueError("Percorso non valido")
    if path.suffix.lower() != '.json':
        raise ValueError('Selezionare un file JSON')
    return json.loads(path.read_text(encoding='utf-8'), object_hook=decode)


def carica_libreria():
    return [carica_modello(p.relative_to(OUTPUT)) for p in sorted(OUTPUT.glob('*/*.json'))]

if __name__ == '__main__':
    try:
        export()
    except Exception as e:
        print('ERRORE:', e)
    input('Premi INVIO per uscire...')
