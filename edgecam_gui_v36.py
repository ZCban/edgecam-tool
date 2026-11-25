import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import json, base64
import hashlib, re, uuid
import threading, queue
import time as clock
from datetime import datetime, date, time
from decimal import Decimal
import pyodbc

# Disable ODBC pooling before opening any connection.
pyodbc.pooling = False

DATABASE = 'TEST_PYTHON'
BACKUP_ROOT = Path(__file__).resolve().with_name('BACKUP_DATABASE')
BACKUP_KEEP = 30
OPTIONS_FILE = Path(__file__).resolve().with_name('EDGECAM_OPTIONS.json')

TRANSLATIONS = {'Importa utensili': {'it': 'Importa utensili', 'en': 'Import tools', 'es': 'Importar herramientas', 'fr': 'Importer les outils', 'de': 'Werkzeuge importieren', 'pt': 'Importar ferramentas'}, 'Destination Database': {'it': 'Destination Database', 'en': 'Destination Database', 'es': 'Base de datos de destino', 'fr': 'Base de données de destination', 'de': 'Zieldatenbank', 'pt': 'Banco de dados de destino'}, 'Aggiorna database': {'it': 'Aggiorna database', 'en': 'Refresh databases', 'es': 'Actualizar bases de datos', 'fr': 'Actualiser les bases', 'de': 'Datenbanken aktualisieren', 'pt': 'Atualizar bancos'}, 'Ripristina backup...': {'it': 'Ripristina backup...', 'en': 'Restore backup...', 'es': 'Restaurar copia...', 'fr': 'Restaurer la sauvegarde...', 'de': 'Sicherung wiederherstellen...', 'pt': 'Restaurar backup...'}, 'Cartella libreria...': {'it': 'Cartella libreria...', 'en': 'Library folder...', 'es': 'Carpeta de biblioteca...', 'fr': 'Dossier bibliothèque...', 'de': 'Bibliotheksordner...', 'pt': 'Pasta da biblioteca...'}, 'Aggiorna elenco': {'it': 'Aggiorna elenco', 'en': 'Refresh list', 'es': 'Actualizar lista', 'fr': 'Actualiser la liste', 'de': 'Liste aktualisieren', 'pt': 'Atualizar lista'}, 'Sottocategoria di tornitura': {'it': 'Sottocategoria di tornitura', 'en': 'Turning category', 'es': 'Categoría de torneado', 'fr': 'Catégorie de tournage', 'de': 'Drehkategorie', 'pt': 'Categoria de torneamento'}, 'Spunta gli utensili da inserire; clicca sul nome per scegliere Graphic': {'it': 'Spunta gli utensili da inserire; clicca sul nome per scegliere Graphic', 'en': 'Check tools to insert; click a name to choose Graphic', 'es': 'Marca las herramientas; pulsa el nombre para elegir Graphic', 'fr': 'Cochez les outils ; cliquez sur le nom pour choisir Graphic', 'de': 'Werkzeuge markieren; Namen für Graphic anklicken', 'pt': 'Marque as ferramentas; clique no nome para escolher Graphic'}, 'Seleziona tutto': {'it': 'Seleziona tutto', 'en': 'Select all', 'es': 'Seleccionar todo', 'fr': 'Tout sélectionner', 'de': 'Alles auswählen', 'pt': 'Selecionar tudo'}, 'Deseleziona tutto': {'it': 'Deseleziona tutto', 'en': 'Deselect all', 'es': 'Deseleccionar todo', 'fr': 'Tout désélectionner', 'de': 'Auswahl aufheben', 'pt': 'Desmarcar tudo'}, 'Categoria': {'it': 'Categoria', 'en': 'Category', 'es': 'Categoría', 'fr': 'Catégorie', 'de': 'Kategorie', 'pt': 'Categoria'}, 'Utensile': {'it': 'Utensile', 'en': 'Tool', 'es': 'Herramienta', 'fr': 'Outil', 'de': 'Werkzeug', 'pt': 'Ferramenta'}, 'Graphic per utensile...': {'it': 'Graphic per utensile...', 'en': 'Graphic per tool...', 'es': 'Graphic por herramienta...', 'fr': 'Graphic par outil...', 'de': 'Graphic pro Werkzeug...', 'pt': 'Graphic por ferramenta...'}, 'Rimuovi Graphic': {'it': 'Rimuovi Graphic', 'en': 'Remove Graphic', 'es': 'Quitar Graphic', 'fr': 'Retirer Graphic', 'de': 'Graphic entfernen', 'pt': 'Remover Graphic'}, 'Graphic opzionale: seleziona un solo utensile per assegnargli un file.': {'it': 'Graphic opzionale: seleziona un solo utensile per assegnargli un file.', 'en': 'Optional Graphic: select one tool to assign a file.', 'es': 'Graphic opcional: selecciona una herramienta para asignar un archivo.', 'fr': 'Graphic facultatif : sélectionnez un outil pour attribuer un fichier.', 'de': 'Optionales Graphic: ein Werkzeug für die Dateizuordnung auswählen.', 'pt': 'Graphic opcional: selecione uma ferramenta para atribuir um arquivo.'}, 'Salta utensili duplicati': {'it': 'Salta utensili duplicati', 'en': 'Skip duplicate tools', 'es': 'Omitir herramientas duplicadas', 'fr': 'Ignorer les outils en double', 'de': 'Doppelte Werkzeuge überspringen', 'pt': 'Ignorar ferramentas duplicadas'}, 'Backup automatico': {'it': 'Backup automatico', 'en': 'Automatic backup', 'es': 'Copia automática', 'fr': 'Sauvegarde automatique', 'de': 'Automatische Sicherung', 'pt': 'Backup automático'}, 'Opzioni': {'it': 'Opzioni', 'en': 'Options', 'es': 'Opciones', 'fr': 'Options', 'de': 'Optionen', 'pt': 'Opções'}, 'Lingua': {'it': 'Lingua', 'en': 'Language', 'es': 'Idioma', 'fr': 'Langue', 'de': 'Sprache', 'pt': 'Idioma'}, 'Verifica connessione': {'it': 'Verifica connessione', 'en': 'Test connection', 'es': 'Probar conexión', 'fr': 'Tester la connexion', 'de': 'Verbindung prüfen', 'pt': 'Testar conexão'}, 'Inserisci selezionati': {'it': 'Inserisci selezionati', 'en': 'Insert selected tools', 'es': 'Insertar seleccionadas', 'fr': 'Insérer les outils sélectionnés', 'de': 'Ausgewählte Werkzeuge einfügen', 'pt': 'Inserir selecionadas'}, 'Risultato': {'it': 'Risultato', 'en': 'Result', 'es': 'Resultado', 'fr': 'Résultat', 'de': 'Ergebnis', 'pt': 'Resultado'}, 'Errore': {'it': 'Errore', 'en': 'Error', 'es': 'Error', 'fr': 'Erreur', 'de': 'Fehler', 'pt': 'Erro'}, 'Operazione non riuscita': {'it': 'Operazione non riuscita', 'en': 'Operation failed', 'es': 'Operación fallida', 'fr': 'Échec de l’opération', 'de': 'Vorgang fehlgeschlagen', 'pt': 'Falha na operação'}, 'Operazione in corso': {'it': 'Operazione in corso', 'en': 'Operation in progress', 'es': 'Operación en curso', 'fr': 'Opération en cours', 'de': 'Vorgang läuft', 'pt': 'Operação em andamento'}, 'Attendi il completamento della transazione SQL.': {'it': 'Attendi il completamento della transazione SQL.', 'en': 'Wait for the SQL transaction to finish.', 'es': 'Espera a que termine la transacción SQL.', 'fr': 'Attendez la fin de la transaction SQL.', 'de': 'SQL-Transaktion abwarten.', 'pt': 'Aguarde o fim da transação SQL.'}, 'Clicca sul nome di un utensile.': {'it': 'Clicca sul nome di un utensile.', 'en': 'Click a tool name.', 'es': 'Pulsa el nombre de una herramienta.', 'fr': 'Cliquez sur le nom d’un outil.', 'de': 'Werkzeugnamen anklicken.', 'pt': 'Clique no nome de uma ferramenta.'}, 'Seleziona il database di destinazione.': {'it': 'Seleziona il database di destinazione.', 'en': 'Select the destination database.', 'es': 'Selecciona la base de datos de destino.', 'fr': 'Sélectionnez la base de destination.', 'de': 'Zieldatenbank auswählen.', 'pt': 'Selecione o banco de destino.'}, 'Ripristina backup': {'it': 'Ripristina backup', 'en': 'Restore backup', 'es': 'Restaurar copia', 'fr': 'Restaurer la sauvegarde', 'de': 'Sicherung wiederherstellen', 'pt': 'Restaurar backup'}, 'Seleziona una versione. Chiudi EDGECAM prima del ripristino.': {'it': 'Seleziona una versione. Chiudi EDGECAM prima del ripristino.', 'en': 'Select a version. Close EDGECAM before restoring.', 'es': 'Selecciona una versión. Cierra EDGECAM antes de restaurar.', 'fr': 'Sélectionnez une version. Fermez EDGECAM avant la restauration.', 'de': 'Version auswählen. EDGECAM vor Wiederherstellung schließen.', 'pt': 'Selecione uma versão. Feche EDGECAM antes de restaurar.'}, 'Emergenza': {'it': 'Emergenza', 'en': 'Emergency', 'es': 'Emergencia', 'fr': 'Urgence', 'de': 'Notfall', 'pt': 'Emergência'}, 'Automatico': {'it': 'Automatico', 'en': 'Automatic', 'es': 'Automático', 'fr': 'Automatique', 'de': 'Automatisch', 'pt': 'Automático'}, 'Conferma ripristino': {'it': 'Conferma ripristino', 'en': 'Confirm restore', 'es': 'Confirmar restauración', 'fr': 'Confirmer la restauration', 'de': 'Wiederherstellung bestätigen', 'pt': 'Confirmar restauração'}, 'Conferma definitiva': {'it': 'Conferma definitiva', 'en': 'Final confirmation', 'es': 'Confirmación final', 'fr': 'Confirmation finale', 'de': 'Endgültige Bestätigung', 'pt': 'Confirmação final'}, 'Ripristina versione selezionata': {'it': 'Ripristina versione selezionata', 'en': 'Restore selected version', 'es': 'Restaurar versión seleccionada', 'fr': 'Restaurer la version sélectionnée', 'de': 'Ausgewählte Version wiederherstellen', 'pt': 'Restaurar versão selecionada'}, 'Annulla': {'it': 'Annulla', 'en': 'Cancel', 'es': 'Cancelar', 'fr': 'Annuler', 'de': 'Abbrechen', 'pt': 'Cancelar'}, 'Modelli': {'it': 'Modelli', 'en': 'Templates', 'es': 'Modelos', 'fr': 'Modèles', 'de': 'Vorlagen', 'pt': 'Modelos'}, 'Seleziona almeno un utensile': {'it': 'Seleziona almeno un utensile', 'en': 'Select at least one tool', 'es': 'Selecciona al menos una herramienta', 'fr': 'Sélectionnez au moins un outil', 'de': 'Mindestens ein Werkzeug auswählen', 'pt': 'Selecione pelo menos uma ferramenta'}, 'Conferma inserimento': {'it': 'Conferma inserimento', 'en': 'Confirm insertion', 'es': 'Confirmar inserción', 'fr': 'Confirmer l’insertion', 'de': 'Einfügen bestätigen', 'pt': 'Confirmar inserção'}, 'Un backup prima del lotto.': {'it': 'Un backup prima del lotto.', 'en': 'One backup before the batch.', 'es': 'Una copia antes del lote.', 'fr': 'Une sauvegarde avant le lot.', 'de': 'Eine Sicherung vor dem Stapel.', 'pt': 'Um backup antes do lote.'}, 'ATTENZIONE: backup automatico DISATTIVATO. Nessuna copia di sicurezza prima del lotto.': {'it': 'ATTENZIONE: backup automatico DISATTIVATO. Nessuna copia di sicurezza prima del lotto.', 'en': 'WARNING: automatic backup OFF. No backup before the batch.', 'es': 'ATENCIÓN: copia automática DESACTIVADA. Sin copia antes del lote.', 'fr': 'ATTENTION : sauvegarde automatique DÉSACTIVÉE. Aucune sauvegarde avant le lot.', 'de': 'ACHTUNG: automatische Sicherung AUS. Keine Sicherung vor dem Stapel.', 'pt': 'ATENÇÃO: backup automático DESATIVADO. Sem backup antes do lote.'}, '{n} selezionati': {'it': '{n} selezionati', 'en': '{n} selected', 'es': '{n} seleccionadas', 'fr': '{n} sélectionnés', 'de': '{n} ausgewählt', 'pt': '{n} selecionadas'}, '{n} grafiche assegnate nella libreria': {'it': '{n} grafiche assegnate nella libreria', 'en': '{n} graphics assigned in library', 'es': '{n} gráficos asignados', 'fr': '{n} graphiques attribués', 'de': '{n} Grafiken zugeordnet', 'pt': '{n} gráficos atribuídos'}}
LANGUAGES = {'it':'Italiano','en':'English','es':'Español','fr':'Français','de':'Deutsch','pt':'Português'}
TRANSLATIONS.update({'Destinazione': {'it': 'Destinazione', 'en': 'Destination', 'es': 'Destino', 'fr': 'Destination', 'de': 'Ziel', 'pt': 'Destino'}, 'Utensili selezionati': {'it': 'Utensili selezionati', 'en': 'Selected tools', 'es': 'Herramientas seleccionadas', 'fr': 'Outils sélectionnés', 'de': 'Ausgewählte Werkzeuge', 'pt': 'Ferramentas selecionadas'}, 'Confermi?': {'it': 'Confermi?', 'en': 'Do you want to proceed?', 'es': '¿Deseas continuar?', 'fr': 'Voulez-vous continuer ?', 'de': 'Möchten Sie fortfahren?', 'pt': 'Deseja continuar?'}, 'Conferma': {'it': 'Conferma', 'en': 'Confirm', 'es': 'Confirmar', 'fr': 'Confirmer', 'de': 'Bestätigen', 'pt': 'Confirmar'}})
TRANSLATIONS.update({'Attivo': dict(zip(('it','en','es','fr','de','pt'), ('Attivo','Enabled','Activado','Activé','Aktiviert','Ativado'))), 'Disattivato': dict(zip(('it','en','es','fr','de','pt'), ('Disattivato','Disabled','Desactivado','Désactivé','Deaktiviert','Desativado')))})

