 Gerenciador de Arquivos Inteligente (CLI)

Uma ferramenta de linha de comando (CLI) desenvolvida em Python para automatizar a organização de arquivos. O script varre um diretório de origem, identifica os tipos de arquivos e os move para pastas categorizadas (como Imagens, Documentos, Audios), gerando logs e relatórios detalhados da operação.

 Funcionalidades

- **Organização Automática:** Classifica arquivos com base em suas extensões.
- **Segurança de Dados:** Tratamento automático de conflitos de nome (não sobrescreve arquivos existentes).
- **Filtro por Data:** Opção para processar apenas arquivos modificados após uma data específica.
- **Modo Simulação (Dry-Run):** Permite visualizar o que será feito sem mover nenhum arquivo.
- **Relatórios:** Gera arquivos JSON e CSV com o resumo da execução.
- **Logs:** Registro detalhado de operações e erros (console e arquivo).

 Requisitos

- Python 3.8 ou superior.
- Biblioteca `python-dateutil`.

Como Usar

O script deve ser executado via terminal a partir do arquivo main.py.
1. Execução Básica Organiza os arquivos da pasta de origem e cria uma pasta organized dentro dela. python main.py --source "C:/Caminho/Para/Downloads"
2. Modo Simulação (Dry-Run)Verifica o que seria movido sem realizar alterações reais. Recomendado para a primeira execução. python main.py --source "./minha_pasta" --dry-run
3. Definir Destino PersonalizadoEspecifica onde os arquivos organizados serão salvos. python main.py --source "./bagunca" --output "./documentos_organizados"
4. Filtrar por DataOrganiza apenas arquivos modificados após a data especificada (Formato YYYY-MM-DD). python main.py --source "./arquivos" --date 2023-01-01
5. Ver Logs DetalhadosAtiva o modo verbose para debug. python main.py --source "./arquivos" --verbose

   
Argumento,Abreviação,Obrigatório,Descrição

--source,-s,Sim,Diretório de origem contendo os arquivos.

--output,-o,Não,Diretório de destino (Padrão: cria pasta 'organized' na origem).

--date,-d,Não,Data de corte (YYYY-MM-DD). Processa arquivos modificados após esta data.

--dry-run,N/A,Não,Ativa o modo de simulação.

--verbose,-v,Não,Ativa logs detalhados no console.

Estrutura do Projeto
main.py: Ponto de entrada.
Gerencia os argumentos e inicia o processo.
config.py: Configurações globais (extensões, diretórios ignorados).
src/scanner.py: Responsável por listar e filtrar arquivos.
src/organizer.py: Lógica de movimentação e criação de pastas.
src/reporter.py: Geração de estatísticas e relatórios (CSV/JSON).
src/utils.py: Funções auxiliares.
Licença
Este projeto é de uso livre para fins educacionais e pessoais.
