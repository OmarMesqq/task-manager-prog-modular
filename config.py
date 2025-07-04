"""
Configurações e constantes do Task Manager

Este módulo contém todas as configurações e constantes utilizadas
pelo sistema de gerenciamento de tarefas.
"""

from datetime import datetime
import os

# Detecta o caminho correto baseado no local de execução
def get_project_root():
    """Retorna o caminho raiz do projeto"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Se estamos executando a partir da aplicação web
    if 'web/task_manager_web/src' in current_dir:
        # Sobe 3 níveis para chegar na raiz do projeto
        return os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    
    # Se estamos na raiz do projeto
    return current_dir

PROJECT_ROOT = get_project_root()

# Configurações de arquivo
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
BACKUP_DIR = os.path.join(PROJECT_ROOT, "backup")
EXPORT_DIR = os.path.join(PROJECT_ROOT, "exports")

# Configurações de persistência
USUARIOS_FILE = "usuarios.json"
TAGS_FILE = "tags.json"
TIMES_FILE = "times.json"
TAREFAS_FILE = "tarefas.json"

# Configurações da aplicação web
WEB_HOST = "0.0.0.0"
WEB_PORT = 5000
WEB_DEBUG = True

# Códigos de retorno (conforme especificação)
SUCESSO = 0
ERRO = -1

# Limites do sistema
MAX_NOME_LENGTH = 100
MAX_EMAIL_LENGTH = 200
MAX_TITULO_LENGTH = 200
MAX_DESCRICAO_LENGTH = 1000
MAX_COR_LENGTH = 7  # #RRGGBB

# Formatos de data
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT_SHORT = "%Y-%m-%d"

# Validações
def validar_email(email):
    """Valida formato básico de email"""
    if not email or "@" not in email or "." not in email:
        return False
    return True

def validar_cor_hex(cor):
    """Valida formato de cor hexadecimal (#RRGGBB)"""
    if not cor or len(cor) != 7 or not cor.startswith("#"):
        return False
    try:
        int(cor[1:], 16)
        return True
    except ValueError:
        return False

def criar_diretorios():
    """Cria os diretórios necessários para o sistema"""
    for dir_name in [DATA_DIR, BACKUP_DIR, EXPORT_DIR]:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

# Mensagens de erro padrão
ERRO_PONTEIRO_NULO = "Ponteiro nulo fornecido"
ERRO_DADOS_INVALIDOS = "Dados inválidos fornecidos"
ERRO_ENTIDADE_NAO_ENCONTRADA = "Entidade não encontrada"
ERRO_ENTIDADE_DUPLICADA = "Entidade já existe"
ERRO_FALHA_ALOCACAO = "Falha na alocação de memória"

