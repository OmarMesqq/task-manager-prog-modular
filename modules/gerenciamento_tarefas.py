"""
Módulo de Gerenciamento de Tarefas

Este módulo é responsável por orquestrar a lógica de gerenciamento de tarefas
(criação, exclusão, alteração e consulta) a partir das informações que consome
das demais entidades do sistema (Time, Tarefa, Tag e Usuario).

Funções principais:
- gt_inicializar: Inicializa o sistema de gerenciamento
- gt_finalizar: Finaliza e libera recursos
- gt_registrar_time: Registra um time no sistema
- gt_criar_tarefa: Cria uma nova tarefa
- gt_remover_tarefa: Remove uma tarefa
- gt_listar_tarefas_time: Lista tarefas de um time

Conforme especificação: Este módulo atua como cliente dos módulos Time, Tarefa,
Tag e Usuario, utilizando suas funções para orquestrar a lógica de gerenciamento.

WORKFLOW DE PERSISTÊNCIA:
- Inicialização: Carrega dados dos JSONs uma única vez usando as estruturas encapsuladas dos módulos
- Durante execução: Todas as operações trabalham apenas com variáveis em memória
- Finalização: Salva todos os dados nos JSONs uma única vez usando as estruturas encapsuladas dos módulos
"""

from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
import sys
import os

# Adiciona o diretório raiz ao path se não estiver lá
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from config import SUCESSO, ERRO
from utils import log_operacao, exportar_para_csv
from modules.usuario import *
from modules.tag import *
from modules.team import *
from modules.tarefa import *

def gt_inicializar() -> Optional[Dict[str, Any]]:
    """
    Inicializa o sistema de gerenciamento de tarefas.
    Carrega dados dos JSONs uma única vez usando as estruturas encapsuladas dos módulos.
    
    Conforme especificação:
    Entrada: nenhuma
    Saída: Ponteiro para a struct GT
    
    Returns:
        Dict ou None: Sistema GT em formato dicionário ou None se erro
    """
    try:
        # Carrega dados usando as estruturas encapsuladas dos módulos
        usuario_carregar_dados()
        tag_carregar_dados()
        time_carregar_dados()
        tarefa_carregar_dados()
        
        # Cria um dicionário vazio para representar o sistema GT
        # (os dados reais estão nas estruturas encapsuladas dos módulos)
        gt = {}
        
        log_operacao("GerenciamentoTarefas", "Inicializado", "Sistema pronto")
        return gt
    except Exception as e:
        log_operacao("GerenciamentoTarefas", "Erro ao inicializar", str(e))
        return None

def gt_finalizar(gt: Dict[str, Any]) -> None:
    """
    Finaliza o sistema e libera recursos.
    Salva dados nos JSONs uma única vez usando as estruturas encapsuladas dos módulos.
    
    Conforme especificação:
    Entrada: Ponteiro para a struct GT
    Saída: nenhuma (libera os recursos alocados)
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
    """
    if gt is None:
        log_operacao("GerenciamentoTarefas", "Erro ao finalizar", "Ponteiro nulo")
        return
    
    # Salva dados usando as estruturas encapsuladas dos módulos
    usuario_salvar_dados()
    tag_salvar_dados()
    time_salvar_dados()
    tarefa_salvar_dados()
    
    # Limpa o dicionário GT
    gt.clear()
    
    log_operacao("GerenciamentoTarefas", "Finalizado", "Sistema encerrado")

def gt_registrar_time(gt: Dict[str, Any], time: Dict[str, Any]) -> int:
    """
    Registra um time no sistema.
    Operação realizada apenas em memória - não salva no JSON.
    
    Conforme especificação:
    Entrada: Ponteiro para a struct GT e ponteiro para struct Time a ser registrada
    Saída: inteiro indicando sucesso (0) ou erro (por exemplo, GT ou Time nulo)
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
        time (Dict): Time em formato dicionário a ser registrado
        
    Returns:
        int: 0 para sucesso, -1 para erro
    """
    if gt is None:
        log_operacao("GerenciamentoTarefas", "Erro ao registrar time", "Ponteiro GT nulo")
        return ERRO
    
    if time is None:
        log_operacao("GerenciamentoTarefas", "Erro ao registrar time", "Ponteiro Time nulo")
        return ERRO
    
    try:
        # Registra o time usando a estrutura encapsulada do módulo team
        resultado = time_registrar(time)
        if resultado == SUCESSO:
            log_operacao("GerenciamentoTarefas", "Time registrado", f"ID: {time_get_id(time)}")
        return resultado
        
    except Exception as e:
        log_operacao("GerenciamentoTarefas", "Erro ao registrar time", f"Falha: {str(e)}")
        return ERRO