LANG = 'it'
def tr(key):
    return TRANSLATIONS.get(key, {}).get(LANG, key)


LOG_ROWS = [('Connessione riuscita: ', 'Connection successful: ', 'Conexión correcta: ', 'Connexion réussie : ', 'Verbindung erfolgreich: ', 'Conexão bem-sucedida: '), ('Verifica backup selezionato...', 'Checking selected backup...', 'Verificando copia seleccionada...', 'Vérification de la sauvegarde...', 'Sicherung wird geprüft...', 'Verificando backup selecionado...'), ('Backup di emergenza dello stato attuale...', 'Backing up current state...', 'Guardando estado actual...', 'Sauvegarde de l’état actuel...', 'Aktueller Zustand wird gesichert...', 'Salvando estado atual...'), ('Backup di emergenza verificato: ', 'Emergency backup verified: ', 'Copia de emergencia verificada: ', 'Sauvegarde d’urgence vérifiée : ', 'Notfallsicherung geprüft: ', 'Backup de emergência verificado: '), ('Chiusura connessioni attive e ripristino...', 'Closing active connections and restoring...', 'Cerrando conexiones y restaurando...', 'Fermeture des connexions et restauration...', 'Verbindungen werden geschlossen und Sicherung wiederhergestellt...', 'Fechando conexões e restaurando...'), ('Ripristino completato; riapertura database...', 'Restore completed; reopening database...', 'Restauración completada; reabriendo base...', 'Restauration terminée ; réouverture...', 'Wiederherstellung abgeschlossen; Datenbank wird geöffnet...', 'Restauração concluída; reabrindo banco...'), ('Ripristino riuscito.', 'Restore successful.', 'Restauración correcta.', 'Restauration réussie.', 'Wiederherstellung erfolgreich.', 'Restauração bem-sucedida.'), ('Backup di emergenza: ', 'Emergency backup: ', 'Copia de emergencia: ', 'Sauvegarde d’urgence : ', 'Notfallsicherung: ', 'Backup de emergência: '), ('Nuova connessione SQL: tentativo ', 'New SQL connection: attempt ', 'Nueva conexión SQL: intento ', 'Nouvelle connexion SQL : tentative ', 'Neue SQL-Verbindung: Versuch ', 'Nova conexão SQL: tentativa '), ('Database ONLINE / MULTI_USER; tabelle ToolStore accessibili.', 'Database ONLINE / MULTI_USER; ToolStore tables accessible.', 'Base ONLINE / MULTI_USER; tablas ToolStore accesibles.', 'Base ONLINE / MULTI_USER ; tables ToolStore accessibles.', 'Datenbank ONLINE / MULTI_USER; ToolStore-Tabellen zugänglich.', 'Banco ONLINE / MULTI_USER; tabelas ToolStore acessíveis.'), ('Backup completo prima del lotto...', 'Full backup before batch...', 'Copia completa antes del lote...', 'Sauvegarde complète avant le lot...', 'Vollsicherung vor dem Stapel...', 'Backup completo antes do lote...'), ('Backup verificato: ', 'Backup verified: ', 'Copia verificada: ', 'Sauvegarde vérifiée : ', 'Sicherung geprüft: ', 'Backup verificado: '), ('Avviso pulizia backup: ', 'Backup cleanup warning: ', 'Aviso de limpieza: ', 'Avertissement de nettoyage : ', 'Warnung zur Sicherungsbereinigung: ', 'Aviso de limpeza: '), ('Backup automatico disattivato: inserimento senza nuova copia di sicurezza.', 'Automatic backup disabled: inserting without a new backup.', 'Copia automática desactivada: inserción sin nueva copia.', 'Sauvegarde automatique désactivée : insertion sans nouvelle sauvegarde.', 'Automatische Sicherung deaktiviert: Einfügen ohne neue Sicherung.', 'Backup automático desativado: inserção sem novo backup.'), ('Duplicato: ', 'Duplicate: ', 'Duplicado: ', 'Doublon : ', 'Duplikat: ', 'Duplicado: '), ('Rollback dell’intero lotto eseguito.', 'Entire batch rolled back.', 'Lote completo revertido.', 'Lot entier annulé.', 'Gesamter Stapel zurückgesetzt.', 'Lote inteiro revertido.'), ('Backup conservato: ', 'Backup retained: ', 'Copia conservada: ', 'Sauvegarde conservée : ', 'Sicherung behalten: ', 'Backup preservado: '), ('Inserimento completato: {a} utensili; duplicati saltati: {b}.', 'Insertion completed: {a} tools; duplicates skipped: {b}.', 'Inserción completada: {a} herramientas; duplicados omitidos: {b}.', 'Insertion terminée : {a} outils ; doublons ignorés : {b}.', 'Einfügen abgeschlossen: {a} Werkzeuge; Duplikate übersprungen: {b}.', 'Inserção concluída: {a} ferramentas; duplicados ignorados: {b}.'), ('Nessun inserimento necessario. Duplicati saltati: {a}', 'No insertion needed. Duplicates skipped: {a}', 'No se requiere inserción. Duplicados omitidos: {a}', 'Aucune insertion nécessaire. Doublons ignorés : {a}', 'Kein Einfügen nötig. Duplikate übersprungen: {a}', 'Nenhuma inserção necessária. Duplicados ignorados: {a}'), ('Verificato {a}, nuovo ID {b}', 'Verified {a}, new ID {b}', 'Verificado {a}, nuevo ID {b}', 'Vérifié {a}, nouvel ID {b}', '{a} geprüft, neue ID {b}', 'Verificado {a}, novo ID {b}')]

