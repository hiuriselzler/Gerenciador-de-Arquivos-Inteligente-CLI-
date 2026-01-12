#Funções genéricas

import math
from datetime import datetime
from dateutil import parser

def format_size(size_bytes: int) -> str:
    """
    Converte um tamanho em bytes para uma string legível (KB, MB, GB).
    Ex: 1024 -> '1.00 KB'
    """
    if size_bytes == 0:
        return "0 B"
    
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_name[i]}"


#math.log = "A que potência devo elevar 1024 para chegar ao tamanho do arquivo?"

def parse_date(date_string: str) -> datetime:
    """
    Tenta converter uma string (ex: '2023-01-01') para um objeto datetime.
    Retorna None se falhar, para que o chamador decida o que fazer.
    """
    if not date_string:
        return None
    
    try:
        # O dateutil é inteligente: entende '2023-01-01', '01/01/2023', etc.
        return parser.parse(date_string)
    except (ValueError, TypeError):
        return None