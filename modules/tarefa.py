"""
Módulo de Cadastro de Tarefa

Este módulo é responsável por gerenciar a entidade "Tarefa" dentro do sistema.
Cada tarefa representa uma atividade ou trabalho a ser realizado.

Funções principais:
- tarefa_criar: Cria uma nova tarefa
- tarefa_destruir: Libera recursos de uma tarefa
- tarefa_set_status: Altera o status de uma tarefa
- tarefa_add_tag: Adiciona uma tag a uma tarefa
- tarefa_get_titulo: Obtém o título de uma tarefa

Conforme especificação: O módulo não conhece nem depende dos outros módulos.
Ele apenas expõe sua interface por meio de funções públicas.

ESTRUTURAS ENCAPSULADAS:
- _tarefas_registradas: Dicionário com todas as tarefas registradas em memória
- tarefa_carregar_dados: Carrega tarefas dos arquivos JSON
- tarefa_salvar_dados: Salva tarefas nos arquivos JSON
- tarefa_registrar: Registra uma tarefa no sistema
- tarefa_listar_todas: Lista todas as tarefas registradas
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import sys
import os

#Encapsulamento

__all__ = [
    "StatusTarefa",
    "tarefa_criar",
    "tarefa_destruir",
    "tarefa_set_status",
    "tarefa_add_tag",
    "tarefa_list_tags",
    "tarefa_get_titulo",
    "tarefa_get_descricao",
    "tarefa_get_status",
    "tarefa_get_usuario_responsavel_id",
    "tarefa_get_prazo",
    "tarefa_get_id",
    "tarefa_get_tags_ids",
    "tarefa_remover_tag",
    "tarefa_from_dict",
    "tarefa_to_dict",
    "tarefa_carregar_dados",
    "tarefa_salvar_dados",
    "tarefa_registrar",
    "tarefa_listar_todas",
    "tarefa_set_titulo",
    "tarefa_set_descricao",
    "tarefa_set_prazo"
]

# Adiciona o diretório raiz ao path se não estiver lá
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from config import SUCESSO, ERRO, MAX_TITULO_LENGTH, MAX_DESCRICAO_LENGTH, TAREFAS_FILE
from utils import gerar_id_unico, validar_string_nao_vazia, log_operacao, formatar_data, carregar_json, salvar_json

# Estrutura encapsulada para armazenar todas as tarefas registradas
_tarefas_registradas: Dict[int, Dict[str, Any]] = {}

class StatusTarefa(Enum):
    """Enumeração dos possíveis status de uma tarefa"""
    TAREFA_ABERTA = "aberta"
    TAREFA_EM_PROGRESSO = "em_progresso"
    TAREFA_CONCLUIDA = "concluida"
    TAREFA_CANCELADA = "cancelada"

def _criar_tarefa_dict(titulo: str, descricao: str, usuario_responsavel, prazo: datetime) -> Dict[str, Any]:
    """
    Cria um dicionário representando uma tarefa.
    
    Args:
        titulo (str): Título da tarefa
        descricao (str): Descrição da tarefa
        usuario_responsavel: Usuário responsável pela tarefa
        prazo (datetime): Prazo da tarefa
        
    Returns:
        Dict: Dicionário representando a tarefa
    """
    return {
        'id': gerar_id_unico(),
        'titulo': titulo,
        'descricao': descricao,
        'usuario_responsavel_id': usuario_responsavel['id'] if isinstance(usuario_responsavel, dict) else usuario_responsavel,
        'prazo': prazo,
        'status': StatusTarefa.TAREFA_ABERTA,
        'tags': [],
        'data_criacao': datetime.now(),
        'data_modificacao': datetime.now()
    }

def tarefa_to_dict(tarefa: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converte a tarefa para dicionário (para persistência).
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário
        
    Returns:
        Dict: Representação da tarefa em dicionário para persistência
    """
    return {
        'id': tarefa['id'],
        'titulo': tarefa['titulo'],
        'descricao': tarefa['descricao'],
        'usuario_responsavel_id': tarefa['usuario_responsavel_id'],
        'prazo': formatar_data(tarefa['prazo']),
        'status': tarefa['status'].value if isinstance(tarefa['status'], StatusTarefa) else tarefa['status'],
        'tags': tarefa['tags'].copy(),
        'data_criacao': formatar_data(tarefa['data_criacao']),
        'data_modificacao': formatar_data(tarefa['data_modificacao'])
    }

