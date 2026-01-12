#Se o script de movimentação der erro,É o código que efetivamente executa a promessa do software (mover, calcular, salvar).

import shutil
import logging
from pathlib import Path
from config import FILE_MAP, DEFAULT_FOLDER

class FileOrganizer:
    def __init__(self, output_dir: Path, dry_run: bool = False):
        self.output_dir = output_dir
        self.dry_run = dry_run
        self.logger = logging.getLogger(__name__)

    def _get_destination_folder(self, extension: str) -> str:
        """
        Busca a extensão no FILE_MAP do config.py e retorna a categoria.
        """
        for category, extensions in FILE_MAP.items():
            if extension in extensions:
                return category
        return DEFAULT_FOLDER

    def _handle_collision(self, destination: Path) -> Path:
        """
        Se o arquivo já existe, adiciona um contador ao nome.
        Ex: arquivo.txt -> arquivo_1.txt -> arquivo_2.txt
        """
        if not destination.exists():
            return destination

        counter = 1
        stem = destination.stem # Nome sem extensão
        suffix = destination.suffix # Apenas extensão
        
        while destination.exists():
            new_name = f"{stem}_{counter}{suffix}"
            destination = destination.parent / new_name
            counter += 1
            
        return destination

    def organize(self, file_list: list) -> list:
        """
        Recebe a lista do scanner e move os arquivos.
        Retorna uma lista de resultados para o relatório.
        """
        results = []
        
        # Cria o diretório base de saída se não for Dry Run
        if not self.dry_run:
            self.output_dir.mkdir(parents=True, exist_ok=True)

        for file_info in file_list:
            original_path = file_info['path']
            file_name = file_info['name']
            extension = file_info['extension']

            # 1. Define Categoria e Pasta
            category = self._get_destination_folder(extension)
            target_folder = self.output_dir / category
            
            # 2. Define Caminho Final
            target_path = target_folder / file_name
            
            # 3. Resolve Colisões (apenas calculamos o novo nome)
            final_path = self._handle_collision(target_path)
            
            status = "skipped"
            
            try:
                if self.dry_run:
                    self.logger.info(f"[SIMULAÇÃO] Mover: {file_name} -> {category}/")
                    status = "dry_run"
                else:
                    # Cria subpasta (ex: output/IMAGENS)
                    target_folder.mkdir(exist_ok=True)
                    
                    # Move fisicamente
                    shutil.move(str(original_path), str(final_path))
                    self.logger.info(f"Movido: {file_name} -> {category}/{final_path.name}")
                    status = "success"

            except Exception as e:
                self.logger.error(f"Erro ao mover {file_name}: {e}")
                status = "error"

            # Registra o resultado para o relatório
            results.append({
                "file": file_name,
                "original_path": str(original_path),
                "destination": str(final_path),
                "category": category,
                "size_bytes": file_info['size'],
                "status": status
            })

        return results