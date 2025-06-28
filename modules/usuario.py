"""
Módulo de Cadastro de Usuario

Este módulo é responsável por gerenciar a entidade "Usuario" dentro do sistema.
Cada usuário representa uma pessoa que pode ser responsável por tarefas.

Funções principais:
- usuario_criar: Cria um novo usuário
- usuario_destruir: Libera recursos de um usuário
- usuario_set_email: Altera o email de um usuário
- usuario_get_nome: Obtém o nome de um usuário
- usuario_get_email: Obtém o email de um usuário

Conforme especificação: O módulo não conhece nem depende dos outros módulos.
Ele apenas expõe sua interface por meio de funções públicas.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
import sys
import os

#Encapsulamento

__all__ = [
    "usuario_criar",
    "usuario_destruir",
    "usuario_set_email",
    "usuario_get_nome",
    "usuario_get_email",
    "usuario_get_id",
    "usuario_to_dict",
    "usuario_from_dict"
]

# Adiciona o diretório raiz ao path se não estiver lá
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from config import SUCESSO, ERRO, validar_email, MAX_NOME_LENGTH, MAX_EMAIL_LENGTH
from utils import gerar_id_unico, validar_string_nao_vazia, log_operacao, formatar_data

def _criar_usuario_dict(nome: str, email: str) -> Dict[str, Any]:
    """
    Cria um dicionário representando um usuário.
    
    Args:
        nome (str): Nome do usuário
        email (str): Email do usuário
        
    Returns:
        Dict: Dicionário representando o usuário
    """
    return {
        'id': gerar_id_unico(),
        'nome': nome,
        'email': email,
        'data_criacao': datetime.now(),
        'data_modificacao': datetime.now()
    }

def usuario_to_dict(usuario: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converte o usuário para dicionário (para persistência).
    
    Args:
        usuario (Dict): Usuário em formato dicionário
        
    Returns:
        Dict: Representação do usuário em dicionário para persistência
    """
    return {
        'id': usuario['id'],
        'nome': usuario['nome'],
        'email': usuario['email'],
        'data_criacao': formatar_data(usuario['data_criacao']),
        'data_modificacao': formatar_data(usuario['data_modificacao'])
    }