def translate_log(text):
    def line_translate(line):
        if line in TRANSLATIONS:
            return tr(line)
        for row in LOG_ROWS:
            source=row[0]; target=row[list(LANGUAGES).index(LANG)]
            if '{a}' in source:
                pattern=re.escape(source).replace(r'\{a\}', '(?P<a>.+?)').replace(r'\{b\}', '(?P<b>.+?)')
                match=re.fullmatch(pattern,line)
                if match: return target.format(**match.groupdict())
            elif source.endswith(' ') and line.startswith(source):
                return target+line[len(source):]
            elif line==source: return target
        return line
    return '\n'.join(line_translate(line) for line in text.split('\n'))


THEMES = {
    'original': None,
    'black': ('#121212','#ffffff','#252525','#555555','#2563eb'),
}
THEME_ROWS = [
 ('Tema interfaccia','Interface theme','Tema de interfaz','Thème de l’interface','Oberflächendesign','Tema da interface'),
 ('Originale','Original','Original','Original','Original','Original'),
 ('Nero','Black','Negro','Noir','Schwarz','Preto'),
]
THEME_KEYS = dict(zip(THEMES, [r[0] for r in THEME_ROWS[1:]]))
for row in THEME_ROWS:
    TRANSLATIONS[row[0]] = dict(zip(LANGUAGES,row))

def load_options():
    try:
        data = json.loads(OPTIONS_FILE.read_text(encoding='utf-8'))
        return {**{k: data[k] if isinstance(data.get(k), bool) else True for k in ('skip_duplicates', 'auto_backup')}, 'theme': data.get('theme') if data.get('theme') in THEMES else 'original', 'language': data.get('language') if data.get('language') in LANGUAGES else 'it'}
    except (OSError, ValueError, TypeError, AttributeError):
        return {'skip_duplicates': True, 'auto_backup': True, 'language':'it', 'theme':'original'}

SERVERS = [r'(localdb)\.\ECSQLEXPRESSSHARED', r'(localdb)\ECSQLEXPRESS']
TRANSLATIONS.update({'TURNING': {'it': 'Tornitura', 'en': 'Turning', 'es': 'Torneado', 'fr': 'Tournage', 'de': 'Drehen', 'pt': 'Torneamento'}, 'MILLING': {'it': 'Fresatura', 'en': 'Milling', 'es': 'Fresado', 'fr': 'Fraisage', 'de': 'Fräsen', 'pt': 'Fresagem'}, 'HOLE': {'it': 'Foratura', 'en': 'Hole', 'es': 'Taladrado', 'fr': 'Perçage', 'de': 'Bohren', 'pt': 'Furação'}, 'ALL': {'it': 'Tutte', 'en': 'ALL', 'es': 'Todas', 'fr': 'Toutes', 'de': 'Alle', 'pt': 'Todas'}, 'TURN': {'it': 'Tornitura esterna', 'en': 'TURN', 'es': 'Torneado exterior', 'fr': 'Tournage extérieur', 'de': 'Außendrehen', 'pt': 'Torneamento externo'}, 'BORE': {'it': 'Barenatura', 'en': 'BORE', 'es': 'Mandrinado', 'fr': 'Alésage', 'de': 'Ausdrehen', 'pt': 'Mandrilamento'}, 'INTERNAL GROOVE': {'it': 'Gole interne', 'en': 'INTERNAL GROOVE', 'es': 'Ranurado interior', 'fr': 'Gorge intérieure', 'de': 'Innenstechen', 'pt': 'Canal interno'}, 'EXTERNAL GROOVE': {'it': 'Gole esterne', 'en': 'EXTERNAL GROOVE', 'es': 'Ranurado exterior', 'fr': 'Gorge extérieure', 'de': 'Außenstechen', 'pt': 'Canal externo'}, 'INTERNAL PARTING': {'it': 'Troncatura interna', 'en': 'INTERNAL PARTING', 'es': 'Tronzado interior', 'fr': 'Tronçonnage intérieur', 'de': 'Innenabstechen', 'pt': 'Corte interno'}, 'EXTERNAL PARTING': {'it': 'Troncatura esterna', 'en': 'EXTERNAL PARTING', 'es': 'Tronzado exterior', 'fr': 'Tronçonnage extérieur', 'de': 'Außenabstechen', 'pt': 'Corte externo'}, 'INTERNAL THREAD': {'it': 'Filettatura interna', 'en': 'INTERNAL THREAD', 'es': 'Roscado interior', 'fr': 'Filetage intérieur', 'de': 'Innengewinde', 'pt': 'Rosca interna'}, 'EXTERNAL THREAD': {'it': 'Filettatura esterna', 'en': 'EXTERNAL THREAD', 'es': 'Roscado exterior', 'fr': 'Filetage extérieur', 'de': 'Außengewinde', 'pt': 'Rosca externa'}, 'END MILL': {'it': 'Fresa cilindrica', 'en': 'END MILL', 'es': 'Fresa cilíndrica', 'fr': 'Fraise cylindrique', 'de': 'Schaftfräser', 'pt': 'Fresa cilíndrica'}, 'BULL NOSE': {'it': 'Fresa torica', 'en': 'BULL NOSE', 'es': 'Fresa tórica', 'fr': 'Fraise torique', 'de': 'Torusfräser', 'pt': 'Fresa toroidal'}, 'BALL NOSE': {'it': 'Fresa sferica', 'en': 'BALL NOSE', 'es': 'Fresa esférica', 'fr': 'Fraise sphérique', 'de': 'Kugelfräser', 'pt': 'Fresa esférica'}, 'SLOT DRILL': {'it': 'Fresa a due taglienti', 'en': 'SLOT DRILL', 'es': 'Fresa de dos labios', 'fr': 'Fraise deux tailles', 'de': 'Zweischneider', 'pt': 'Fresa de dois cortes'}, 'CHAMFER MILL': {'it': 'Fresa per smussi', 'en': 'CHAMFER MILL', 'es': 'Fresa de chaflán', 'fr': 'Fraise à chanfreiner', 'de': 'Fasenfräser', 'pt': 'Fresa de chanfro'}, 'FACE MILL': {'it': 'Fresa a spianare', 'en': 'FACE MILL', 'es': 'Fresa de planear', 'fr': 'Fraise à surfacer', 'de': 'Planfräser', 'pt': 'Fresa de facear'}, 'T-SLOT': {'it': 'Fresa per cave a T', 'en': 'T-SLOT', 'es': 'Fresa de ranura en T', 'fr': 'Fraise à rainure en T', 'de': 'T-Nutenfräser', 'pt': 'Fresa de ranhura em T'}, 'LOLLIPOP': {'it': 'Fresa a lecca-lecca', 'en': 'LOLLIPOP', 'es': 'Fresa de bola invertida', 'fr': 'Fraise sucette', 'de': 'Lollipopfräser', 'pt': 'Fresa pirulito'}, 'THREAD MILL': {'it': 'Fresa per filetti', 'en': 'THREAD MILL', 'es': 'Fresa de roscar', 'fr': 'Fraise à fileter', 'de': 'Gewindefräser', 'pt': 'Fresa de roscar'}, 'CORNER ROUNDER': {'it': 'Fresa per raggi', 'en': 'CORNER ROUNDER', 'es': 'Fresa de radio', 'fr': 'Fraise à rayon', 'de': 'Radiusfräser', 'pt': 'Fresa de raio'}, 'DOVETAIL': {'it': 'Fresa a coda di rondine', 'en': 'DOVETAIL', 'es': 'Cola de milano', 'fr': 'Fraise queue d’aronde', 'de': 'Schwalbenschwanzfräser', 'pt': 'Fresa cauda de andorinha'}, 'BARREL': {'it': 'Fresa a barile', 'en': 'BARREL', 'es': 'Fresa de barril', 'fr': 'Fraise tonneau', 'de': 'Tonnenfräser', 'pt': 'Fresa barril'}, 'DOUBLE ANGLE': {'it': 'Fresa a doppio angolo', 'en': 'DOUBLE ANGLE', 'es': 'Fresa de doble ángulo', 'fr': 'Fraise à double angle', 'de': 'Doppelwinkelfräser', 'pt': 'Fresa de duplo ângulo'}, 'DRILL': {'it': 'Punte', 'en': 'DRILL', 'es': 'Brocas', 'fr': 'Forets', 'de': 'Bohrer', 'pt': 'Brocas'}, 'REAM': {'it': 'Alesatori', 'en': 'REAM', 'es': 'Escariadores', 'fr': 'Alésoirs', 'de': 'Reibahlen', 'pt': 'Alargadores'}, 'TAP': {'it': 'Maschi', 'en': 'TAP', 'es': 'Machos', 'fr': 'Tarauds', 'de': 'Gewindebohrer', 'pt': 'Machos'}, 'HOLE BORE': {'it': 'Barenatori', 'en': 'HOLE BORE', 'es': 'Mandrinado', 'fr': 'Barres d’alésage', 'de': 'Bohrstangen', 'pt': 'Mandriladores'}, 'COUNTERSINK': {'it': 'Svasatori', 'en': 'COUNTERSINK', 'es': 'Avellanadores', 'fr': 'Fraises à chanfreiner', 'de': 'Kegelsenker', 'pt': 'Escareadores'}, 'CENTRE DRILL': {'it': 'Punte da centro', 'en': 'CENTRE DRILL', 'es': 'Brocas de centro', 'fr': 'Forets à centrer', 'de': 'Zentrierbohrer', 'pt': 'Brocas de centro'}, 'SPOT DRILL': {'it': 'Punte da centratura', 'en': 'SPOT DRILL', 'es': 'Brocas de puntear', 'fr': 'Forets à pointer', 'de': 'NC-Anbohrer', 'pt': 'Brocas de ponto'}, 'Famiglia utensili': {'it': 'Famiglia utensili', 'en': 'Tool family', 'es': 'Familia de herramientas', 'fr': 'Famille d’outils', 'de': 'Werkzeugfamilie', 'pt': 'Família de ferramentas'}, 'Sottocategoria': {'it': 'Sottocategoria', 'en': 'Subcategory', 'es': 'Subcategoría', 'fr': 'Sous-catégorie', 'de': 'Unterkategorie', 'pt': 'Subcategoria'}})
LIBRARY_ROOT = Path(__file__).resolve().parent / 'LIBRERIA_UTENSILI'
LIBRARY = LIBRARY_ROOT / 'LIBRERIA_TORNITURA'
CATEGORY_ORDER = ['TURN', 'BORE', 'INTERNAL GROOVE', 'EXTERNAL GROOVE', 'INTERNAL PARTING', 'EXTERNAL PARTING', 'INTERNAL THREAD', 'EXTERNAL THREAD']
EXCLUDE = {'TL_TOOL_ID','TL_CREATED','TL_MODIFIED','MNT_MOUNTING_ID','MNT_UNIQUE_CONSTRAINT','MNT_CREATED','MNT_MODIFIED','MNT_GAUGE_X','MNT_GAUGE_Y','MNT_GAUGE_Z','MNT_X_OFFSET','MNT_Y_OFFSET','MNT_Z_OFFSET'}

