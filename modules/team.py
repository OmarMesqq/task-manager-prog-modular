"""
Módulo de Cadastro de Time

Este módulo é responsável por gerenciar a entidade "Time" dentro do sistema.
Cada time representa uma equipe ou grupo de usuários ao qual uma tarefa pode
ser associada.

Funções principais:
- time_criar: Cria um novo time
- time_destruir: Libera recursos de um time
- time_adicionar_usuario: Adiciona um usuário ao time
- time_remover_usuario: Remove um usuário do time
- time_qtd_membros: Retorna quantidade de membros do time

Conforme especificação: O módulo não conhece nem depende dos outros módulos.
Ele apenas expõe sua interface por meio de funções públicas.

ESTRUTURAS ENCAPSULADAS:
- _times_registrados: Dicionário com todos os times registrados em memória
- time_carregar_dados: Carrega times dos arquivos JSON
- time_salvar_dados: Salva times nos arquivos JSON
- time_registrar: Registra um time no sistema
- time_listar_todos: Lista todos os times registrados
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
import sys
import os

__all__ = [
    "time_criar",
    "time_destruir",
    "time_adicionar_usuario",
    "time_remover_usuario",
    "time_qtd_membros",
    "time_get_nome",
    "time_get_id",
    "time_get_membros",
    "time_set_nome",
    "time_from_dict",
    "time_to_dict",
    "time_carregar_dados",
    "time_salvar_dados",
    "time_registrar",
    "time_listar_todos"
]

# Adiciona o diretório raiz ao path se não estiver lá
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from config import SUCESSO, ERRO, MAX_NOME_LENGTH, TIMES_FILE
from utils import gerar_id_unico, validar_string_nao_vazia, log_operacao, formatar_data, carregar_json, salvar_json

# Estrutura encapsulada para armazenar todos os times registrados
_times_registrados: Dict[int, Dict[str, Any]] = {}

def _criar_time_dict(nome: str) -> Dict[str, Any]:
    """
    Cria um dicionário representando um time.
    
    Args:
        nome (str): Nome do time
        
    Returns:
        Dict: Dicionário representando o time
    """
    return {
        'id': gerar_id_unico(),
        'nome': nome,
        'membros': [],  # Lista de IDs dos usuários (para evitar dependência circular)
        'data_criacao': datetime.now(),
        'data_modificacao': datetime.now()
    }

def time_to_dict(time: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converte o time para dicionário (para persistência).
    
    Args:
        time (Dict): Time em formato dicionário
        
    Returns:
        Dict: Representação do time em dicionário para persistência
    """
    return {
        'id': time['id'],
        'nome': time['nome'],
        'membros': time['membros'].copy(),
        'data_criacao': formatar_data(time['data_criacao']),
        'data_modificacao': formatar_data(time['data_modificacao'])
    }