def gt_criar_tarefa(gt: Dict[str, Any], time: Dict[str, Any], titulo: str, descricao: str, 
                   usuario: Dict[str, Any], tags: List, qtd_tags: int, prazo: datetime) -> Optional[Dict[str, Any]]:
    """
    Cria uma nova tarefa no sistema.
    Operação realizada apenas em memória - não salva no JSON.
    
    Conforme especificação:
    Entrada: Ponteiro para a struct GT, ponteiro para struct Time, string com título,
    string com descrição, ponteiro para struct Usuario, vetor de ponteiros para Tag,
    quantidade de tags e prazo da tarefa
    Saída: ponteiro para struct Tarefa criada ou NULL em caso de erro
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
        time (Dict): Time em formato dicionário
        titulo (str): Título da tarefa
        descricao (str): Descrição da tarefa
        usuario (Dict): Usuário responsável em formato dicionário
        tags (List): Lista de tags em formato dicionário
        qtd_tags (int): Quantidade de tags
        prazo (datetime): Prazo da tarefa
        
    Returns:
        Dict ou None: Tarefa criada em formato dicionário ou None em caso de erro
    """
    if gt is None:
        log_operacao("GerenciamentoTarefas", "Erro ao criar tarefa", "Ponteiro GT nulo")
        return None
    
    if time is None:
        log_operacao("GerenciamentoTarefas", "Erro ao criar tarefa", "Ponteiro Time nulo")
        return None
    
    if usuario is None:
        log_operacao("GerenciamentoTarefas", "Erro ao criar tarefa", "Ponteiro Usuario nulo")
        return None
    
    try:
        # Verifica se o time está registrado
        time_id = time_get_id(time)
        if time_id is None:
            log_operacao("GerenciamentoTarefas", "Erro ao criar tarefa", "Time inválido")
            return None
        
        # Verifica se o usuário está registrado
        usuario_id = usuario_get_id(usuario)
        if usuario_id is None:
            log_operacao("GerenciamentoTarefas", "Erro ao criar tarefa", "Usuário inválido")
            return None
        
        # Cria a tarefa
        tarefa = tarefa_criar(titulo, descricao, usuario, prazo)
        if tarefa is None:
            log_operacao("GerenciamentoTarefas", "Erro ao criar tarefa", "Falha na criação da tarefa")
            return None
        
        # Adiciona as tags à tarefa
        for i in range(min(qtd_tags, len(tags))):
            if tags[i] is not None:
                tarefa_add_tag(tarefa, tags[i])
        
        # Registra a tarefa usando a estrutura encapsulada do módulo tarefa
        if tarefa_registrar(tarefa) == SUCESSO:
            log_operacao("GerenciamentoTarefas", "Tarefa criada", f"ID: {tarefa_get_id(tarefa)}, Título: {titulo}")
            return tarefa
        else:
            log_operacao("GerenciamentoTarefas", "Erro ao criar tarefa", "Falha no registro da tarefa")
            return None
        
    except Exception as e:
        log_operacao("GerenciamentoTarefas", "Erro ao criar tarefa", f"Falha: {str(e)}")
        return None

