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
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import sys
import os

# Adiciona o diretório raiz ao path se não estiver lá
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from config import SUCESSO, ERRO, MAX_TITULO_LENGTH, MAX_DESCRICAO_LENGTH
from utils import gerar_id_unico, validar_string_nao_vazia, log_operacao, formatar_data

class StatusTarefa(Enum):
    """Enumeração dos possíveis status de uma tarefa"""
    TAREFA_ABERTA = "aberta"
    TAREFA_EM_PROGRESSO = "em_progresso"
    TAREFA_CONCLUIDA = "concluida"
    TAREFA_CANCELADA = "cancelada"

def criar_tarefa_dict(titulo: str, descricao: str, usuario_responsavel, prazo: datetime) -> Dict[str, Any]:
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
        tarefa = criar_tarefa_dict(titulo.strip(), descricao.strip(), usuario_responsavel, prazo)
        log_operacao("Tarefa", "Criada com sucesso", f"ID: {tarefa['id']}, Título: {titulo}")
        return tarefa
        
    except Exception as e:
        log_operacao("Tarefa", "Erro ao criar", f"Falha na alocação: {str(e)}")
        return None

def tarefa_destruir(tarefa: Dict[str, Any]) -> None:
    """
    Libera os recursos alocados pela tarefa.
    
    Conforme especificação:
    Entrada: Ponteiro para a struct Tarefa
    Saída: nenhuma (libera a memória alocada)
    
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
    Entrada: Ponteiro para a struct Tarefa, enum de status da tarefa (StatusTarefa)
    Saída: inteiro indicando sucesso (0) ou erro (por exemplo, tarefa inexistente)
    
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
        log_operacao("Tarefa", "Status alterado", f"ID: {tarefa['id']}, De: {status_antigo.value if hasattr(status_antigo, 'value') else status_antigo} Para: {status.value}")
        return SUCESSO
        
    except Exception as e:
        log_operacao("Tarefa", "Erro ao alterar status", f"Falha: {str(e)}")
        return ERRO

def tarefa_get_status(tarefa: Dict[str, Any]) -> Optional[StatusTarefa]:
    """
    Obtém o status atual da tarefa.
    
    Conforme especificação:
    Entrada: Ponteiro para a struct Tarefa
    Saída: enum StatusTarefa com o status atual
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário
        
    Returns:
        StatusTarefa ou None: Status atual da tarefa ou None em caso de erro
    """
    if tarefa is None:
        log_operacao("Tarefa", "Erro ao obter status", "Ponteiro de tarefa nulo")
        return None
    
    try:
        return tarefa['status']
    except KeyError:
        log_operacao("Tarefa", "Erro ao obter status", "Campo status não encontrado")
        return None

def tarefa_add_tag(tarefa: Dict[str, Any], tag) -> int:
    """
    Adiciona uma tag à tarefa.
    
    Conforme especificação:
    Entrada: Ponteiro para a struct Tarefa, ponteiro para a struct Tag
    Saída: 0 se adicionada com sucesso, -1 em caso de erro (ex: tag duplicada)
    
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
        
        # Adiciona a tag
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
    Entrada: Ponteiro para a struct Tarefa, buffer para armazenar as tags,
    tamanho máximo do buffer
    Saída: número de tags listadas
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário
        buffer (List): Lista para armazenar as tags
        tamanho_max (int): Tamanho máximo do buffer
        
    Returns:
        int: Número de tags listadas
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
        
        # Copia as tags para o buffer (limitando ao tamanho máximo)
        tags_para_copiar = tarefa['tags'][:tamanho_max]
        buffer.extend(tags_para_copiar)
        
        log_operacao("Tarefa", "Tags listadas", f"Tarefa ID: {tarefa['id']}, Tags: {len(buffer)}")
        return len(buffer)
        
    except Exception as e:
        log_operacao("Tarefa", "Erro ao listar tags", f"Falha: {str(e)}")
        return 0

def tarefa_get_titulo(tarefa: Dict[str, Any]) -> Optional[str]:
    """
    Obtém o título da tarefa.
    
    Conforme especificação:
    Entrada: Ponteiro para a struct Tarefa
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
    except KeyError:
        log_operacao("Tarefa", "Erro ao obter título", "Campo título não encontrado")
        return None

def tarefa_get_descricao(tarefa: Dict[str, Any]) -> Optional[str]:
    """
    Obtém a descrição da tarefa.
    
    Conforme especificação:
    Entrada: Ponteiro para a struct Tarefa
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
    except KeyError:
        log_operacao("Tarefa", "Erro ao obter descrição", "Campo descrição não encontrado")
        return None

def tarefa_get_usuario_responsavel_id(tarefa: Dict[str, Any]) -> Optional[int]:
    """
    Obtém o ID do usuário responsável pela tarefa.
    
    Conforme especificação:
    Entrada: Ponteiro para a struct Tarefa
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
    except KeyError:
        log_operacao("Tarefa", "Erro ao obter usuário responsável", "Campo usuário responsável não encontrado")
        return None

def tarefa_get_prazo(tarefa: Dict[str, Any]) -> Optional[datetime]:
    """
    Obtém o prazo da tarefa.
    
    Conforme especificação:
    Entrada: Ponteiro para a struct Tarefa
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
    except KeyError:
        log_operacao("Tarefa", "Erro ao obter prazo", "Campo prazo não encontrado")
        return None

def tarefa_get_id(tarefa: Dict[str, Any]) -> Optional[int]:
    """
    Obtém o ID da tarefa.
    
    Conforme especificação:
    Entrada: Ponteiro para a struct Tarefa
    Saída: ID da tarefa
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário
        
    Returns:
        int ou None: ID da tarefa ou None em caso de erro
    """
    if tarefa is None:
        log_operacao("Tarefa", "Erro ao obter ID", "Ponteiro de tarefa nulo")
        return None
    
    try:
        return tarefa['id']
    except KeyError:
        log_operacao("Tarefa", "Erro ao obter ID", "Campo ID não encontrado")
        return None

def tarefa_get_tags_ids(tarefa: Dict[str, Any]) -> List[int]:
    """
    Obtém a lista de IDs das tags da tarefa.
    
    Args:
        tarefa (Dict): Tarefa em formato dicionário
        
    Returns:
        List[int]: Lista de IDs das tags
    """
    if tarefa is None:
        return []
    
    try:
        return tarefa['tags'].copy()
    except KeyError:
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
        
        # Remove a tag
        tarefa['tags'].remove(tag_id)
        tarefa['data_modificacao'] = datetime.now()
        log_operacao("Tarefa", "Tag removida", f"Tarefa ID: {tarefa['id']}, Tag ID: {tag_id}")
        return SUCESSO
        
    except Exception as e:
        log_operacao("Tarefa", "Erro ao remover tag", f"Falha: {str(e)}")
        return ERRO