def decode(v):
    if '$type' not in v: return v
    return {'datetime':datetime.fromisoformat,'date':date.fromisoformat,'time':time.fromisoformat,'decimal':Decimal,'bytes':base64.b64decode}[v['$type']](v['value'])

def connect(database, server, autocommit=False):
    # ODBC brace quoting protects database names containing punctuation.
    db = '{' + database.replace('}', '}}') + '}'
    c=pyodbc.connect('DRIVER={SQL Server Native Client 11.0};'+f'SERVER={server};DATABASE={db};Trusted_Connection=yes;',timeout=5,autocommit=autocommit)
    try:
        if c.cursor().execute('SELECT DB_NAME()').fetchone()[0].casefold()!=database.casefold():
            raise RuntimeError('Database di destinazione non corrispondente')
        return c
    except Exception:
        c.close(); raise

def backup_directory(database, server):
    # Separate identical database names on different SQL instances.
    safe = re.sub(r'[^A-Za-z0-9_-]', '_', database)[:80] or 'database'
    key = hashlib.sha256((server.casefold() + '|' + database.casefold()).encode()).hexdigest()[:12]
    return BACKUP_ROOT / (safe + '_' + key)

def sql_identifier(name):
    return '[' + name.replace(']', ']]') + ']'

def drain(cursor):
    # BACKUP/RESTORE can return multiple results and informational messages.
    while cursor.nextset():
        pass

def backup_database(database, server, emergency=False):
    folder = backup_directory(database, server)
    if emergency: folder = folder / 'EMERGENCY'
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    stem = ('SAFETY_' if emergency else 'AUTO_') + stamp + '_' + uuid.uuid4().hex[:12]
    pending = folder / (stem + '.pending')
    final = folder / (stem + '.bak')
    c = connect(database, server, autocommit=True)
    try:
        c.timeout = 0
        cur = c.cursor()
        cur.execute('BACKUP DATABASE ' + sql_identifier(database) +
                    ' TO DISK = ? WITH COPY_ONLY, CHECKSUM, INIT', str(pending))
        drain(cur)
        cur.execute('RESTORE VERIFYONLY FROM DISK = ? WITH CHECKSUM', str(pending))
        drain(cur)
        # Publish only after SQL verification; incomplete backups are never rotated.
        pending.rename(final)
    finally:
        c.close()
    return final

def rotate_backups(folder):
    pattern = re.compile(r'AUTO_\d{8}_\d{6}_\d{6}_[0-9a-f]{12}\.bak')
    files = sorted((p for p in folder.iterdir() if p.is_file() and pattern.fullmatch(p.name)),
                   key=lambda p: p.name, reverse=True)
    removed = 0
    for p in files[BACKUP_KEEP:]:
        p.unlink()
        removed += 1
    return removed

def discover():
    found=[]; errors=[]
    for server in SERVERS:
        try:
            with connect('master',server) as c:
                names=[r[0] for r in c.cursor().execute("SELECT name FROM sys.databases WHERE database_id > 4 AND state=0 AND is_read_only=0 AND HAS_DBACCESS(name)=1").fetchall()]
            c.close()
            for name in names:
                try:
                    c=connect(name,server)
                    try:
                        row=c.cursor().execute("SELECT OBJECT_ID('dbo.TS_TOOL','U'), OBJECT_ID('dbo.TS_MOUNTING','U'), HAS_PERMS_BY_NAME('dbo.TS_TOOL','OBJECT','INSERT'), HAS_PERMS_BY_NAME('dbo.TS_MOUNTING','OBJECT','INSERT')").fetchone()
                        if row[0] and row[1] and row[2]==1 and row[3]==1: found.append((name,server))
                    finally: c.close()
                except Exception as e: errors.append(str(e))
        except Exception as e: errors.append(str(e))
    if not found: raise RuntimeError('Nessun ToolStore scrivibile trovato.\n'+'\n'.join(errors))
    return found

def writable(cur,table,data):
    rows=cur.execute('''SELECT name,is_identity,is_computed,generated_always_type,system_type_id FROM sys.columns WHERE object_id=OBJECT_ID(?)''', 'dbo.'+table).fetchall()
    if not rows: raise ValueError('Tabella mancante: '+table)
    known={r[0] for r in rows}
    unknown=set(data)-known
    if unknown: raise ValueError('Colonne non presenti nel database: '+', '.join(sorted(unknown)))
    allowed={r[0] for r in rows if not (r[1] or r[2] or r[3] or r[4]==189)}-EXCLUDE
    return {k:v for k,v in data.items() if k in allowed}

def new_tool_parameters(data):
    return {k:v for k,v in data.items() if k not in EXCLUDE and k != 'MNT_TOOL_ID'}

def insert(cur,table,data):
    data=writable(cur,table,data)
    if table == 'TS_TOOL' and 'TL_TOOL_ID' in data:
        raise RuntimeError('ID originale non consentito')
    if table == 'TS_MOUNTING' and ('MNT_MOUNTING_ID' in data or 'MNT_TOOL_ID' not in data):
        raise RuntimeError('Montaggio senza nuovo riferimento valido')
    cols=', '.join('['+k+']' for k in data)
    marks=', '.join('?' for k in data)
    cur.execute(f'SET NOCOUNT ON; INSERT INTO dbo.[{table}] ({cols}) VALUES ({marks}); SELECT CAST(SCOPE_IDENTITY() AS int) AS NUOVO_ID;', *data.values())
    while True:
        if cur.description and cur.description[0][0]=='NUOVO_ID':
            row=cur.fetchone()
            if row and row[0] is not None: return int(row[0])
            raise RuntimeError('ID non generato')
        if not cur.nextset(): raise RuntimeError('ID non trovato')

TRANSLATIONS.update({'File di backup': {'it': 'File di backup', 'en': 'Backup file', 'es': 'Archivo de copia', 'fr': 'Fichier de sauvegarde', 'de': 'Sicherungsdatei', 'pt': 'Arquivo de backup'}, 'Tutte le modifiche successive al backup saranno sostituite. Le connessioni attive verranno interrotte. Confermi?': {'it': 'Tutte le modifiche successive al backup saranno sostituite. Le connessioni attive verranno interrotte. Confermi?', 'en': 'All changes made after the backup will be overwritten. Active connections will be disconnected. Continue?', 'es': 'Se sobrescribirán todos los cambios posteriores a la copia. Se interrumpirán las conexiones activas. ¿Confirmas?', 'fr': 'Toutes les modifications postérieures à la sauvegarde seront écrasées. Les connexions actives seront interrompues. Confirmer ?', 'de': 'Alle Änderungen seit der Sicherung werden überschrieben. Aktive Verbindungen werden getrennt. Fortfahren?', 'pt': 'Todas as alterações posteriores ao backup serão sobrescritas. As conexões ativas serão interrompidas. Confirmar?'}, 'Digita il nome esatto del database:': {'it': 'Digita il nome esatto del database:', 'en': 'Type the exact database name:', 'es': 'Escribe el nombre exacto de la base de datos:', 'fr': 'Saisissez le nom exact de la base de données :', 'de': 'Geben Sie den exakten Datenbanknamen ein:', 'pt': 'Digite o nome exato do banco de dados:'}, 'Il database verrà sovrascritto.': {'it': 'Il database verrà sovrascritto.', 'en': 'The database will be overwritten.', 'es': 'Se sobrescribirá la base de datos.', 'fr': 'La base de données sera écrasée.', 'de': 'Die Datenbank wird überschrieben.', 'pt': 'O banco de dados será sobrescrito.'}, 'Nessun backup disponibile per ': {'it': 'Nessun backup disponibile per ', 'en': 'No backup available for ', 'es': 'No hay copias disponibles para ', 'fr': 'Aucune sauvegarde disponible pour ', 'de': 'Keine Sicherung verfügbar für ', 'pt': 'Nenhum backup disponível para '}})

GRAPHICS_ROOT = Path(__file__).resolve().with_name('GRAFICHE')
GRAPHICS_CATEGORIES = {
    'TURNING': CATEGORY_ORDER,
    'MILLING': ['END MILL','BULL NOSE','BALL NOSE','SLOT DRILL','CHAMFER MILL','FACE MILL','T-SLOT','LOLLIPOP','THREAD MILL','CORNER ROUNDER','DOVETAIL','BARREL','DOUBLE ANGLE'],
    'HOLE': ['DRILL','REAM','TAP','HOLE BORE','COUNTERSINK','CENTRE DRILL','SPOT DRILL'],
}
TRANSLATIONS['Graphic esterno non consentito.'] = dict(zip(['it','en','es','fr','de','pt'], ['Graphic esterno non consentito.','External graphics are not allowed.','No se permiten gráficos externos.','Les graphiques externes ne sont pas autorisés.','Externe Grafiken sind nicht erlaubt.','Gráficos externos não são permitidos.']))

GRAPHIC_EXTENSIONS = {'.stl', '.meg'}
TRANSLATIONS['Formato Graphic non consentito. Usa solo .stl o .meg.'] = dict(zip(['it','en','es','fr','de','pt'], ['Formato Graphic non consentito. Usa solo .stl o .meg.','Unsupported graphic format. Use only .stl or .meg.','Formato gráfico no permitido. Usa solo .stl o .meg.','Format graphique non autorisé. Utilisez uniquement .stl ou .meg.','Grafikformat nicht erlaubt. Nur .stl oder .meg verwenden.','Formato gráfico não permitido. Use apenas .stl ou .meg.']))
TRANSLATIONS['File grafico non valido o esterno.'] = dict(zip(['it','en','es','fr','de','pt'], ['File grafico non valido o esterno.','Invalid or external graphic file.','Archivo gráfico no válido o externo.','Fichier graphique invalide ou externe.','Ungültige oder externe Grafikdatei.','Arquivo gráfico inválido ou externo.']))