def gt_remover_tarefa(gt: Dict[str, Any], tarefa: Dict[str, Any]) -> int:
    """
    Remove uma tarefa do sistema.
    Operação realizada apenas em memória - não salva no JSON.
    
    Conforme especificação:
    Entrada: Ponteiro para a struct GT e ponteiro para struct Tarefa a ser removida
    Saída: inteiro indicando sucesso (0) ou erro (por exemplo, tarefa inexistente)
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
        tarefa (Dict): Tarefa em formato dicionário a ser removida
        
    Returns:
        int: 0 para sucesso, -1 para erro
    """
    if gt is None:
        log_operacao("GerenciamentoTarefas", "Erro ao remover tarefa", "Ponteiro GT nulo")
        return ERRO
    
    if tarefa is None:
        log_operacao("GerenciamentoTarefas", "Erro ao remover tarefa", "Ponteiro Tarefa nulo")
        return ERRO
    
    try:
        tarefa_id = tarefa_get_id(tarefa)
        if tarefa_id is None:
            log_operacao("GerenciamentoTarefas", "Erro ao remover tarefa", "ID da tarefa inválido")
            return ERRO
        
        # Remove a tarefa da estrutura encapsulada do módulo tarefa
        # (implementação específica seria necessária no módulo tarefa)
        # Por enquanto, apenas destrói a tarefa
        tarefa_destruir(tarefa)
        
        log_operacao("GerenciamentoTarefas", "Tarefa removida", f"ID: {tarefa_id}")
        return SUCESSO
        
    except Exception as e:
        log_operacao("GerenciamentoTarefas", "Erro ao remover tarefa", f"Falha: {str(e)}")
        return ERRO

def gt_listar_tarefas_time(gt: Dict[str, Any], time: Dict[str, Any], qtd_out: List[int]) -> Optional[List[Dict[str, Any]]]:
    """
    Lista todas as tarefas de um time específico.
    Consulta realizada apenas em memória.
    
    Conforme especificação:
    Entrada: Ponteiro para a struct GT, ponteiro para struct Time e ponteiro para
    inteiro que receberá a quantidade de tarefas encontradas
    Saída: vetor de ponteiros para struct Tarefa ou NULL em caso de erro
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
        time (Dict): Time em formato dicionário
        qtd_out (List[int]): Lista para receber a quantidade de tarefas
        
    Returns:
        List[Dict] ou None: Lista de tarefas em formato dicionário ou None em caso de erro
    """
    if gt is None:
        log_operacao("GerenciamentoTarefas", "Erro ao listar tarefas", "Ponteiro GT nulo")
        return None
    
    if time is None:
        log_operacao("GerenciamentoTarefas", "Erro ao listar tarefas", "Ponteiro Time nulo")
        return None
    
    if qtd_out is None:
        log_operacao("GerenciamentoTarefas", "Erro ao listar tarefas", "Ponteiro qtd_out nulo")
        return None
    
    try:
        time_id = time_get_id(time)
        if time_id is None:
            log_operacao("GerenciamentoTarefas", "Erro ao listar tarefas", "Time inválido")
            return None
        
        # Lista todas as tarefas (assumindo que todas pertencem ao time)
        # Em uma implementação mais completa, haveria associação tarefa-time
        tarefas_time = tarefa_listar_todas()
        
        qtd_out[0] = len(tarefas_time)
        log_operacao("GerenciamentoTarefas", "Tarefas listadas", f"Time ID: {time_id}, Qtd: {len(tarefas_time)}")
        return tarefas_time
        
    except Exception as e:
        log_operacao("GerenciamentoTarefas", "Erro ao listar tarefas", f"Falha: {str(e)}")
        return None

def gt_registrar_usuario(gt: Dict[str, Any], usuario: Dict[str, Any]) -> int:
    """
    Registra um usuário no sistema.
    Operação realizada apenas em memória - não salva no JSON.
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
        usuario (Dict): Usuário em formato dicionário a ser registrado
        
    Returns:
        int: 0 para sucesso, -1 para erro
    """
    if gt is None:
        log_operacao("GerenciamentoTarefas", "Erro ao registrar usuário", "Ponteiro GT nulo")
        return ERRO
    
    if usuario is None:
        log_operacao("GerenciamentoTarefas", "Erro ao registrar usuário", "Ponteiro Usuario nulo")
        return ERRO
    
    try:
        # Registra o usuário usando a estrutura encapsulada do módulo usuario
        resultado = usuario_registrar(usuario)
        if resultado == SUCESSO:
            log_operacao("GerenciamentoTarefas", "Usuário registrado", f"ID: {usuario_get_id(usuario)}")
        return resultado
        
    except Exception as e:
        log_operacao("GerenciamentoTarefas", "Erro ao registrar usuário", f"Falha: {str(e)}")
        return ERRO

