import argparse
import sys
import logging
from pathlib import Path
#python main.py --source ./teste_arquivos
# Imports dos nossos módulos (agora eles existem!)
from src.scanner import FileScanner
from src.organizer import FileOrganizer
from src.reporter import Reporter
from config import LOG_FILE, DATE_FORMAT_LOG

def setup_logging(verbose):
    """
    Configura o log para aparecer no Terminal E salvar em arquivo.
    """
    level = logging.DEBUG if verbose else logging.INFO
    
    # Handlers: Um para o arquivo, um para a tela (stdout)
    handlers = [
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt=DATE_FORMAT_LOG,
        handlers=handlers
    )

def main():
    # 1. Definição dos Argumentos CLI
    parser = argparse.ArgumentParser(
        description="Gerenciador de Arquivos Inteligente CLI",
        epilog="Exemplo: python main.py --source ./downloads --dry-run"
    )

    parser.add_argument('--source', '-s', required=True, type=Path, help="Pasta de origem.")
    parser.add_argument('--output', '-o', type=Path, help="Pasta de destino (Opcional).")
    parser.add_argument('--date', '-d', type=str, help="Filtrar arquivos modificados APÓS esta data (YYYY-MM-DD).")
    parser.add_argument('--dry-run', action='store_true', help="Simulação (não move arquivos).")
    parser.add_argument('--verbose', '-v', action='store_true', help="Logs detalhados.")
    
    args = parser.parse_args()

    # 2. Configuração Inicial
    setup_logging(args.verbose)
    logger = logging.getLogger("Main") # Nome do logger principal

    # Validação
    if not args.source.exists() or not args.source.is_dir():
        logger.critical(f"A origem não existe ou não é uma pasta: {args.source}")
        sys.exit(1)

    # Se não informar output, cria pasta 'organized' dentro da origem
    if not args.output:
        args.output = args.source / "organized"

    logger.info("=== Iniciando Processo de Organização ===")
    logger.info(f"Origem: {args.source}")
    logger.info(f"Destino: {args.output}")
    if args.dry_run:
        logger.warning("MODO DRY-RUN ATIVADO: Nenhuma alteração real será feita.")

    try:
        # 3. ETAPA 1: ESCANEAR (Input)
        scanner = FileScanner(args.source)
        files_found = scanner.scan(filter_date_str=args.date)

        if not files_found:
            logger.warning("Nenhum arquivo encontrado com os critérios fornecidos.")
            sys.exit(0)

        # 4. ETAPA 2: ORGANIZAR (Processamento)
        organizer = FileOrganizer(output_dir=args.output, dry_run=args.dry_run)
        results = organizer.organize(files_found)

        # 5. ETAPA 3: RELATÓRIO (Output)
        reporter = Reporter(results)
        reporter.print_summary()
        
        # Gera relatórios físicos na pasta de destino (se não for dry-run ou se quiser salvar em outro lugar)
        # Nota: Em dry-run, o output pode não existir, então salvamos na raiz ou log, 
        # mas aqui vamos tentar salvar no output mesmo assim (cria só a pasta se precisar).
        if not args.dry_run:
            reporter.export_json(args.output / "report.json")
            reporter.export_csv(args.output / "report.csv")
        else:
            logger.info("Relatórios JSON/CSV ignorados no modo Dry-Run.")

        logger.info("=== Processo Finalizado com Sucesso ===")

    except KeyboardInterrupt:
        logger.warning("\nOperação interrompida pelo usuário.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Erro fatal não tratado: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()