def graphic_format_allowed(path):
    return Path(path).suffix.lower() in GRAPHIC_EXTENSIONS and Path(path).resolve().suffix.lower() in GRAPHIC_EXTENSIONS

def graphic_allowed(path):
    try:
        Path(path).resolve().relative_to(GRAPHICS_ROOT.resolve())
        return Path(path).is_file() and graphic_format_allowed(path)
    except (ValueError, OSError, RuntimeError):
        return False

def create_graphics_folders():
    for family, categories in GRAPHICS_CATEGORIES.items():
        for category in categories:
            (GRAPHICS_ROOT / family / category).mkdir(parents=True, exist_ok=True)


TRANSLATIONS.update({
    'Ricerca database in corso...': dict(zip(['it','en','es','fr','de','pt'], ['Ricerca database in corso...','Searching for databases...','Buscando bases de datos...','Recherche des bases de données...','Datenbanken werden gesucht...','Buscando bancos de dados...'])),
    'Verifica connessione in corso...': dict(zip(['it','en','es','fr','de','pt'], ['Verifica connessione in corso...','Testing connection...','Probando conexión...','Vérification de la connexion...','Verbindung wird geprüft...','Verificando conexão...'])),
})

TRANSLATIONS.update({
    'Cerca codice': dict(zip(('it','en','es','fr','de','pt'), ('Cerca codice','Search code','Buscar código','Rechercher un code','Code suchen','Pesquisar código'))),
    'Codice': dict(zip(('it','en','es','fr','de','pt'), ('Codice','Code','Código','Code','Code','Código'))),
    '{n} risultati': dict(zip(('it','en','es','fr','de','pt'), ('{n} risultati','{n} results','{n} resultados','{n} résultats','{n} Ergebnisse','{n} resultados'))),
})

def tool_labels(path):
    try:
        data=json.loads(path.read_text(encoding='utf-8-sig'))
        return str(data.get('codice') or ''), str(data.get('nome') or path.stem)
    except (OSError, ValueError, AttributeError):
        return '', path.stem