def gt_registrar_tag(gt: Dict[str, Any], tag: Dict[str, Any]) -> int:
    """
    Registra uma tag no sistema.
    Operação realizada apenas em memória - não salva no JSON.
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
        tag (Dict): Tag em formato dicionário a ser registrada
        
    Returns:
        int: 0 para sucesso, -1 para erro
    """
    if gt is None:
        log_operacao("GerenciamentoTarefas", "Erro ao registrar tag", "Ponteiro GT nulo")
        return ERRO
    
    if tag is None:
        log_operacao("GerenciamentoTarefas", "Erro ao registrar tag", "Ponteiro Tag nulo")
        return ERRO
    
    try:
        # Registra a tag usando a estrutura encapsulada do módulo tag
        resultado = tag_registrar(tag)
        if resultado == SUCESSO:
            log_operacao("GerenciamentoTarefas", "Tag registrada", f"ID: {tag_get_id(tag)}")
        return resultado
        
    except Exception as e:
        log_operacao("GerenciamentoTarefas", "Erro ao registrar tag", f"Falha: {str(e)}")
        return ERRO

def gt_listar_todas_tarefas(gt: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Lista todas as tarefas do sistema.
    Consulta realizada apenas em memória.
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
        
    Returns:
        List[Dict]: Lista de todas as tarefas em formato dicionário
    """
    if gt is None:
        return []
    
    return tarefa_listar_todas()

def gt_listar_todos_usuarios(gt: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Lista todos os usuários do sistema.
    Consulta realizada apenas em memória.
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
        
    Returns:
        List[Dict]: Lista de todos os usuários em formato dicionário
    """
    if gt is None:
        return []
    
    return usuario_listar_todos()

def gt_listar_todas_tags(gt: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Lista todas as tags do sistema.
    Consulta realizada apenas em memória.
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
        
    Returns:
        List[Dict]: Lista de todas as tags em formato dicionário
    """
    if gt is None:
        return []
    
    return tag_listar_todas()

def gt_listar_todos_times(gt: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Lista todos os times do sistema.
    Consulta realizada apenas em memória.
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
        
    Returns:
        List[Dict]: Lista de todos os times em formato dicionário
    """
    if gt is None:
        return []
    
    return time_listar_todos()

def gt_exportar_tarefas_csv(gt: Dict[str, Any], nome_arquivo: str) -> bool:
    """
    Exporta as tarefas para um arquivo CSV.
    Usa dados em memória para exportação.
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
        nome_arquivo (str): Nome do arquivo CSV
        
    Returns:
        bool: True se exportou com sucesso, False caso contrário
    """
    if gt is None:
        log_operacao("GerenciamentoTarefas", "Erro ao exportar CSV", "Ponteiro GT nulo")
        return False
    
    try:
        # Obtém todas as tarefas da estrutura encapsulada
        tarefas = tarefa_listar_todas()
        
        # Prepara os dados para exportação
        dados_exportacao = []
        for tarefa in tarefas:
            dados_exportacao.append({
                'ID': tarefa['id'],
                'Título': tarefa['titulo'],
                'Descrição': tarefa['descricao'],
                'Status': tarefa['status'].value if hasattr(tarefa['status'], 'value') else str(tarefa['status']),
                'Usuário Responsável': tarefa['usuario_responsavel_id'],
                'Prazo': str(tarefa['prazo']),
                'Tags': ', '.join(map(str, tarefa['tags'])),
                'Data Criação': str(tarefa['data_criacao']),
                'Data Modificação': str(tarefa['data_modificacao'])
            })
        
        # Exporta para CSV
        if exportar_para_csv(dados_exportacao, nome_arquivo):
            log_operacao("GerenciamentoTarefas", "CSV exportado", f"Arquivo: {nome_arquivo}")
            return True
        else:
            log_operacao("GerenciamentoTarefas", "Erro ao exportar CSV", "Falha na exportação")
            return False
            
    except Exception as e:
        log_operacao("GerenciamentoTarefas", "Erro ao exportar CSV", f"Falha: {str(e)}")
        return False

