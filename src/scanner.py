#A camada de Entrada (Input).Ele não modifica nada, apenas lê.

import logging
from pathlib import Path
from datetime import datetime
from config import IGNORED_DIRS, IGNORED_FILES
from src.utils import parse_date

class FileScanner:
    def __init__(self, source_dir: Path):
        self.source_dir = source_dir
        self.logger = logging.getLogger(__name__)

    def scan(self, filter_date_str=None):
        """
        Varre o diretório e retorna uma lista de arquivos válidos.
        """
        files_found = []
        
        # Converte a data de corte (string -> datetime) se ela existir
        cutoff_date = parse_date(filter_date_str)
        if filter_date_str and not cutoff_date:
            self.logger.warning(f"Data inválida fornecida: {filter_date_str}. Ignorando filtro.")

        self.logger.info(f"Iniciando varredura em: {self.source_dir}")

        # Varredura (apenas nível atual, não entra em subpastas recursivamente por segurança inicial)
        if not self.source_dir.exists():
            self.logger.error("Diretório de origem não encontrado.")
            return []

        for item in self.source_dir.iterdir():
            # 1. Ignora diretórios (neste momento só queremos mover arquivos)
            if item.is_dir():
                if item.name in IGNORED_DIRS:
                    self.logger.debug(f"Ignorando diretório proibido: {item.name}")
                continue

            # 2. Ignora arquivos de sistema proibidos
            if item.name in IGNORED_FILES:
                continue

            # 3. Coleta Metadados
            stats = item.stat()
            mod_time = datetime.fromtimestamp(stats.st_mtime)

            # 4. Aplica Filtro de Data (se o usuário pediu)
            # Ex: Se user pediu date='2023-01-01', só pegamos arquivos DEPOIS dessa data
            if cutoff_date and mod_time < cutoff_date:
                continue

            # Adiciona à lista de processamento
            file_info = {
                "path": item,           # Objeto Path completo
                "name": item.name,      # Nome do arquivo
                "extension": item.suffix.lower(), # Extensão (.pdf)
                "size": stats.st_size,  # Tamanho em bytes
                "date": mod_time        # Datetime objeto
            }
            files_found.append(file_info)

        self.logger.info(f"Escaneamento concluído. {len(files_found)} arquivos encontrados.")
        return files_found