class App:
    def __init__(self, root):
        global LANG
        options=load_options(); LANG=options['language']; self.translated_widgets=[]; self.log_history=[]; self.last_status=""
        self.root=root; self.folder=LIBRARY; self.family_keys=['TURNING','MILLING','HOLE']; self.family_key='TURNING'; self.category_key='ALL'; self.folders=dict(zip(self.family_keys,[LIBRARY,LIBRARY_ROOT / 'LIBRERIA_FRESATURA',LIBRARY_ROOT / 'LIBRERIA_FORATURA'])); self.model=None; self.chosen=set(); self.graphics={}; self.visible=[]; self.tool_index={}
        for family, folder in self.folders.items():
            for category in GRAPHICS_CATEGORIES[family]:
                (folder / category).mkdir(parents=True, exist_ok=True)
        create_graphics_folders()
        self.destinations={}; self.busy=False; self.events=queue.Queue(); self.controls=[]
        root.protocol("WM_DELETE_WINDOW", self.close)
        root.title('EDGECAM - '+tr('Importa utensili')+' V36'); root.geometry('950x900')
        f=ttk.Frame(root,padding=20); f.pack(fill='both',expand=True)
        self.localized(ttk.Label,f,'Importa utensili',font=('Segoe UI',20,'bold')).pack(anchor='w')
        self.localized(ttk.Label,f,'Destination Database').pack(anchor='w',pady=5)
        self.destination=tk.StringVar()
        self.db_combo=ttk.Combobox(f,textvariable=self.destination,state='readonly')
        self.db_combo.pack(fill='x')
        dbbar=ttk.Frame(f); dbbar.pack(fill='x',pady=4)
        self.localized(ttk.Button,dbbar,'Aggiorna database',command=self.scan).pack(side='left')
        self.localized(ttk.Button,dbbar,'Ripristina backup...',command=self.choose_restore).pack(side='left',padx=8)
        filters=ttk.Frame(f); filters.pack(fill='x',pady=(4,8))
        filters.columnconfigure(0,weight=1,uniform='filters')
        filters.columnconfigure(1,weight=1,uniform='filters')
        family_box=ttk.Frame(filters); family_box.grid(row=0,column=0,sticky='ew',padx=(0,8))
        category_box=ttk.Frame(filters); category_box.grid(row=0,column=1,sticky='ew',padx=(8,0))
        self.localized(ttk.Label,family_box,'Famiglia utensili').pack(anchor='w')
        self.family_combo=ttk.Combobox(family_box,state='readonly',values=[tr(k) for k in self.family_keys]); self.family_combo.pack(fill='x',pady=(3,0)); self.family_combo.current(0)
        self.family_combo.bind('<<ComboboxSelected>>',self.change_family)
        self.localized(ttk.Label,category_box,'Sottocategoria').pack(anchor='w')
        self.category=tk.StringVar()
        self.category_combo=ttk.Combobox(category_box,textvariable=self.category,state='readonly')
        self.category_combo.pack(fill='x',pady=(3,0))
        self.category_combo.bind('<<ComboboxSelected>>',self.refresh_files)
        searchbar=ttk.Frame(f); searchbar.pack(fill='x',pady=(0,6))
        self.localized(ttk.Label,searchbar,'Cerca codice').pack(side='left',padx=(0,8))
        self.search_code=tk.StringVar()
        ttk.Entry(searchbar,textvariable=self.search_code).pack(side='left',fill='x',expand=True)
        ttk.Button(searchbar,text='X',width=3,command=lambda: self.search_code.set('')).pack(side='left',padx=5)
        self.search_count=tk.StringVar(); ttk.Label(searchbar,textvariable=self.search_count).pack(side='right')
        self.localized(ttk.Label,f,'Spunta gli utensili da inserire; clicca sul nome per scegliere Graphic').pack(anchor='w')
        bar=ttk.Frame(f); bar.pack(fill='x')
        self.localized(ttk.Button,bar,'Seleziona tutto',command=self.select_visible).pack(side='left')
        self.localized(ttk.Button,bar,'Deseleziona tutto',command=self.clear_selection).pack(side='left',padx=5)
        self.count=tk.StringVar(); ttk.Label(bar,textvariable=self.count).pack(side='right')
        table=ttk.Frame(f); table.pack(fill='both',pady=5)
        style=ttk.Style(root)
        style.configure('Tools.Treeview',rowheight=30)
        self.check_images={}
        for checked in (False,True):
            img=tk.PhotoImage(master=root,width=22,height=22)
            img.put('#344054',to=(1,1,21,21))
            img.put('#ffffff',to=(3,3,19,19))
            if checked:
                img.put('#2563eb',to=(3,3,19,19))
                for x,y in [(5,10),(6,11),(7,12),(8,13),(9,12),(10,11),(11,10),(12,9),(13,8),(14,7),(15,6)]:
                    img.put('#ffffff',to=(x,y,x+2,y+2))
            self.check_images[checked]=img
        self.lb=ttk.Treeview(table,columns=('category','code','name','graphic'),show='tree headings',selectmode='browse',height=10,style='Tools.Treeview')
        self.lb.heading('#0',text='✓'); self.lb.column('#0',width=55,minwidth=55,stretch=False,anchor='center')
        for col,title,width in [('category','Categoria',155),('code','Codice',180),('name','Utensile',330),('graphic','Graphic',560)]:
            self.lb.heading(col,text=tr(title)); self.lb.column(col,width=width,stretch=col=='graphic',anchor='w')
        scroll=ttk.Scrollbar(table,orient='vertical',command=self.lb.yview)
        hscroll=ttk.Scrollbar(table,orient='horizontal',command=self.lb.xview)
        self.lb.configure(yscrollcommand=scroll.set,xscrollcommand=hscroll.set)
        hscroll.pack(side='bottom',fill='x')
        scroll.pack(side='right',fill='y'); self.lb.pack(side='left',fill='both',expand=True)
        self.lb.bind('<Button-1>',self.toggle_click)
        self.lb.bind('<space>',self.toggle_space)
        self.lb.bind('<<TreeviewSelect>>',self.show_graphic_path)
        self.graphic_path=tk.StringVar()
        ttk.Entry(f,textvariable=self.graphic_path,state='readonly').pack(fill='x',pady=(0,4))
        self.info=tk.StringVar(); ttk.Label(f,textvariable=self.info,wraplength=880).pack(anchor='w')
        g=ttk.Frame(f); g.pack(fill='x',pady=5)
        self.localized(ttk.Button,g,'Graphic per utensile...',command=self.browse).pack(side='left')
        self.localized(ttk.Button,g,'Rimuovi Graphic',command=self.remove_graphic).pack(side='left',padx=5)
        self.localized(ttk.Label,f,'Graphic opzionale: seleziona un solo utensile per assegnargli un file.').pack(anchor='w')
        options=load_options()
        self.skip=tk.BooleanVar(value=options['skip_duplicates'])
        self.auto_backup=tk.BooleanVar(value=options['auto_backup'])
        menubar=tk.Menu(root,tearoff=False); self.menubar=menubar
        self.options_menu=tk.Menu(menubar,tearoff=False)
        self.options_menu.add_checkbutton(label=tr('Salta utensili duplicati'),variable=self.skip,command=self.save_options)
        self.options_menu.add_checkbutton(label=tr('Backup automatico'),variable=self.auto_backup,command=self.save_options)
        self.language=tk.StringVar(value=LANG)
        self.language_menu=tk.Menu(self.options_menu,tearoff=False)
        for code,name in LANGUAGES.items(): self.language_menu.add_radiobutton(label=name,variable=self.language,value=code,command=self.change_language)
        self.options_menu.add_cascade(label=tr('Lingua'),menu=self.language_menu)
        self.theme=tk.StringVar(value=options['theme'])
        self.theme_menu=tk.Menu(self.options_menu,tearoff=False)
        for code,key in THEME_KEYS.items():
            self.theme_menu.add_radiobutton(label=tr(key),variable=self.theme,value=code,command=self.change_theme)
        self.options_menu.add_cascade(label=tr('Tema interfaccia'),menu=self.theme_menu)
        menubar.add_cascade(label=tr('Opzioni'),menu=self.options_menu)
        root.configure(menu=menubar)
        self.status=tk.StringVar(); ttk.Label(f,textvariable=self.status,wraplength=780).pack(anchor='w',pady=10)
        buttons=ttk.Frame(f); buttons.pack(fill='x',side='bottom')
        self.localized(ttk.Button,buttons,'Verifica connessione',command=self.test).pack(side='left')
        self.localized(ttk.Button,buttons,'Inserisci selezionati',command=self.save).pack(side='right')
        self.progress=ttk.Progressbar(f,maximum=100,mode='determinate')
        self.progress.pack(fill='x',pady=5)
        self.percent=tk.StringVar(value='0%'); ttk.Label(f,textvariable=self.percent).pack(anchor='e')
        self.log=tk.Text(f,height=8,wrap='word',state='disabled'); self.log.pack(fill='both',expand=True,pady=5)
        def collect(w):
            for child in w.winfo_children():
                if isinstance(child,(ttk.Button,ttk.Entry,ttk.Combobox,ttk.Checkbutton,tk.Listbox)):
                    self.controls.append((child,str(child.cget('state'))))
                collect(child)
        collect(f)
        self.original_theme = style.theme_use()
        style.theme_create('edgecam_black', parent='clam')
        self.original_colors = []
        for widget, keys in [(root, ('background',)), (self.log, ('background','foreground','insertbackground','selectbackground','selectforeground'))] + [(m, ('background','foreground','activebackground','activeforeground','selectcolor')) for m in (self.menubar,self.options_menu,self.language_menu,self.theme_menu)]:
            self.original_colors.append((widget, {k:widget.cget(k) for k in keys}))
        self.original_popdowns = []
        for combo in (self.db_combo,self.family_combo,self.category_combo):
            try:
                pop=combo.tk.call('ttk::combobox::PopdownWindow',str(combo))+'.f.l'
                keys=('background','foreground','selectbackground','selectforeground')
                self.original_popdowns.append((pop, {k:combo.tk.call(pop,'cget','-'+k) for k in keys}))
            except tk.TclError:
                pass
        self.apply_theme()
        self.refresh()
        self.search_code.trace_add('write',lambda *_: self.refresh_files())
        root.after(80,self.poll)
        root.after(100,self.scan)
    def localized(self, cls, parent, key, **kwargs):
        w=cls(parent,text=tr(key),**kwargs)
        self.translated_widgets.append((w,key))
        return w
    def change_language(self):
        global LANG
        if self.busy: return
        LANG=self.language.get()
        self.root.title('EDGECAM - '+tr('Importa utensili')+' V36')
        self.translated_widgets=[(w,k) for w,k in self.translated_widgets if w.winfo_exists()]
        for w,k in self.translated_widgets: w.configure(text=tr(k))
        for i,k in enumerate(('Salta utensili duplicati','Backup automatico','Lingua','Tema interfaccia')): self.options_menu.entryconfigure(i,label=tr(k))
        for i,key in enumerate(THEME_KEYS.values()): self.theme_menu.entryconfigure(i,label=tr(key))
        self.menubar.entryconfigure(1 if self.menubar.cget('tearoff') else 0,label=tr('Opzioni'))
        for col,k in [('category','Categoria'),('code','Codice'),('name','Utensile'),('graphic','Graphic')]: self.lb.heading(col,text=tr(k))
        self.family_combo.configure(values=[tr(k) for k in self.family_keys]); self.family_combo.current(self.family_keys.index(self.family_key))
        self.refresh_categories(); self.refresh_files(); self.update_count(); self.render_log(); self.status.set(translate_log(self.last_status)); self.save_options()
    def change_theme(self):
        self.apply_theme()
        self.save_options()

    def apply_theme(self):
        style=ttk.Style(self.root)
        if self.theme.get() == 'original':
            style.theme_use(self.original_theme)
            for widget, colors in self.original_colors:
                widget.configure(**colors)
            for pop, colors in self.original_popdowns:
                try:
                    for k,v in colors.items(): self.root.tk.call(pop,'configure','-'+k,v)
                except tk.TclError:
                    pass
            for checked,img in self.check_images.items():
                img.put('#344054',to=(1,1,21,21))
                img.put('#2563eb' if checked else '#ffffff',to=(3,3,19,19))
                if checked:
                    for x,y in [(5,10),(6,11),(7,12),(8,13),(9,12),(10,11),(11,10),(12,9),(13,8),(14,7),(15,6)]:
                        img.put('#ffffff',to=(x,y,x+2,y+2))
            return
        bg,fg,panel,border,accent=THEMES['black']
        style.theme_use('edgecam_black')
        style.configure('.',background=bg,foreground=fg,fieldbackground=panel,
                        bordercolor=border,lightcolor=border,darkcolor=border,
                        troughcolor=panel,arrowcolor=fg,selectbackground=accent,selectforeground='#ffffff')
        for name in ('TFrame','TLabel','TLabelframe','TLabelframe.Label'):
            style.configure(name,background=bg,foreground=fg)
        for name in ('TButton','TCombobox','TEntry','TCheckbutton'):
            style.configure(name,background=panel,foreground=fg,fieldbackground=panel)
            style.map(name,background=[('disabled',bg),('active',border)],
                      foreground=[('disabled',fg)],fieldbackground=[('readonly',panel),('disabled',bg)])
        style.configure('Tools.Treeview',rowheight=30,background=bg,fieldbackground=bg,foreground=fg)
        style.map('Tools.Treeview',background=[('selected',accent)],foreground=[('selected','#ffffff')])
        style.configure('Treeview.Heading',background=panel,foreground=fg)
        style.map('Treeview.Heading',background=[('active',border)])
        style.configure('Horizontal.TProgressbar',background=accent,troughcolor=panel)
        for name in ('Vertical.TScrollbar','Horizontal.TScrollbar'):
            style.configure(name,background=border,troughcolor=panel,arrowcolor=fg)
        self.root.configure(background=bg)
        for menu in (self.menubar,self.options_menu,self.language_menu,self.theme_menu):
            menu.configure(background=panel,foreground=fg,activebackground=accent,activeforeground='#ffffff',selectcolor=fg)
        self.log.configure(background=panel,foreground=fg,insertbackground=fg,selectbackground=accent,selectforeground='#ffffff')
        for checked,img in self.check_images.items():
            img.put(fg,to=(1,1,21,21)); img.put(accent if checked else bg,to=(3,3,19,19))
            if checked:
                for x,y in [(5,10),(6,11),(7,12),(8,13),(9,12),(10,11),(11,10),(12,9),(13,8),(14,7),(15,6)]:
                    img.put('#ffffff',to=(x,y,x+2,y+2))
        # Existing combobox popdowns may already have been created.
        for combo in (self.db_combo,self.family_combo,self.category_combo):
            try:
                pop=combo.tk.call('ttk::combobox::PopdownWindow',str(combo))
                combo.tk.call(pop+'.f.l','configure','-background',panel,'-foreground',fg,'-selectbackground',accent,'-selectforeground','#ffffff')
            except tk.TclError:
                pass

    def save_options(self):
        try:
            tmp=OPTIONS_FILE.with_suffix('.tmp')
            tmp.write_text(json.dumps({'skip_duplicates': self.skip.get(), 'auto_backup': self.auto_backup.get(), 'language': self.language.get(), 'theme': self.theme.get()}, indent=2),encoding='utf-8')
            tmp.replace(OPTIONS_FILE)
        except OSError as e:
            messagebox.showwarning(tr('Opzioni'),'Impostazioni valide per questa sessione, ma non salvate: '+str(e))
    def change_family(self,event=None):
        self.family_key=self.family_keys[self.family_combo.current()]
        self.folder=self.folders[self.family_key]; self.category_key='ALL'; self.refresh()
    def library_files(self):
        return sorted(p for p in self.folder.glob('*/*.json') if p.is_file())
    def refresh_categories(self):
        folders=sorted({p.parent.name for p in self.library_files()})
        self.category_keys=['ALL']+folders
        if self.category_key not in self.category_keys: self.category_key='ALL'
        self.category_combo.configure(values=[tr(k) for k in self.category_keys]); self.category_combo.current(self.category_keys.index(self.category_key))
    def refresh(self):
        files=set(self.library_files()); self.tool_index={p:tool_labels(p) for p in files}; self.chosen.intersection_update(files)
        self.graphics={p:g for p,g in self.graphics.items() if p in files}
        self.refresh_categories(); self.refresh_files()
    def refresh_files(self,event=None):
        if event is not None: self.category_key=self.category_keys[self.category_combo.current()]
        old=self.focused_path()
        query=self.search_code.get().strip().casefold()
        self.visible=[p for p in sorted(self.tool_index) if (self.category_key=='ALL' or p.parent.name==self.category_key) and query in self.tool_index[p][0].casefold()]
        self.search_count.set(tr('{n} risultati').format(n=len(self.visible)))
        self.lb.delete(*self.lb.get_children())
        for i,p in enumerate(self.visible):
            self.lb.insert('', 'end', iid=str(i), image=self.check_images[p in self.chosen], values=(tr(p.parent.name),*self.tool_index[p],self.graphics.get(p,'')))
            if p==old:
                self.lb.selection_set(str(i)); self.lb.focus(str(i))
        self.update_count(); self.show_graphic_path()
    def show_graphic_path(self,event=None):
        self.graphic_path.set(self.graphics.get(self.focused_path(),''))
    def focused_path(self):
        sel=self.lb.selection()
        if sel and int(sel[0])<len(self.visible): return self.visible[int(sel[0])]
        return None
    def update_count(self):
        self.count.set(tr('{n} selezionati').format(n=len(self.chosen))); self.info.set(tr('{n} grafiche assegnate nella libreria').format(n=len(self.graphics)))
    def toggle(self,iid):
        if self.busy or not iid: return
        p=self.visible[int(iid)]
        if p in self.chosen: self.chosen.remove(p)
        else: self.chosen.add(p)
        self.lb.item(iid,image=self.check_images[p in self.chosen]); self.update_count()
    def toggle_click(self,event):
        if self.busy: return 'break'
        if self.lb.identify_region(event.x,event.y) in ('tree','cell') and self.lb.identify_column(event.x)=='#0':
            iid=self.lb.identify_row(event.y)
            self.toggle(iid)
            return 'break'
    def toggle_space(self,event):
        self.toggle(self.lb.focus()); return 'break'
    def select_visible(self):
        self.chosen.update(self.visible); self.refresh_files()
    def clear_selection(self):
        self.chosen.clear(); self.refresh_files()
    def browse(self):
        target=self.focused_path()
        if target is None: messagebox.showinfo('Graphic',tr('Clicca sul nome di un utensile.')); return
        folder=GRAPHICS_ROOT / self.family_key / target.parent.name
        folder.mkdir(parents=True, exist_ok=True)
        p=filedialog.askopenfilename(parent=self.root, initialdir=str(folder), title=tr('Graphic per utensile...'), filetypes=[('STL / MEG', ('*.stl','*.meg','*.STL','*.MEG'))])
        if not p: return
        if not graphic_format_allowed(p):
            messagebox.showerror(tr('Errore'),tr('Formato Graphic non consentito. Usa solo .stl o .meg.'),parent=self.root)
            return
        if not graphic_allowed(p):
            messagebox.showerror(tr('Errore'),tr('File grafico non valido o esterno.'),parent=self.root)
            return
        self.graphics[target]=str(Path(p).resolve()); self.refresh_files()
    def remove_graphic(self):
        target=self.focused_path()
        if target is not None: self.graphics.pop(target,None)
        self.refresh_files()
    def close(self):
        if self.busy:
            messagebox.showinfo(tr('Operazione in corso'),tr('Attendi il completamento della transazione SQL.'))
        else: self.root.destroy()
    def append(self,text):
        stamp=datetime.now().strftime('%H:%M:%S')
        self.log_history.append((stamp,text))
        self.log.configure(state='normal')
        self.log.insert('end',stamp+'  '+translate_log(text)+'\n')
        self.log.see('end'); self.log.configure(state='disabled')
    def render_log(self):
        self.log.configure(state='normal'); self.log.delete('1.0','end')
        for stamp,text in self.log_history:
            self.log.insert('end',stamp+'  '+translate_log(text)+'\n')
        self.log.see('end'); self.log.configure(state='disabled')
    def start(self,target,*args):
        if self.busy: return
        self.busy=True
        for i in (0,1,2,3): self.options_menu.entryconfigure(i,state="disabled")
        for w,_ in self.controls: w.configure(state='disabled')
        self.progress['value']=0; self.percent.set('0%'); self.log_history.clear(); self.last_status=''
        self.log.configure(state='normal'); self.log.delete('1.0','end'); self.log.configure(state='disabled')
        if target in (self.scan_worker, self.test_worker):
            self.last_status = 'Ricerca database in corso...' if target == self.scan_worker else 'Verifica connessione in corso...'
            self.status.set(tr(self.last_status)); self.append(self.last_status)
            self.percent.set('')
            self.progress.configure(mode='indeterminate')
            self.progress.start(12)
        else:
            self.progress.configure(mode='determinate')
        threading.Thread(target=target,args=args,daemon=False).start()
    def poll(self):
        try:
            while True:
                kind,value,text=self.events.get_nowait()
                self.last_status=text; self.status.set(translate_log(text)); self.append(text)
                if kind != 'progress':
                    self.progress.stop()
                    self.progress.configure(mode='determinate')
                if kind=='databases':
                    self.progress['value']=100; self.percent.set('100%')
                    self.destinations={f'{n} | {s}':(n,s) for n,s in value}
                    self.db_combo['values']=list(self.destinations)
                    self.destination.set(next((k for k in self.destinations if k.startswith('TEST_PYTHON |')), ''))
                    self.busy=False
                    for i in (0,1,2,3): self.options_menu.entryconfigure(i,state="normal")
                    for w,state in self.controls: w.configure(state=state)
                elif kind=='progress':
                    self.progress['value']=value; self.percent.set(f'{value}%')
                else:
                    self.busy=False
                    for i in (0,1,2,3): self.options_menu.entryconfigure(i,state="normal")
                    for w,state in self.controls: w.configure(state=state)
                    if kind=='ok':
                        self.progress['value']=100; self.percent.set('100%')
                        messagebox.showinfo(tr('Risultato'),translate_log(text))
                    else:
                        self.progress['value']=0; self.percent.set(tr('Errore')); messagebox.showerror(tr('Operazione non riuscita'),translate_log(text))
        except queue.Empty: pass
        self.root.after(80,self.poll)
    def report(self,n,text): self.events.put(('progress',n,text))
    def scan(self):
        if self.busy: return
        self.destinations={}; self.destination.set(''); self.db_combo['values']=[]
        self.start(self.scan_worker)
    def scan_worker(self):
        try: self.events.put(('databases',discover(),'Seleziona il database di destinazione.'))
        except Exception as e: self.events.put(('error',0,str(e)))
    def selected(self):
        dest=self.destinations.get(self.destination.get())
        if not dest: messagebox.showerror('Database','Seleziona un database di destinazione.'); return None
        return dest
    def test(self):
        dest=self.selected()
        if dest: self.start(self.test_worker,*dest)
    def test_worker(self,database,server):
        c=None
        try:
            c=connect(database,server)
            self.events.put(('ok',100,'Connessione riuscita: '+server+' / '+database))
        except Exception as e: self.events.put(('error',0,str(e)))
        finally:
            if c: c.close()
    def choose_restore(self):
        if self.busy: return
        dest=self.selected()
        if not dest: return
        database,server=dest
        folder=backup_directory(database,server)
        files=sorted(list(folder.glob('AUTO_*.bak'))+list((folder/'EMERGENCY').glob('SAFETY_*.bak')),key=lambda p:p.stat().st_mtime,reverse=True)
        if not files:
            messagebox.showinfo('Backup',tr('Nessun backup disponibile per ')+database); return
        win=tk.Toplevel(self.root); win.title(tr('Ripristina backup')); win.geometry('850x400'); win.transient(self.root); win.grab_set()
        ttk.Label(win,text=f'{database} | {server}').pack(pady=8)
        self.localized(ttk.Label,win,'Seleziona una versione. Chiudi EDGECAM prima del ripristino.').pack()
        lb=tk.Listbox(win)
        if self.theme.get() == 'black':
            bg,fg,panel,border,accent=THEMES['black']
            win.configure(background=bg)
            lb.configure(background=panel,foreground=fg,selectbackground=accent,selectforeground='#ffffff')
        lb.pack(fill='both',expand=True,padx=12,pady=8)
        for p in files:
            lb.insert('end',datetime.fromtimestamp(p.stat().st_mtime).strftime('%d/%m/%Y %H:%M:%S')+' | '+tr('Emergenza' if p.parent.name=='EMERGENCY' else 'Automatico')+' | '+p.name)
        lb.selection_set(0)
        def confirm():
            sel=lb.curselection()
            if not sel: return
            path=files[sel[0]]
            text = (f"{tr('Destinazione')}: {database}\nServer: {server}\n"
                    f"{tr('File di backup')}: {path.name}\n\n"
                    + tr('Tutte le modifiche successive al backup saranno sostituite. Le connessioni attive verranno interrotte. Confermi?'))
            if not self.restore_confirmation(win, 'Conferma ripristino', text): return
            if not self.restore_confirmation(win, 'Conferma definitiva', tr('Il database verrà sovrascritto.')+'\n\n'+tr('Digita il nome esatto del database:')+' '+database, database): return
            win.destroy(); self.start(self.restore_worker,database,server,path)
        self.localized(ttk.Button,win,'Ripristina versione selezionata',command=confirm).pack(pady=8)
        self.localized(ttk.Button,win,'Annulla',command=win.destroy).pack(pady=4)
    def restore_confirmation(self, parent, title, text, expected=None):
        win = tk.Toplevel(parent)
        win.title(tr(title)); win.transient(parent); win.resizable(False, False)
        if self.theme.get() == 'black': win.configure(background=THEMES['black'][0])
        frame = ttk.Frame(win, padding=20); frame.pack(fill='both', expand=True)
        ttk.Label(frame, text=text, justify='left', wraplength=500).pack(anchor='w', pady=(0, 16))
        result = [False]
        typed = tk.StringVar(master=win)
        entry = None
        if expected is not None:
            entry = ttk.Entry(frame, textvariable=typed, width=48)
            entry.pack(fill='x', pady=(0, 16))
        buttons = ttk.Frame(frame); buttons.pack(fill='x')
        def finish(value=False):
            if value and expected is not None and typed.get() != expected: return
            result[0] = value
            win.destroy()
        cancel = ttk.Button(buttons, text=tr('Annulla'), command=finish)
        cancel.pack(side='right', padx=(8, 0))
        ok = ttk.Button(buttons, text=tr('Conferma'), command=lambda: finish(True))
        ok.pack(side='right')
        if expected is not None:
            ok.state(['disabled'])
            typed.trace_add('write', lambda *_: ok.state(['!disabled'] if typed.get()==expected else ['disabled']))
        win.protocol('WM_DELETE_WINDOW', finish)
        win.bind('<Escape>', lambda event: finish())
        win.update_idletasks()
        win.geometry(f'+{max(0,parent.winfo_rootx()+(parent.winfo_width()-win.winfo_width())//2)}+{max(0,parent.winfo_rooty()+(parent.winfo_height()-win.winfo_height())//2)}')
        win.grab_set()
        (entry if entry is not None else cancel).focus_set()
        parent.wait_window(win)
        if parent.winfo_exists(): parent.grab_set()
        return result[0]

    def restore_worker(self,database,server,path):
        c=None; safety=None; single=False; restored=False; error=None
        try:
            self.report(5,'Verifica backup selezionato...')
            c=connect('master',server,autocommit=True); c.timeout=0; cur=c.cursor()
            cur.execute('RESTORE HEADERONLY FROM DISK = ?',str(path))
            cols=[d[0] for d in cur.description]; rows=[dict(zip(cols,r)) for r in cur.fetchall()]; drain(cur)
            if len(rows)!=1 or rows[0].get('DatabaseName')!=database or rows[0].get('BackupType')!=1:
                raise RuntimeError('Backup non completo o non appartenente al database selezionato.')
            cur.execute('RESTORE VERIFYONLY FROM DISK = ? WITH CHECKSUM',str(path)); drain(cur)
            self.report(25,'Backup di emergenza dello stato attuale...')
            safety=backup_database(database,server,emergency=True)
            self.report(45,'Backup di emergenza verificato: '+str(safety))
            db=sql_identifier(database)
            self.report(55,'Chiusura connessioni attive e ripristino...')
            single=True
            cur.execute('ALTER DATABASE '+db+' SET SINGLE_USER WITH ROLLBACK IMMEDIATE'); drain(cur)
            cur.execute('RESTORE DATABASE '+db+' FROM DISK = ? WITH REPLACE, RECOVERY, CHECKSUM',str(path)); drain(cur)
            restored=True
            self.report(85,'Ripristino completato; riapertura database...')
        except Exception as e: error=str(e)
        finally:
            if c:
                try: c.close()
                except Exception: pass  # The restore may have invalidated the pipe.
            if single:
                try:
                    self.verify_reopened_database(database,server)
                except Exception as e:
                    error=(error+'\n' if error else '')+'Verifica riapertura: '+str(e)
            msg=('Ripristino riuscito.' if not error else ('Ripristino eseguito, ma verifica finale non riuscita: ' if restored else 'Ripristino non confermato: ')+error)
            if safety: msg+='\nBackup di emergenza: '+str(safety)
            self.events.put(('error' if error else 'ok',0 if error else 100,msg))
    def verify_reopened_database(self,database,server):
        last=None
        for attempt in range(1,9):
            master=None; check=None
            try:
                clock.sleep(2)
                self.report(90,f'Nuova connessione SQL: tentativo {attempt}/8...')
                master=connect('master',server,autocommit=True)
                master.timeout=15
                cur=master.cursor()
                row=cur.execute('SELECT state_desc,user_access_desc FROM sys.databases WHERE name=?',database).fetchone()
                if not row or row[0]!='ONLINE':
                    raise RuntimeError('Database non ONLINE: '+str(row))
                if row[1]!='MULTI_USER':
                    cur.execute('ALTER DATABASE '+sql_identifier(database)+' SET MULTI_USER WITH ROLLBACK IMMEDIATE'); drain(cur)
                row=cur.execute('SELECT state_desc,user_access_desc FROM sys.databases WHERE name=?',database).fetchone()
                if not row or tuple(row)!=('ONLINE','MULTI_USER'):
                    raise RuntimeError('Database non ONLINE/MULTI_USER: '+str(row))
                check=connect(database,server,autocommit=True)
                check.timeout=15
                cur=check.cursor()
                for table in ('TS_TOOL','TS_MOUNTING'):
                    cur.execute('SELECT TOP (1) * FROM dbo.'+table).fetchone()
                self.report(98,'Database ONLINE / MULTI_USER; tabelle ToolStore accessibili.')
                return
            except Exception as e:
                last=e
            finally:
                for conn in (check,master):
                    if conn is not None:
                        try: conn.close()
                        except Exception: pass
        raise RuntimeError('Riapertura non verificata dopo 8 tentativi: '+str(last))
    def confirm_insert(self, database, server, auto_backup):
        win = tk.Toplevel(self.root)
        if self.theme.get() == 'black': win.configure(background=THEMES['black'][0])
        win.title(tr('Conferma inserimento'))
        win.transient(self.root)
        win.resizable(False, False)
        result = [False]
        frame = ttk.Frame(win, padding=20)
        frame.pack(fill='both', expand=True)
        text = (f"{tr('Destinazione')}: {database}\n"
                f"Server: {server}\n"
                f"{tr('Utensili selezionati')}: {len(self.chosen)}\n\n"
                f"{tr('Backup automatico')}: {tr('Attivo' if auto_backup else 'Disattivato')}\n\n")
        if not auto_backup:
            text += tr('ATTENZIONE: backup automatico DISATTIVATO. Nessuna copia di sicurezza prima del lotto.') + "\n\n"
        text += tr('Confermi?')
        ttk.Label(frame, text=text, justify='left', wraplength=500).pack(anchor='w', pady=(0, 16))
        buttons = ttk.Frame(frame)
        buttons.pack(fill='x')
        def finish(value=False):
            result[0] = value
            win.destroy()
        cancel = ttk.Button(buttons, text=tr('Annulla'), command=finish)
        cancel.pack(side='right', padx=(8, 0))
        ttk.Button(buttons, text=tr('Conferma'), command=lambda: finish(True)).pack(side='right')
        win.protocol('WM_DELETE_WINDOW', finish)
        win.bind('<Escape>', lambda event: finish())
        win.update_idletasks()
        win.geometry(f'+{max(0, self.root.winfo_rootx()+ (self.root.winfo_width()-win.winfo_width())//2)}+{max(0, self.root.winfo_rooty()+ (self.root.winfo_height()-win.winfo_height())//2)}')
        win.grab_set()
        cancel.focus_set()
        self.root.wait_window(win)
        return result[0]
    def save(self):
        if self.busy: return
        dest=self.selected()
        if not dest: return
        if not self.chosen: messagebox.showerror(tr('Modelli'),tr('Seleziona almeno un utensile')); return
        database,server=dest
        auto_backup=self.auto_backup.get()
        if not self.confirm_insert(database, server, auto_backup): return
        self.start(self.save_worker,[(p,self.graphics.get(p,'')) for p in sorted(self.chosen)],self.skip.get(),database,server,auto_backup)
    def save_worker(self,items,skip,database,server,auto_backup):
        c=None; backup=None; committed=False; result=None
        try:
            models=[]
            for p,graphic in items:
                m=json.loads(p.read_text(encoding='utf-8-sig'),object_hook=decode)
                t=new_tool_parameters(m['tool']); mounts=[new_tool_parameters(x) for x in m['mountings']]
                if t['TL_TOOL_CATEGORY_ID'] not in (0,1,2) or not mounts: raise ValueError('Modello non valido: '+str(p))
                t.pop('TL_TOOL_GRAPHIC_FILE',None); t['TL_SHANK_VISIBILITY']=not bool(graphic)
                if graphic:
                    if not graphic_format_allowed(graphic): raise ValueError(tr('Formato Graphic non consentito. Usa solo .stl o .meg.')+' '+graphic)
                    if not graphic_allowed(graphic): raise ValueError(tr('File grafico non valido o esterno.')+' '+graphic)
                    graphic=str(Path(graphic).resolve())
                for x in mounts: x.pop('MNT_TOOL_GRAPHIC_FILE',None)
                models.append((t,mounts,graphic))
            c=connect(database,server); cur=c.cursor(); skipped=[]; todo=[]; seen=set()
            def exists(name):
                return bool(cur.execute('SELECT COUNT(*) FROM dbo.TS_TOOL WHERE TL_TOOL_DESCRIPTION=?',name).fetchone()[0])
            for t,m,g in models:
                name=t['TL_TOOL_DESCRIPTION']
                if name in seen or exists(name):
                    if not skip: raise ValueError('Duplicato: '+name)
                    skipped.append(name); continue
                seen.add(name); todo.append((t,m,g))
            c.rollback()
            if not todo:
                result=('ok',100,f'Nessun inserimento necessario. Duplicati saltati: {len(skipped)}'); return
            if auto_backup:
                self.report(10,'Backup completo prima del lotto...'); backup=backup_database(database,server)
                self.report(20,'Backup verificato: '+str(backup))
                try: rotate_backups(backup.parent)
                except OSError as e: self.report(20,'Avviso pulizia backup: '+str(e))
            else:
                self.report(20,'Backup automatico disattivato: inserimento senza nuova copia di sicurezza.')
            inserted=0
            for i,(t,mounts,graphic) in enumerate(todo,1):
                name=t['TL_TOOL_DESCRIPTION']; self.report(20+int(70*(i-1)/len(todo)),f'{i}/{len(todo)}: {name}')
                if exists(name):
                    if skip: skipped.append(name); continue
                    raise ValueError('Duplicato: '+name)
                tid=insert(cur,'TS_TOOL',t)
                for m in mounts:
                    m['MNT_TOOL_ID']=tid
                    if graphic: m['MNT_TOOL_GRAPHIC_FILE']=graphic
                    mid=insert(cur,'TS_MOUNTING',m)
                    r=cur.execute('SELECT MNT_HOLDER_OFFSET_ORIGIN,MNT_TOOL_GRAPHIC_FILE FROM dbo.TS_MOUNTING WHERE MNT_MOUNTING_ID=? AND MNT_TOOL_ID=?',mid,tid).fetchone()
                    if not r or r[0]!=m.get('MNT_HOLDER_OFFSET_ORIGIN') or r[1]!=m.get('MNT_TOOL_GRAPHIC_FILE'): raise RuntimeError('Verifica montaggio fallita: '+name)
                r=cur.execute('SELECT TL_HAND_OF_TOOL_ID,TL_TOOL_DESCRIPTION,TL_SHANK_VISIBILITY FROM dbo.TS_TOOL WHERE TL_TOOL_ID=?',tid).fetchone()
                if not r or r[0]!=t.get('TL_HAND_OF_TOOL_ID') or r[1]!=name or r[2] is None or bool(r[2])!=(not bool(graphic)): raise RuntimeError('Verifica utensile fallita: '+name)
                inserted+=1; self.report(20+int(70*i/len(todo)),f'Verificato {name}, nuovo ID {tid}')
            c.commit(); committed=True
            msg=f"Inserimento completato: {inserted} utensili; duplicati saltati: {len(skipped)}."
            if skipped: msg+='\n'+ '\n'.join(skipped)
            if backup: msg+='\nBackup: '+str(backup)
            result=('ok',100,msg)
        except Exception as e:
            msg=str(e)
            if c and not committed:
                try: c.rollback(); msg+='\nRollback dell’intero lotto eseguito.'
                except Exception as re: msg+='\nRollback non verificato: '+str(re)
            if backup: msg+='\nBackup conservato: '+str(backup)
            result=('error',0,msg)
        finally:
            if c:
                try: c.close()
                except Exception: pass
            self.events.put(result)

if __name__=='__main__':
    root=tk.Tk(); App(root); root.mainloop()
