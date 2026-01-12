#Se você quer mudar onde os arquivos são salvos


from pathlib import Path

# --- Diretórios e Logs ---
BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "app.log"

# Cria o diretório de logs se não existir (garantia de execução)
LOG_DIR.mkdir(exist_ok=True)

# --- Mapeamento de Arquivos ---
# Usamos SETS ({}) em vez de LISTAS ([]) porque a busca em sets é O(1) (instantânea)
FILE_MAP = {
    'IMAGENS':      {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.tiff'},
    'DOCUMENTOS':   {'.pdf', '.docx', '.doc', '.txt', '.xlsx', '.csv', '.pptx', '.md'},
    'AUDIOS':       {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'},
    'VIDEOS':       {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv'},
    'COMPACTADOS':  {'.zip', '.rar', '.7z', '.tar', '.gz', '.iso'},
    'EXECUTAVEIS':  {'.exe', '.msi', '.bat', '.sh', '.bin', '.app'},
    'CODIGOS':      {'.py', '.js', '.html', '.css', '.java', '.cpp', '.json', '.sql'}
}

# Pasta padrão para arquivos que não se encaixam nas regras acima
DEFAULT_FOLDER = 'OUTROS'

# --- Formatos ---
DATE_FORMAT_LOG = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT_FOLDER = '%Y-%m-%d'  # Formato para pastas de data (ex: 2023-10-25)

# --- Exceções de Sistema ---
# Arquivos ou pastas que o scanner deve ignorar para evitar quebrar o sistema ou loops
IGNORED_DIRS = {'.git', '.vscode', '__pycache__', 'logs', 'organized', 'node_modules'}
IGNORED_FILES = {'.DS_Store', 'Thumbs.db', 'desktop.ini'}