def tarefa_from_dict(dados: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Cria uma tarefa a partir de um dicionário.
    
    Args:
        dados (Dict): Dados da tarefa
        
    Returns:
        Dict ou None: Tarefa em formato dicionário ou None em caso de erro
    """
    from utils import parse_data
    
    try:
        # Converte prazo se for string
        prazo = dados['prazo']
        if isinstance(prazo, str):
            prazo = parse_data(prazo)
        
        tarefa = {
            'id': dados['id'],
            'titulo': dados['titulo'],
            'descricao': dados['descricao'],
            'usuario_responsavel_id': dados['usuario_responsavel_id'],
            'prazo': prazo,
            'status': StatusTarefa(dados['status']) if isinstance(dados['status'], str) else dados['status'],
            'tags': dados.get('tags', []),
            'data_criacao': parse_data(dados['data_criacao']) if isinstance(dados['data_criacao'], str) else dados['data_criacao'],
            'data_modificacao': parse_data(dados['data_modificacao']) if isinstance(dados['data_modificacao'], str) else dados['data_modificacao']
        }
        
        return tarefa
        
    except Exception as e:
        print(f"Erro ao criar tarefa a partir de dict: {e}")
        print(f"Dados: {dados}")
        return None

# Funções de gerenciamento das estruturas encapsuladas

def tarefa_carregar_dados() -> None:
    """
    Carrega todas as tarefas dos arquivos JSON para a estrutura encapsulada.
    Esta função é chamada apenas uma vez durante a inicialização.
    """
    try:
        dados_tarefas = carregar_json(TAREFAS_FILE)
        if dados_tarefas:
            for tarefa_data in dados_tarefas.values():
                tarefa = tarefa_from_dict(tarefa_data)
                if tarefa:
                    _tarefas_registradas[tarefa['id']] = tarefa
        
        log_operacao("Tarefa", "Dados carregados", f"Total de tarefas: {len(_tarefas_registradas)}")
                    
    except Exception as e:
        log_operacao("Tarefa", "Erro ao carregar dados", str(e))

def tarefa_salvar_dados() -> bool:
    """
    Salva todas as tarefas da estrutura encapsulada nos arquivos JSON.
    Esta função é chamada apenas uma vez durante a finalização.
    
    Returns:
        bool: True se salvou com sucesso, False caso contrário
    """
    try:
        dados_tarefas = {str(tid): tarefa_to_dict(tarefa) for tid, tarefa in _tarefas_registradas.items()}
        if salvar_json(dados_tarefas, TAREFAS_FILE):
            log_operacao("Tarefa", "Dados salvos", f"Total de tarefas: {len(_tarefas_registradas)}")
            return True
        else:
            log_operacao("Tarefa", "Erro ao salvar dados", "Falha na persistência")
            return False
        
    except Exception as e:
        log_operacao("Tarefa", "Erro ao salvar dados", str(e))
        return False

def tarefa_registrar(tarefa: Dict[str, Any]) -> int:
    """
    Registra uma tarefa na estrutura encapsulada.
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário a ser registrada
        
    Returns:
        int: 0 para sucesso, -1 para erro
    """
    if tarefa is None:
        log_operacao("Tarefa", "Erro ao registrar", "Ponteiro Tarefa nulo")
        return ERRO
    
    try:
        tarefa_id = tarefa_get_id(tarefa)
        if tarefa_id is None:
            log_operacao("Tarefa", "Erro ao registrar", "ID da tarefa inválido")
            return ERRO
        
        # Verifica se a tarefa já está registrada
        if tarefa_id in _tarefas_registradas:
            log_operacao("Tarefa", "Erro ao registrar", f"Tarefa {tarefa_id} já registrada")
            return ERRO
        
        # Registra a tarefa
        _tarefas_registradas[tarefa_id] = tarefa
        log_operacao("Tarefa", "Tarefa registrada", f"ID: {tarefa_id}")
        return SUCESSO
        
    except Exception as e:
        log_operacao("Tarefa", "Erro ao registrar", f"Falha: {str(e)}")
        return ERRO

def tarefa_listar_todas() -> List[Dict[str, Any]]:
    """
    Lista todas as tarefas registradas na estrutura encapsulada.
    
    Returns:
        List[Dict]: Lista de todas as tarefas em formato dicionário
    """
    return list(_tarefas_registradas.values())

# Funções da interface pública (conforme especificação)

def tarefa_criar(titulo: str, descricao: str, usuario_responsavel, prazo: datetime) -> Optional[Dict[str, Any]]:
    """
    Cria uma nova tarefa com os dados fornecidos.
    
    Conforme especificação:
    Entrada: Strings de título e descrição da tarefa, ponteiro para struct Usuario
    responsável e prazo desta (time_t)
    Saída: ponteiro para Tarefa criada ou NULL em caso de erro genérico (falha de
    alocação de memória ou tarefa duplicada)
    
    Args:
        titulo (str): Título da tarefa (não pode ser nulo nem vazio)
        descricao (str): Descrição da tarefa (não pode ser nulo nem vazio)
        usuario_responsavel: Usuário responsável pela tarefa
        prazo (datetime): Prazo da tarefa
        
    Returns:
        Dict ou None: Tarefa em formato dicionário ou None em caso de erro
    """
    # Validação do título
    if not validar_string_nao_vazia(titulo, "titulo"):
        log_operacao("Tarefa", "Erro ao criar", "Título inválido")
        return None
    
    if len(titulo) > MAX_TITULO_LENGTH:
        log_operacao("Tarefa", "Erro ao criar", f"Título muito longo (max {MAX_TITULO_LENGTH})")
        return None
    
    # Validação da descrição
    if not validar_string_nao_vazia(descricao, "descricao"):
        log_operacao("Tarefa", "Erro ao criar", "Descrição inválida")
        return None
    
    if len(descricao) > MAX_DESCRICAO_LENGTH:
        log_operacao("Tarefa", "Erro ao criar", f"Descrição muito longa (max {MAX_DESCRICAO_LENGTH})")
        return None
    
    # Validação do usuário responsável
    if usuario_responsavel is None:
        log_operacao("Tarefa", "Erro ao criar", "Usuário responsável nulo")
        return None
    
    # Validação do prazo
    if prazo is None:
        log_operacao("Tarefa", "Erro ao criar", "Prazo inválido")
        return None
    
    if not isinstance(prazo, datetime):
        log_operacao("Tarefa", "Erro ao criar", "Prazo deve ser um objeto datetime")
        return None
    
    try:
        # Cria a tarefa
        tarefa = _criar_tarefa_dict(titulo.strip(), descricao.strip(), usuario_responsavel, prazo)
        log_operacao("Tarefa", "Criada com sucesso", f"ID: {tarefa['id']}, Título: {titulo}")
        return tarefa
        
    except Exception as e:
        log_operacao("Tarefa", "Erro ao criar", f"Falha na alocação: {str(e)}")
        return None

def tarefa_destruir(tarefa: Dict[str, Any]) -> None:
    """
    Libera os recursos alocados pela tarefa.
    
    Conforme especificação:
    Entrada: ponteiro para a struct Tarefa
    Saída: nenhuma (libera os recursos alocados)
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário a ser destruída
    """
    if tarefa is None:
        log_operacao("Tarefa", "Erro ao destruir", "Ponteiro nulo")
        return
    
    log_operacao("Tarefa", "Destruída", f"ID: {tarefa['id']}")
    # Em Python, o garbage collector cuida da liberação de memória
    tarefa.clear()

def tarefa_set_status(tarefa: Dict[str, Any], status: StatusTarefa) -> int:
    """
    Altera o status da tarefa.
    
    Conforme especificação:
    Entrada: ponteiro para a struct Tarefa e novo status
    Saída: 0 em caso de sucesso, -1 em caso de erro
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário
        status (StatusTarefa): Novo status da tarefa
        
    Returns:
        int: 0 para sucesso, -1 para erro
    """
    if tarefa is None:
        log_operacao("Tarefa", "Erro ao alterar status", "Ponteiro de tarefa nulo")
        return ERRO
    
    if status is None:
        log_operacao("Tarefa", "Erro ao alterar status", "Status nulo")
        return ERRO
    
    if not isinstance(status, StatusTarefa):
        log_operacao("Tarefa", "Erro ao alterar status", "Status inválido")
        return ERRO
    
    try:
        status_antigo = tarefa['status']
        tarefa['status'] = status
        tarefa['data_modificacao'] = datetime.now()
        
        log_operacao("Tarefa", "Status alterado", f"ID: {tarefa['id']}, '{status_antigo.value}' -> '{status.value}'")
        return SUCESSO
        
    except Exception as e:
        log_operacao("Tarefa", "Erro ao alterar status", f"Falha: {str(e)}")
        return ERRO

def tarefa_get_status(tarefa: Dict[str, Any]) -> Optional[StatusTarefa]:
    """
    Obtém o status da tarefa.
    
    Conforme especificação:
    Entrada: ponteiro para a struct Tarefa
    Saída: status da tarefa
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário
        
    Returns:
        StatusTarefa ou None: Status da tarefa ou None em caso de erro
    """
    if tarefa is None:
        log_operacao("Tarefa", "Erro ao obter status", "Ponteiro de tarefa nulo")
        return None
    
    try:
        return tarefa['status']
    except Exception as e:
        log_operacao("Tarefa", "Erro ao obter status", f"Falha: {str(e)}")
        return None

def tarefa_add_tag(tarefa: Dict[str, Any], tag) -> int:
    """
    Adiciona uma tag à tarefa.
    
    Conforme especificação:
    Entrada: ponteiro para a struct Tarefa e ponteiro para struct Tag
    Saída: 0 em caso de sucesso, -1 em caso de erro
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário
        tag: Tag a ser adicionada (pode ser objeto Tag ou ID)
        
    Returns:
        int: 0 para sucesso, -1 para erro
    """
    if tarefa is None:
        log_operacao("Tarefa", "Erro ao adicionar tag", "Ponteiro de tarefa nulo")
        return ERRO
    
    if tag is None:
        log_operacao("Tarefa", "Erro ao adicionar tag", "Ponteiro de tag nulo")
        return ERRO
    
    try:
        # Obtém o ID da tag (pode ser objeto Tag ou ID direto)
        if isinstance(tag, dict) and 'id' in tag:
            tag_id = tag['id']
        elif hasattr(tag, 'id'):
            tag_id = tag.id
        else:
            tag_id = tag
        
        # Verifica se a tag já está na tarefa
        if tag_id in tarefa['tags']:
            log_operacao("Tarefa", "Erro ao adicionar tag", f"Tag {tag_id} já está na tarefa")
            return ERRO
        
        # Adiciona a tag à tarefa
        tarefa['tags'].append(tag_id)
        tarefa['data_modificacao'] = datetime.now()
        
        log_operacao("Tarefa", "Tag adicionada", f"Tarefa ID: {tarefa['id']}, Tag ID: {tag_id}")
        return SUCESSO
        
    except Exception as e:
        log_operacao("Tarefa", "Erro ao adicionar tag", f"Falha: {str(e)}")
        return ERRO

def tarefa_list_tags(tarefa: Dict[str, Any], buffer: List, tamanho_max: int) -> int:
    """
    Lista as tags da tarefa.
    
    Conforme especificação:
    Entrada: ponteiro para a struct Tarefa, buffer para receber as tags e tamanho máximo
    Saída: quantidade de tags copiadas para o buffer
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário
        buffer (List): Buffer para receber as tags
        tamanho_max (int): Tamanho máximo do buffer
        
    Returns:
        int: Quantidade de tags copiadas para o buffer
    """
    if tarefa is None:
        log_operacao("Tarefa", "Erro ao listar tags", "Ponteiro de tarefa nulo")
        return 0
    
    if buffer is None:
        log_operacao("Tarefa", "Erro ao listar tags", "Buffer nulo")
        return 0
    
    try:
        # Limpa o buffer
        buffer.clear()
        
        # Copia as tags para o buffer (limitado pelo tamanho máximo)
        qtd_copiadas = min(len(tarefa['tags']), tamanho_max)
        buffer.extend(tarefa['tags'][:qtd_copiadas])
        
        log_operacao("Tarefa", "Tags listadas", f"Tarefa ID: {tarefa['id']}, Qtd: {qtd_copiadas}")
        return qtd_copiadas
        
    except Exception as e:
        log_operacao("Tarefa", "Erro ao listar tags", f"Falha: {str(e)}")
        return 0

def tarefa_get_titulo(tarefa: Dict[str, Any]) -> Optional[str]:
    """
    Obtém o título da tarefa.
    
    Conforme especificação:
    Entrada: ponteiro para a struct Tarefa
    Saída: string com o título da tarefa
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário
        
    Returns:
        str ou None: Título da tarefa ou None em caso de erro
    """
    if tarefa is None:
        log_operacao("Tarefa", "Erro ao obter título", "Ponteiro de tarefa nulo")
        return None
    
    try:
        return tarefa['titulo']
    except Exception as e:
        log_operacao("Tarefa", "Erro ao obter título", f"Falha: {str(e)}")
        return None

def tarefa_get_descricao(tarefa: Dict[str, Any]) -> Optional[str]:
    """
    Obtém a descrição da tarefa.
    
    Conforme especificação:
    Entrada: ponteiro para a struct Tarefa
    Saída: string com a descrição da tarefa
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário
        
    Returns:
        str ou None: Descrição da tarefa ou None em caso de erro
    """
    if tarefa is None:
        log_operacao("Tarefa", "Erro ao obter descrição", "Ponteiro de tarefa nulo")
        return None
    
    try:
        return tarefa['descricao']
    except Exception as e:
        log_operacao("Tarefa", "Erro ao obter descrição", f"Falha: {str(e)}")
        return None

def tarefa_get_usuario_responsavel_id(tarefa: Dict[str, Any]) -> Optional[int]:
    """
    Obtém o ID do usuário responsável pela tarefa.
    
    Conforme especificação:
    Entrada: ponteiro para a struct Tarefa
    Saída: ID do usuário responsável
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário
        
    Returns:
        int ou None: ID do usuário responsável ou None em caso de erro
    """
    if tarefa is None:
        log_operacao("Tarefa", "Erro ao obter usuário responsável", "Ponteiro de tarefa nulo")
        return None
    
    try:
        return tarefa['usuario_responsavel_id']
    except Exception as e:
        log_operacao("Tarefa", "Erro ao obter usuário responsável", f"Falha: {str(e)}")
        return None

def tarefa_get_prazo(tarefa: Dict[str, Any]) -> Optional[datetime]:
    """
    Obtém o prazo da tarefa.
    
    Conforme especificação:
    Entrada: ponteiro para a struct Tarefa
    Saída: prazo da tarefa (time_t)
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário
        
    Returns:
        datetime ou None: Prazo da tarefa ou None em caso de erro
    """
    if tarefa is None:
        log_operacao("Tarefa", "Erro ao obter prazo", "Ponteiro de tarefa nulo")
        return None
    
    try:
        return tarefa['prazo']
    except Exception as e:
        log_operacao("Tarefa", "Erro ao obter prazo", f"Falha: {str(e)}")
        return None

def tarefa_get_id(tarefa: Dict[str, Any]) -> Optional[int]:
    """
    Obtém o ID da tarefa.
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário
        
    Returns:
        int ou None: ID da tarefa ou None em caso de erro
    """
    if tarefa is None:
        return None
    
    try:
        return tarefa['id']
    except Exception as e:
        log_operacao("Tarefa", "Erro ao obter ID", f"Falha: {str(e)}")
        return None

def tarefa_get_tags_ids(tarefa: Dict[str, Any]) -> List[int]:
    """
    Obtém a lista de IDs das tags da tarefa.
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário
        
    Returns:
        List[int]: Lista de IDs das tags da tarefa
    """
    if tarefa is None:
        return []
    
    try:
        return tarefa['tags'].copy()
    except Exception as e:
        log_operacao("Tarefa", "Erro ao obter tags", f"Falha: {str(e)}")
        return []

def tarefa_remover_tag(tarefa: Dict[str, Any], tag) -> int:
    """
    Remove uma tag da tarefa.
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário
        tag: Tag a ser removida (pode ser objeto Tag ou ID)
        
    Returns:
        int: 0 para sucesso, -1 para erro
    """
    if tarefa is None:
        log_operacao("Tarefa", "Erro ao remover tag", "Ponteiro de tarefa nulo")
        return ERRO
    
    if tag is None:
        log_operacao("Tarefa", "Erro ao remover tag", "Ponteiro de tag nulo")
        return ERRO
    
    try:
        # Obtém o ID da tag (pode ser objeto Tag ou ID direto)
        if isinstance(tag, dict) and 'id' in tag:
            tag_id = tag['id']
        elif hasattr(tag, 'id'):
            tag_id = tag.id
        else:
            tag_id = tag
        
        # Verifica se a tag está na tarefa
        if tag_id not in tarefa['tags']:
            log_operacao("Tarefa", "Erro ao remover tag", f"Tag {tag_id} não está na tarefa")
            return ERRO
        
        # Remove a tag da tarefa
        tarefa['tags'].remove(tag_id)
        tarefa['data_modificacao'] = datetime.now()
        
        log_operacao("Tarefa", "Tag removida", f"Tarefa ID: {tarefa['id']}, Tag ID: {tag_id}")
        return SUCESSO
        
    except Exception as e:
        log_operacao("Tarefa", "Erro ao remover tag", f"Falha: {str(e)}")
        return ERRO

def tarefa_set_titulo(tarefa: Dict[str, Any], novo_titulo: str) -> int:
    """
    Altera o título da tarefa.
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário
        novo_titulo (str): Novo título da tarefa
        
    Returns:
        int: 0 para sucesso, -1 para erro
    """
    if tarefa is None:
        log_operacao("Tarefa", "Erro ao alterar título", "Ponteiro de tarefa nulo")
        return ERRO
    
    if not validar_string_nao_vazia(novo_titulo, "novo_titulo"):
        log_operacao("Tarefa", "Erro ao alterar título", "Título inválido")
        return ERRO
    
    if len(novo_titulo) > MAX_TITULO_LENGTH:
        log_operacao("Tarefa", "Erro ao alterar título", f"Título muito longo (max {MAX_TITULO_LENGTH})")
        return ERRO
    
    try:
        titulo_antigo = tarefa['titulo']
        tarefa['titulo'] = novo_titulo.strip()
        tarefa['data_modificacao'] = datetime.now()
        
        log_operacao("Tarefa", "Título alterado", f"ID: {tarefa['id']}, '{titulo_antigo}' -> '{novo_titulo}'")
        return SUCESSO
        
    except Exception as e:
        log_operacao("Tarefa", "Erro ao alterar título", f"Falha: {str(e)}")
        return ERRO

def tarefa_set_descricao(tarefa: Dict[str, Any], nova_descricao: str) -> int:
    """
    Altera a descrição da tarefa.
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário
        nova_descricao (str): Nova descrição da tarefa
        
    Returns:
        int: 0 para sucesso, -1 para erro
    """
    if tarefa is None:
        log_operacao("Tarefa", "Erro ao alterar descrição", "Ponteiro de tarefa nulo")
        return ERRO
    
    if not validar_string_nao_vazia(nova_descricao, "nova_descricao"):
        log_operacao("Tarefa", "Erro ao alterar descrição", "Descrição inválida")
        return ERRO
    
    if len(nova_descricao) > MAX_DESCRICAO_LENGTH:
        log_operacao("Tarefa", "Erro ao alterar descrição", f"Descrição muito longa (max {MAX_DESCRICAO_LENGTH})")
        return ERRO
    
    try:
        descricao_antiga = tarefa['descricao']
        tarefa['descricao'] = nova_descricao.strip()
        tarefa['data_modificacao'] = datetime.now()
        
        log_operacao("Tarefa", "Descrição alterada", f"ID: {tarefa['id']}, '{descricao_antiga}' -> '{nova_descricao}'")
        return SUCESSO
        
    except Exception as e:
        log_operacao("Tarefa", "Erro ao alterar descrição", f"Falha: {str(e)}")
        return ERRO

def tarefa_set_prazo(tarefa: Dict[str, Any], novo_prazo: datetime) -> int:
    """
    Altera o prazo da tarefa.
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário
        novo_prazo (datetime): Novo prazo da tarefa
        
    Returns:
        int: 0 para sucesso, -1 para erro
    """
    if tarefa is None:
        log_operacao("Tarefa", "Erro ao alterar prazo", "Ponteiro de tarefa nulo")
        return ERRO
    
    if novo_prazo is None:
        log_operacao("Tarefa", "Erro ao alterar prazo", "Prazo nulo")
        return ERRO
    
    if not isinstance(novo_prazo, datetime):
        log_operacao("Tarefa", "Erro ao alterar prazo", "Prazo deve ser um objeto datetime")
        return ERRO
    
    try:
        prazo_antigo = tarefa['prazo']
        tarefa['prazo'] = novo_prazo
        tarefa['data_modificacao'] = datetime.now()
        
        log_operacao("Tarefa", "Prazo alterado", f"ID: {tarefa['id']}, '{prazo_antigo}' -> '{novo_prazo}'")
        return SUCESSO
        
    except Exception as e:
        log_operacao("Tarefa", "Erro ao alterar prazo", f"Falha: {str(e)}")
        return ERRO

