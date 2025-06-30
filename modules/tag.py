"""
Módulo de Cadastro de Tag

Este módulo é responsável por gerenciar a entidade "Tag" dentro do sistema.
Cada tag representa uma etiqueta ou categoria que pode ser associada a tarefas.

Funções principais:
- tag_criar: Cria uma nova tag
- tag_destruir: Libera recursos de uma tag
- tag_set_nome: Altera o nome de uma tag
- tag_set_cor: Altera a cor de uma tag
- tag_get_nome: Obtém o nome de uma tag

Conforme especificação: O módulo não conhece nem depende dos outros módulos.
Ele apenas expõe sua interface por meio de funções públicas.

ESTRUTURAS ENCAPSULADAS:
- _tags_registradas: Dicionário com todas as tags registradas em memória
- tag_carregar_dados: Carrega tags dos arquivos JSON
- tag_salvar_dados: Salva tags nos arquivos JSON
- tag_registrar: Registra uma tag no sistema
- tag_listar_todas: Lista todas as tags registradas
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
import sys
import os

#Encapsulamento
__all__ = [
    "tag_criar",
    "tag_destruir",
    "tag_set_nome",
    "tag_set_cor",
    "tag_get_nome",
    "tag_get_cor",
    "tag_get_id",
    "tag_from_dict",
    "tag_to_dict",
    "tag_carregar_dados",
    "tag_salvar_dados",
    "tag_registrar",
    "tag_listar_todas"
]

# Adiciona o diretório raiz ao path se não estiver lá
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from config import SUCESSO, ERRO, validar_cor_hex, MAX_NOME_LENGTH, MAX_COR_LENGTH, TAGS_FILE
from utils import gerar_id_unico, validar_string_nao_vazia, log_operacao, formatar_data, carregar_json, salvar_json

# Estrutura encapsulada para armazenar todas as tags registradas
_tags_registradas: Dict[int, Dict[str, Any]] = {}

def _criar_tag_dict(nome: str, cor: str) -> Dict[str, Any]:
    """
    Cria um dicionário representando uma tag.
    
    Args:
        nome (str): Nome da tag
        cor (str): Cor da tag em formato hexadecimal (#RRGGBB)
        
    Returns:
        Dict: Dicionário representando a tag
    """
    return {
        'id': gerar_id_unico(),
        'nome': nome,
        'cor': cor,
        'data_criacao': datetime.now(),
        'data_modificacao': datetime.now()
    }

def tag_to_dict(tag: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converte a tag para dicionário (para persistência).
    
    Args:
        tag (Dict): Tag em formato dicionário
        
    Returns:
        Dict: Representação da tag em dicionário para persistência
    """
    return {
        'id': tag['id'],
        'nome': tag['nome'],
        'cor': tag['cor'],
        'data_criacao': formatar_data(tag['data_criacao']),
        'data_modificacao': formatar_data(tag['data_modificacao'])
    }

def tag_from_dict(dados: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Cria uma tag a partir de um dicionário.
    
    Args:
        dados (Dict): Dados da tag
        
    Returns:
        Dict ou None: Tag em formato dicionário ou None em caso de erro
    """
    from utils import parse_data
    
    try:
        tag = {
            'id': dados['id'],
            'nome': dados['nome'],
            'cor': dados['cor'],
            'data_criacao': parse_data(dados['data_criacao']),
            'data_modificacao': parse_data(dados['data_modificacao'])
        }
        return tag
    except Exception as e:
        print(f"Erro ao criar tag a partir de dict: {e}")
        return None

# Funções de gerenciamento das estruturas encapsuladas

def tag_carregar_dados() -> None:
    """
    Carrega todas as tags dos arquivos JSON para a estrutura encapsulada.
    Esta função é chamada apenas uma vez durante a inicialização.
    """
    try:
        dados_tags = carregar_json(TAGS_FILE)
        if dados_tags:
            for tag_data in dados_tags.values():
                tag = tag_from_dict(tag_data)
                if tag:
                    _tags_registradas[tag['id']] = tag
        
        log_operacao("Tag", "Dados carregados", f"Total de tags: {len(_tags_registradas)}")
                    
    except Exception as e:
        log_operacao("Tag", "Erro ao carregar dados", str(e))

def tag_salvar_dados() -> bool:
    """
    Salva todas as tags da estrutura encapsulada nos arquivos JSON.
    Esta função é chamada apenas uma vez durante a finalização.
    
    Returns:
        bool: True se salvou com sucesso, False caso contrário
    """
    try:
        dados_tags = {str(tid): tag_to_dict(tag) for tid, tag in _tags_registradas.items()}
        if salvar_json(dados_tags, TAGS_FILE):
            log_operacao("Tag", "Dados salvos", f"Total de tags: {len(_tags_registradas)}")
            return True
        else:
            log_operacao("Tag", "Erro ao salvar dados", "Falha na persistência")
            return False
        
    except Exception as e:
        log_operacao("Tag", "Erro ao salvar dados", str(e))
        return False

def tag_registrar(tag: Dict[str, Any]) -> int:
    """
    Registra uma tag na estrutura encapsulada.
    
    Args:
        tag (Dict): Tag em formato dicionário a ser registrada
        
    Returns:
        int: 0 para sucesso, -1 para erro
    """
    if tag is None:
        log_operacao("Tag", "Erro ao registrar", "Ponteiro Tag nulo")
        return ERRO
    
    try:
        tag_id = tag_get_id(tag)
        if tag_id is None:
            log_operacao("Tag", "Erro ao registrar", "ID da tag inválido")
            return ERRO
        
        # Verifica se a tag já está registrada
        if tag_id in _tags_registradas:
            log_operacao("Tag", "Erro ao registrar", f"Tag {tag_id} já registrada")
            return ERRO
        
        # Registra a tag
        _tags_registradas[tag_id] = tag
        log_operacao("Tag", "Tag registrada", f"ID: {tag_id}")
        return SUCESSO
        
    except Exception as e:
        log_operacao("Tag", "Erro ao registrar", f"Falha: {str(e)}")
        return ERRO

def tag_listar_todas() -> List[Dict[str, Any]]:
    """
    Lista todas as tags registradas na estrutura encapsulada.
    
    Returns:
        List[Dict]: Lista de todas as tags em formato dicionário
    """
    return list(_tags_registradas.values())

# Funções da interface pública (conforme especificação)

def tag_criar(nome: str, cor: str) -> Optional[Dict[str, Any]]:
    """
    Cria uma nova tag com nome e cor fornecidos.
    
    Conforme especificação:
    Entrada: nome da tag e cor em hexadecimal (ex: "#FF0000")
    Saída: ponteiro para struct Tag criada, ou NULL em caso de erro
    
    Args:
        nome (str): Nome da tag (não pode ser nulo nem vazio)
        cor (str): Cor da tag em formato hexadecimal (#RRGGBB)
        
    Returns:
        Dict ou None: Tag em formato dicionário ou None em caso de erro
    """
    # Validação do nome
    if not validar_string_nao_vazia(nome, "nome"):
        log_operacao("Tag", "Erro ao criar", "Nome inválido")
        return None
    
    if len(nome) > MAX_NOME_LENGTH:
        log_operacao("Tag", "Erro ao criar", f"Nome muito longo (max {MAX_NOME_LENGTH})")
        return None
    
    # Validação da cor
    if not validar_string_nao_vazia(cor, "cor"):
        log_operacao("Tag", "Erro ao criar", "Cor inválida")
        return None
    
    if not validar_cor_hex(cor):
        log_operacao("Tag", "Erro ao criar", "Formato de cor inválido (use #RRGGBB)")
        return None
    
    try:
        # Cria a tag
        tag = _criar_tag_dict(nome.strip(), cor.upper())
        log_operacao("Tag", "Criada com sucesso", f"ID: {tag['id']}, Nome: {nome}, Cor: {cor}")
        return tag
        
    except Exception as e:
        log_operacao("Tag", "Erro ao criar", f"Falha na alocação: {str(e)}")
        return None

def tag_destruir(tag: Dict[str, Any]) -> None:
    """
    Libera os recursos alocados pela tag.
    
    Conforme especificação:
    Entrada: ponteiro para a struct Tag
    Saída: nenhuma (libera recursos alocados)
    
    Args:
        tag (Dict): Tag em formato dicionário a ser destruída
    """
    if tag is None:
        log_operacao("Tag", "Erro ao destruir", "Ponteiro nulo")
        return
    
    log_operacao("Tag", "Destruída", f"ID: {tag['id']}")
    # Em Python, o garbage collector cuida da liberação de memória
    tag.clear()

def tag_set_nome(tag: Dict[str, Any], novo_nome: str) -> int:
    """
    Altera o nome da tag.
    
    Conforme especificação:
    Entrada: ponteiro para tag e novo nome
    Saída: 0 em caso de sucesso, -1 em caso de erro
    
    Args:
        tag (Dict): Tag em formato dicionário
        novo_nome (str): Novo nome da tag
        
    Returns:
        int: 0 para sucesso, -1 para erro
    """
    if tag is None:
        log_operacao("Tag", "Erro ao alterar nome", "Ponteiro de tag nulo")
        return ERRO
    
    if not validar_string_nao_vazia(novo_nome, "novo_nome"):
        log_operacao("Tag", "Erro ao alterar nome", "Nome inválido")
        return ERRO
    
    if len(novo_nome) > MAX_NOME_LENGTH:
        log_operacao("Tag", "Erro ao alterar nome", f"Nome muito longo (max {MAX_NOME_LENGTH})")
        return ERRO
    
    try:
        nome_antigo = tag['nome']
        tag['nome'] = novo_nome.strip()
        tag['data_modificacao'] = datetime.now()
        
        log_operacao("Tag", "Nome alterado", f"ID: {tag['id']}, '{nome_antigo}' -> '{novo_nome}'")
        return SUCESSO
        
    except Exception as e:
        log_operacao("Tag", "Erro ao alterar nome", f"Falha: {str(e)}")
        return ERRO

def tag_set_cor(tag: Dict[str, Any], nova_cor: str) -> int:
    """
    Altera a cor da tag.
    
    Conforme especificação:
    Entrada: ponteiro para tag e nova cor
    Saída: 0 em caso de sucesso, -1 em caso de erro
    
    Args:
        tag (Dict): Tag em formato dicionário
        nova_cor (str): Nova cor da tag em formato hexadecimal (#RRGGBB)
        
    Returns:
        int: 0 para sucesso, -1 para erro
    """
    if tag is None:
        log_operacao("Tag", "Erro ao alterar cor", "Ponteiro de tag nulo")
        return ERRO
    
    if not validar_string_nao_vazia(nova_cor, "nova_cor"):
        log_operacao("Tag", "Erro ao alterar cor", "Cor inválida")
        return ERRO
    
    if not validar_cor_hex(nova_cor):
        log_operacao("Tag", "Erro ao alterar cor", "Formato de cor inválido (use #RRGGBB)")
        return ERRO
    
    try:
        cor_antiga = tag['cor']
        tag['cor'] = nova_cor.upper()
        tag['data_modificacao'] = datetime.now()
        
        log_operacao("Tag", "Cor alterada", f"ID: {tag['id']}, '{cor_antiga}' -> '{nova_cor}'")
        return SUCESSO
        
    except Exception as e:
        log_operacao("Tag", "Erro ao alterar cor", f"Falha: {str(e)}")
        return ERRO

def tag_get_nome(tag: Dict[str, Any]) -> Optional[str]:
    """
    Obtém o nome da tag.
    
    Conforme especificação:
    Entrada: ponteiro para a struct Tag
    Saída: string com o nome da tag
    
    Args:
        tag (Dict): Tag em formato dicionário
        
    Returns:
        str ou None: Nome da tag ou None em caso de erro
    """
    if tag is None:
        log_operacao("Tag", "Erro ao obter nome", "Ponteiro de tag nulo")
        return None
    
    try:
        return tag['nome']
    except Exception as e:
        log_operacao("Tag", "Erro ao obter nome", f"Falha: {str(e)}")
        return None

def tag_get_cor(tag: Dict[str, Any]) -> Optional[str]:
    """
    Obtém a cor da tag.
    
    Conforme especificação:
    Entrada: ponteiro para a struct Tag
    Saída: string com a cor da tag
    
    Args:
        tag (Dict): Tag em formato dicionário
        
    Returns:
        str ou None: Cor da tag ou None em caso de erro
    """
    if tag is None:
        log_operacao("Tag", "Erro ao obter cor", "Ponteiro de tag nulo")
        return None
    
    try:
        return tag['cor']
    except Exception as e:
        log_operacao("Tag", "Erro ao obter cor", f"Falha: {str(e)}")
        return None

def tag_get_id(tag: Dict[str, Any]) -> Optional[int]:
    """
    Obtém o ID da tag.
    
    Args:
        tag (Dict): Tag em formato dicionário
        
    Returns:
        int ou None: ID da tag ou None em caso de erro
    """
    if tag is None:
        return None
    
    try:
        return tag['id']
    except Exception as e:
        log_operacao("Tag", "Erro ao obter ID", f"Falha: {str(e)}")
        return None