def usuario_from_dict(dados: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Cria um usuário a partir de um dicionário.
    
    Args:
        dados (Dict): Dados do usuário
        
    Returns:
        Dict ou None: Usuário em formato dicionário ou None em caso de erro
    """
    from utils import parse_data
    
    try:
        usuario = {
            'id': dados['id'],
            'nome': dados['nome'],
            'email': dados['email'],
            'data_criacao': parse_data(dados['data_criacao']),
            'data_modificacao': parse_data(dados['data_modificacao'])
        }
        return usuario
    except Exception as e:
        print(f"Erro ao criar usuário a partir de dict: {e}")
        return None

# Funções da interface pública (conforme especificação)

def usuario_criar(nome: str, email: str) -> Optional[Dict[str, Any]]:
    """
    Cria um novo usuário com nome e email fornecidos.
    
    Conforme especificação:
    Entrada: string com nome e e-mail do usuário
    Saída: ponteiro para a struct Usuario criada, ou NULL em caso de erro
    
    Args:
        nome (str): Nome do usuário (não pode ser nulo nem vazio)
        email (str): Email do usuário (não pode ser nulo nem vazio, deve ser válido)
        
    Returns:
        Dict ou None: Usuário em formato dicionário ou None em caso de erro
    """
    # Validação do nome
    if not validar_string_nao_vazia(nome, "nome"):
        log_operacao("Usuario", "Erro ao criar", "Nome inválido")
        return None
    
    if len(nome) > MAX_NOME_LENGTH:
        log_operacao("Usuario", "Erro ao criar", f"Nome muito longo (max {MAX_NOME_LENGTH})")
        return None
    
    # Validação do email
    if not validar_string_nao_vazia(email, "email"):
        log_operacao("Usuario", "Erro ao criar", "Email inválido")
        return None
    
    if len(email) > MAX_EMAIL_LENGTH:
        log_operacao("Usuario", "Erro ao criar", f"Email muito longo (max {MAX_EMAIL_LENGTH})")
        return None
    
    if not validar_email(email):
        log_operacao("Usuario", "Erro ao criar", "Formato de email inválido")
        return None
    
    try:
        # Cria o usuário
        usuario = _criar_usuario_dict(nome.strip(), email.strip().lower())
        log_operacao("Usuario", "Criado com sucesso", f"ID: {usuario['id']}, Nome: {nome}")
        return usuario
        
    except Exception as e:
        log_operacao("Usuario", "Erro ao criar", f"Falha na alocação: {str(e)}")
        return None

def usuario_destruir(usuario: Dict[str, Any]) -> None:
    """
    Libera os recursos alocados pelo usuário.
    
    Conforme especificação:
    Entrada: ponteiro para struct Usuario
    Saída: nenhuma (libera a memória alocada)
    
    Args:
        usuario (Dict): Usuário em formato dicionário a ser destruído
    """
    if usuario is None:
        log_operacao("Usuario", "Erro ao destruir", "Ponteiro nulo")
        return
    
    log_operacao("Usuario", "Destruído", f"ID: {usuario['id']}")
    # Em Python, o garbage collector cuida da liberação de memória
    # Mas podemos limpar as referências explicitamente se necessário
    usuario.clear()

def usuario_set_email(usuario: Dict[str, Any], novo_email: str) -> int:
    """
    Altera o email do usuário.
    
    Conforme especificação:
    Entrada: ponteiro para struct Usuario e string com novo e-mail
    Saída: 0 se sucesso, -1 se houver erro (como ponteiros nulos ou formato inválido)
    
    Args:
        usuario (Dict): Usuário em formato dicionário
        novo_email (str): Novo email do usuário
        
    Returns:
        int: 0 para sucesso, -1 para erro
    """
    if usuario is None:
        log_operacao("Usuario", "Erro ao alterar email", "Ponteiro de usuário nulo")
        return ERRO
    
    if not validar_string_nao_vazia(novo_email, "novo_email"):
        log_operacao("Usuario", "Erro ao alterar email", "Email inválido")
        return ERRO
    
    if len(novo_email) > MAX_EMAIL_LENGTH:
        log_operacao("Usuario", "Erro ao alterar email", f"Email muito longo (max {MAX_EMAIL_LENGTH})")
        return ERRO
    
    if not validar_email(novo_email):
        log_operacao("Usuario", "Erro ao alterar email", "Formato de email inválido")
        return ERRO
    
    try:
        email_antigo = usuario['email']
        usuario['email'] = novo_email.strip().lower()
        usuario['data_modificacao'] = datetime.now()
        log_operacao("Usuario", "Email alterado", f"ID: {usuario['id']}, De: {email_antigo} Para: {novo_email}")
        return SUCESSO
        
    except Exception as e:
        log_operacao("Usuario", "Erro ao alterar email", f"Falha: {str(e)}")
        return ERRO

def usuario_get_nome(usuario: Dict[str, Any]) -> Optional[str]:
    """
    Obtém o nome do usuário.
    
    Conforme especificação:
    Entrada: ponteiro para struct Usuario
    Saída: string com o nome do usuário
    
    Args:
        usuario (Dict): Usuário em formato dicionário
        
    Returns:
        str ou None: Nome do usuário ou None em caso de erro
    """
    if usuario is None:
        log_operacao("Usuario", "Erro ao obter nome", "Ponteiro de usuário nulo")
        return None
    
    try:
        return usuario['nome']
    except KeyError:
        log_operacao("Usuario", "Erro ao obter nome", "Campo nome não encontrado")
        return None

def usuario_get_email(usuario: Dict[str, Any]) -> Optional[str]:
    """
    Obtém o email do usuário.
    
    Conforme especificação:
    Entrada: ponteiro para struct Usuario
    Saída: string com o e-mail do usuário
    
    Args:
        usuario (Dict): Usuário em formato dicionário
        
    Returns:
        str ou None: Email do usuário ou None em caso de erro
    """
    if usuario is None:
        log_operacao("Usuario", "Erro ao obter email", "Ponteiro de usuário nulo")
        return None
    
    try:
        return usuario['email']
    except KeyError:
        log_operacao("Usuario", "Erro ao obter email", "Campo email não encontrado")
        return None

def usuario_get_id(usuario: Dict[str, Any]) -> Optional[int]:
    """
    Obtém o ID do usuário.
    
    Conforme especificação:
    Entrada: ponteiro para struct Usuario
    Saída: ID do usuário
    
    Args:
        usuario (Dict): Usuário em formato dicionário
        
    Returns:
        int ou None: ID do usuário ou None em caso de erro
    """
    if usuario is None:
        log_operacao("Usuario", "Erro ao obter ID", "Ponteiro de usuário nulo")
        return None
    
    try:
        return usuario['id']
    except KeyError:
        log_operacao("Usuario", "Erro ao obter ID", "Campo ID não encontrado")
        return None

