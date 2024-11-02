import csv
import os
import unicodedata


############
# COSTANTI #
############
VOCALI = {'A', 'E', 'I', 'O', 'U'}
CONSONANTI = {'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z'}


######################
# FUNZIONI UTILITIES #
######################
def _crea_dict_denominazione_codice_catastale_da_csv(filename: str) -> dict[str, str]:
    """Crea un dizionario dai dati di un file CSV con denominazioni e codici catastali.

    Args:
        filename (str): Il nome del file CSV nella directory 'data'.

    Returns:
        dict[str, str]: Dizionario con denominazioni italiane come chiavi e codici catastali come valori.

    Raises:
        FileNotFoundError: Se il file CSV non è trovato nel percorso specificato.
        KeyError: Se le colonne 'Denominazione Italiana' o 'Codice Catastale' mancano nel CSV.
    """
    # Calcola il percorso completo del file, partendo dalla directory in cui si trova utils.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'data', filename)

    dizionario_codici_catastali = {}
    with open(file_path, mode='r', encoding='latin1') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            denominazione = row.get("Denominazione Italiana").upper()
            codice_catastale = row.get("Codice Catastale")
            if denominazione and codice_catastale:  # Salta le righe incomplete
                dizionario_codici_catastali[denominazione] = codice_catastale
    return dizionario_codici_catastali


def _formatta_stringa(stringa: str) -> str:
    """Formatta una stringa rimuovendo spazi e accenti, e convertendo i caratteri in maiuscolo.

    Args:
        stringa (str): La stringa da formattare.

    Returns:
        str: La stringa formattata senza accenti e spazi, in maiuscolo.
    """
    return _rimuovi_accenti(stringa.replace(" ", "")).upper()


def _rimuovi_accenti(stringa: str) -> str:
    """Rimuove gli accenti da una stringa usando la decomposizione Unicode.

    Args:
        stringa (str): La stringa da cui rimuovere gli accenti.

    Returns:
        str: La stringa senza accenti.
    """
    stringa_normalizzata = unicodedata.normalize('NFD', stringa)
    return ''.join(c for c in stringa_normalizzata if unicodedata.category(c) != 'Mn')


def _estrai_caratteri(stringa: str, is_nome: bool = False) -> str:
    """Estrae le consonanti e, se necessario, le vocali per la codifica del codice fiscale.

    Estrae le consonanti e, se non sufficienti, le vocali da una stringa per formare la codifica.
    Se l'opzione `is_nome` è impostata su `True`, utilizza una regola speciale per il nome.

    Args:
        stringa (str): La stringa da cui estrarre i caratteri.
        is_nome (bool, optional): Se True, applica la regola specifica per il nome. Default a False.

    Returns:
        str: Codifica di 3 caratteri, con eventuale aggiunta di 'X' se i caratteri sono meno di 3.
    """
    consonanti = ''.join(char for char in stringa if char in CONSONANTI)
    vocali = ''.join(char for char in stringa if char in VOCALI)
    if is_nome and len(consonanti) >= 4:
        return consonanti[0] + consonanti[2] + consonanti[3]
    codifica = consonanti[:3] if len(consonanti) >= 3 else consonanti + vocali[:3 - len(consonanti)]
    return codifica.ljust(3, 'X')