def time_from_dict(dados: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Cria um time a partir de um dicionário.
    
    Args:
        dados (Dict): Dados do time
        
    Returns:
        Dict ou None: Time em formato dicionário ou None em caso de erro
    """
    from utils import parse_data
    
    try:
        time = {
            'id': dados['id'],
            'nome': dados['nome'],
            'membros': dados.get('membros', []),
            'data_criacao': parse_data(dados['data_criacao']),
            'data_modificacao': parse_data(dados['data_modificacao'])
        }
        return time
    except Exception as e:
        print(f"Erro ao criar time a partir de dict: {e}")
        return None

# Funções de gerenciamento das estruturas encapsuladas

def time_carregar_dados() -> None:
    """
    Carrega todos os times dos arquivos JSON para a estrutura encapsulada.
    Esta função é chamada apenas uma vez durante a inicialização.
    """
    try:
        dados_times = carregar_json(TIMES_FILE)
        if dados_times:
            for time_data in dados_times.values():
                time = time_from_dict(time_data)
                if time:
                    _times_registrados[time['id']] = time
        
        log_operacao("Time", "Dados carregados", f"Total de times: {len(_times_registrados)}")
                    
    except Exception as e:
        log_operacao("Time", "Erro ao carregar dados", str(e))

def time_salvar_dados() -> bool:
    """
    Salva todos os times da estrutura encapsulada nos arquivos JSON.
    Esta função é chamada apenas uma vez durante a finalização.
    
    Returns:
        bool: True se salvou com sucesso, False caso contrário
    """
    try:
        dados_times = {str(tid): time_to_dict(time) for tid, time in _times_registrados.items()}
        if salvar_json(dados_times, TIMES_FILE):
            log_operacao("Time", "Dados salvos", f"Total de times: {len(_times_registrados)}")
            return True
        else:
            log_operacao("Time", "Erro ao salvar dados", "Falha na persistência")
            return False
        
    except Exception as e:
        log_operacao("Time", "Erro ao salvar dados", str(e))
        return False

def time_registrar(time: Dict[str, Any]) -> int:
    """
    Registra um time na estrutura encapsulada.
    
    Args:
        time (Dict): Time em formato dicionário a ser registrado
        
    Returns:
        int: 0 para sucesso, -1 para erro
    """
    if time is None:
        log_operacao("Time", "Erro ao registrar", "Ponteiro Time nulo")
        return ERRO
    
    try:
        time_id = time_get_id(time)
        if time_id is None:
            log_operacao("Time", "Erro ao registrar", "ID do time inválido")
            return ERRO
        
        # Verifica se o time já está registrado
        if time_id in _times_registrados:
            log_operacao("Time", "Erro ao registrar", f"Time {time_id} já registrado")
            return ERRO
        
        # Registra o time
        _times_registrados[time_id] = time
        log_operacao("Time", "Time registrado", f"ID: {time_id}")
        return SUCESSO
        
    except Exception as e:
        log_operacao("Time", "Erro ao registrar", f"Falha: {str(e)}")
        return ERRO

def time_listar_todos() -> List[Dict[str, Any]]:
    """
    Lista todos os times registrados na estrutura encapsulada.
    
    Returns:
        List[Dict]: Lista de todos os times em formato dicionário
    """
    return list(_times_registrados.values())

# Funções da interface pública (conforme especificação)

def time_criar(nome: str) -> Optional[Dict[str, Any]]:
    """
    Cria um novo time com o nome fornecido.
    
    Conforme especificação:
    Entrada: ponteiro para string com o nome do time
    Saída: ponteiro para struct Time recém-criada, ou NULL em caso de erro
    genérico (ex.: falha de alocação de memória)
    
    Args:
        nome (str): Nome do time (não pode ser nulo nem vazio)
        
    Returns:
        Dict ou None: Time em formato dicionário ou None em caso de erro
    """
    # Validação do nome
    if not validar_string_nao_vazia(nome, "nome"):
        log_operacao("Time", "Erro ao criar", "Nome inválido")
        return None
    
    if len(nome) > MAX_NOME_LENGTH:
        log_operacao("Time", "Erro ao criar", f"Nome muito longo (max {MAX_NOME_LENGTH})")
        return None
    
    try:
        # Cria o time
        time = _criar_time_dict(nome.strip())
        log_operacao("Time", "Criado com sucesso", f"ID: {time['id']}, Nome: {nome}")
        return time
        
    except Exception as e:
        log_operacao("Time", "Erro ao criar", f"Falha na alocação: {str(e)}")
        return None

def time_destruir(time: Dict[str, Any]) -> None:
    """
    Libera os recursos alocados pelo time.
    
    Conforme especificação:
    Entrada: ponteiro para uma struct Time
    Saída: nenhuma (libera os recursos alocados pelo time)
    
    Args:
        time (Dict): Time em formato dicionário a ser destruído
    """
    if time is None:
        log_operacao("Time", "Erro ao destruir", "Ponteiro nulo")
        return
    
    log_operacao("Time", "Destruído", f"ID: {time['id']}")
    # Em Python, o garbage collector cuida da liberação de memória
    time.clear()

def time_adicionar_usuario(time: Dict[str, Any], usuario) -> int:
    """
    Adiciona um usuário ao time.
    
    Conforme especificação:
    Entrada: ponteiro para struct Time e ponteiro para o usuário a ser adicionado
    Saída: 0 se adicionado com sucesso, -1 em caso de erro (ex: usuário duplicado
    ou ponteiros NULL)
    
    Args:
        time (Dict): Time em formato dicionário
        usuario: Instância do usuário (pode ser objeto Usuario ou ID)
        
    Returns:
        int: 0 para sucesso, -1 para erro
    """
    if time is None:
        log_operacao("Time", "Erro ao adicionar usuário", "Ponteiro de time nulo")
        return ERRO
    
    if usuario is None:
        log_operacao("Time", "Erro ao adicionar usuário", "Ponteiro de usuário nulo")
        return ERRO
    
    try:
        # Obtém o ID do usuário (pode ser objeto Usuario ou ID direto)
        if isinstance(usuario, dict) and 'id' in usuario:
            usuario_id = usuario['id']
        elif hasattr(usuario, 'id'):
            usuario_id = usuario.id
        else:
            usuario_id = usuario
        
        # Verifica se o usuário já está no time
        if usuario_id in time['membros']:
            log_operacao("Time", "Erro ao adicionar usuário", f"Usuário {usuario_id} já está no time")
            return ERRO
        
        # Adiciona o usuário ao time
        time['membros'].append(usuario_id)
        time['data_modificacao'] = datetime.now()
        
        log_operacao("Time", "Usuário adicionado", f"Time ID: {time['id']}, Usuário ID: {usuario_id}")
        return SUCESSO
        
    except Exception as e:
        log_operacao("Time", "Erro ao adicionar usuário", f"Falha: {str(e)}")
        return ERRO

def time_remover_usuario(time: Dict[str, Any], usuario) -> int:
    """
    Remove um usuário do time.
    
    Conforme especificação:
    Entrada: ponteiro para struct Time e ponteiro para o usuário a ser removido
    Saída: 0 se removido com sucesso, -1 em caso de erro (ex: usuário não encontrado
    ou ponteiros NULL)
    
    Args:
        time (Dict): Time em formato dicionário
        usuario: Instância do usuário (pode ser objeto Usuario ou ID)
        
    Returns:
        int: 0 para sucesso, -1 para erro
    """
    if time is None:
        log_operacao("Time", "Erro ao remover usuário", "Ponteiro de time nulo")
        return ERRO
    
    if usuario is None:
        log_operacao("Time", "Erro ao remover usuário", "Ponteiro de usuário nulo")
        return ERRO
    
    try:
        # Obtém o ID do usuário (pode ser objeto Usuario ou ID direto)
        if isinstance(usuario, dict) and 'id' in usuario:
            usuario_id = usuario['id']
        elif hasattr(usuario, 'id'):
            usuario_id = usuario.id
        else:
            usuario_id = usuario
        
        # Verifica se o usuário está no time
        if usuario_id not in time['membros']:
            log_operacao("Time", "Erro ao remover usuário", f"Usuário {usuario_id} não está no time")
            return ERRO
        
        # Remove o usuário do time
        time['membros'].remove(usuario_id)
        time['data_modificacao'] = datetime.now()
        
        log_operacao("Time", "Usuário removido", f"Time ID: {time['id']}, Usuário ID: {usuario_id}")
        return SUCESSO
        
    except Exception as e:
        log_operacao("Time", "Erro ao remover usuário", f"Falha: {str(e)}")
        return ERRO

def time_qtd_membros(time: Dict[str, Any]) -> int:
    """
    Retorna a quantidade de membros do time.
    
    Conforme especificação:
    Entrada: ponteiro para struct Time
    Saída: inteiro com a quantidade de membros
    
    Args:
        time (Dict): Time em formato dicionário
        
    Returns:
        int: Quantidade de membros do time
    """
    if time is None:
        log_operacao("Time", "Erro ao obter quantidade de membros", "Ponteiro de time nulo")
        return 0
    
    try:
        return len(time['membros'])
    except Exception as e:
        log_operacao("Time", "Erro ao obter quantidade de membros", f"Falha: {str(e)}")
        return 0

def time_get_nome(time: Dict[str, Any]) -> Optional[str]:
    """
    Obtém o nome do time.
    
    Conforme especificação:
    Entrada: ponteiro para a struct Time
    Saída: string com o nome do time
    
    Args:
        time (Dict): Time em formato dicionário
        
    Returns:
        str ou None: Nome do time ou None em caso de erro
    """
    if time is None:
        log_operacao("Time", "Erro ao obter nome", "Ponteiro de time nulo")
        return None
    
    try:
        return time['nome']
    except Exception as e:
        log_operacao("Time", "Erro ao obter nome", f"Falha: {str(e)}")
        return None

def time_get_id(time: Dict[str, Any]) -> Optional[int]:
    """
    Obtém o ID do time.
    
    Args:
        time (Dict): Time em formato dicionário
        
    Returns:
        int ou None: ID do time ou None em caso de erro
    """
    if time is None:
        return None
    
    try:
        return time['id']
    except Exception as e:
        log_operacao("Time", "Erro ao obter ID", f"Falha: {str(e)}")
        return None

def time_get_membros(time: Dict[str, Any]) -> List[int]:
    """
    Obtém a lista de membros do time.
    
    Args:
        time (Dict): Time em formato dicionário
        
    Returns:
        List[int]: Lista de IDs dos membros do time
    """
    if time is None:
        return []
    
    try:
        return time['membros'].copy()
    except Exception as e:
        log_operacao("Time", "Erro ao obter membros", f"Falha: {str(e)}")
        return []

def time_set_nome(time: Dict[str, Any], novo_nome: str) -> int:
    """
    Altera o nome do time.
    
    Args:
        time (Dict): Time em formato dicionário
        novo_nome (str): Novo nome do time
        
    Returns:
        int: 0 para sucesso, -1 para erro
    """
    if time is None:
        log_operacao("Time", "Erro ao alterar nome", "Ponteiro de time nulo")
        return ERRO
    
    if not validar_string_nao_vazia(novo_nome, "novo_nome"):
        log_operacao("Time", "Erro ao alterar nome", "Nome inválido")
        return ERRO
    
    if len(novo_nome) > MAX_NOME_LENGTH:
        log_operacao("Time", "Erro ao alterar nome", f"Nome muito longo (max {MAX_NOME_LENGTH})")
        return ERRO
    
    try:
        nome_antigo = time['nome']
        time['nome'] = novo_nome.strip()
        time['data_modificacao'] = datetime.now()
        
        log_operacao("Time", "Nome alterado", f"ID: {time['id']}, '{nome_antigo}' -> '{novo_nome}'")
        return SUCESSO
        
    except Exception as e:
        log_operacao("Time", "Erro ao alterar nome", f"Falha: {str(e)}")
        return ERRO

