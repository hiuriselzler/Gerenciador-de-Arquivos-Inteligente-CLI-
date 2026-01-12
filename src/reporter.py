import json
import csv
import logging
from pathlib import Path
from collections import Counter
from src.utils import format_size

class Reporter:
    def __init__(self, results: list):
        self.results = results  # Lista retornada pelo Organizer
        self.logger = logging.getLogger(__name__)

    def _calculate_summary(self):
        """Gera estatísticas básicas dos resultados."""
        total_files = len(self.results)
        total_size = sum(r['size_bytes'] for r in self.results)
        
        # Conta quantos arquivos por categoria (ex: {'IMAGENS': 10, 'PDF': 5})
        by_category = Counter(r['category'] for r in self.results)
        
        return {
            "total_files": total_files,
            "total_size_bytes": total_size,
            "total_size_human": format_size(total_size),
            "by_category": dict(by_category)
        }

    def print_summary(self):
        """Imprime um resumo rápido no terminal."""
        if not self.results:
            self.logger.info("Nenhum arquivo foi processado.")
            return

        summary = self._calculate_summary()
        
        print("\n" + "="*40)
        print("RESUMO DA OPERAÇÃO")
        print("="*40)
        print(f"Arquivos Processados: {summary['total_files']}")
        print(f"Tamanho Total: {summary['total_size_human']}")
        print("-" * 20)
        print("Por Categoria:")
        for cat, count in summary['by_category'].items():
            print(f"  {cat}: {count} arquivos")
        print("="*40 + "\n")

    def export_json(self, output_file: Path):
        """Salva o relatório completo em JSON."""
        data = {
            "summary": self._calculate_summary(),
            "details": self.results
        }
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            self.logger.info(f"Relatório JSON salvo em: {output_file}")
        except Exception as e:
            self.logger.error(f"Erro ao salvar JSON: {e}")

    def export_csv(self, output_file: Path):
        """Salva o relatório detalhado em CSV (Excel)."""
        if not self.results:
            return

        try:
            keys = self.results[0].keys() # Pega cabeçalho do primeiro item
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.results)
            self.logger.info(f"Relatório CSV salvo em: {output_file}")
        except Exception as e:
            self.logger.error(f"Erro ao salvar CSV: {e}")