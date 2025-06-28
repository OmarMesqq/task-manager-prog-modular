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

from config import SUCESSO, ERRO, USUARIOS_FILE, TAGS_FILE, TIMES_FILE, TAREFAS_FILE
from utils import salvar_json, carregar_json, log_operacao, exportar_para_csv
from modules.usuario import *
from modules.tag import *
from modules.team import *
from modules.tarefa import *

def criar_gt_dict() -> Dict[str, Any]:
    """
    Cria um dicionário representando o sistema de gerenciamento de tarefas.
    
    Returns:
        Dict: Dicionário representando o sistema GT
    """
    return {
        'usuarios': {},  # Dict[int, Dict] - usuários em formato dicionário
        'tags': {},      # Dict[int, Dict] - tags em formato dicionário
        'times': {},     # Dict[int, Dict] - times em formato dicionário
        'tarefas': {}    # Dict[int, Dict] - tarefas em formato dicionário
    }

def carregar_dados(gt: Dict[str, Any]) -> None:
    """
    Carrega dados persistidos dos arquivos JSON.
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
    """
    try:
        # Carrega usuários
        dados_usuarios = carregar_json(USUARIOS_FILE)
        if dados_usuarios:
            for user_data in dados_usuarios.values():
                usuario = usuario_from_dict(user_data)
                if usuario:
                    gt['usuarios'][usuario['id']] = usuario
        
        # Carrega tags
        dados_tags = carregar_json(TAGS_FILE)
        if dados_tags:
            for tag_data in dados_tags.values():
                tag = tag_from_dict(tag_data)
                if tag:
                    gt['tags'][tag['id']] = tag
        
        # Carrega times
        dados_times = carregar_json(TIMES_FILE)
        if dados_times:
            for time_data in dados_times.values():
                time = time_from_dict(time_data)
                if time:
                    gt['times'][time['id']] = time
        
        # Carrega tarefas
        dados_tarefas = carregar_json(TAREFAS_FILE)
        if dados_tarefas:
            for tarefa_data in dados_tarefas.values():
                tarefa = tarefa_from_dict(tarefa_data)
                if tarefa:
                    gt['tarefas'][tarefa['id']] = tarefa
        
        log_operacao("GerenciamentoTarefas", "Dados carregados", 
                    f"Usuários: {len(gt['usuarios'])}, Tags: {len(gt['tags'])}, "
                    f"Times: {len(gt['times'])}, Tarefas: {len(gt['tarefas'])}")
                    
    except Exception as e:
        log_operacao("GerenciamentoTarefas", "Erro ao carregar dados", str(e))

def salvar_dados(gt: Dict[str, Any]) -> bool:
    """
    Salva todos os dados nos arquivos JSON.
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
        
    Returns:
        bool: True se salvou com sucesso, False caso contrário
    """
    try:
        # Salva usuários
        dados_usuarios = {str(uid): usuario_to_dict(user) for uid, user in gt['usuarios'].items()}
        if not salvar_json(dados_usuarios, USUARIOS_FILE):
            return False
        
        # Salva tags
        dados_tags = {str(tid): tag_to_dict(tag) for tid, tag in gt['tags'].items()}
        if not salvar_json(dados_tags, TAGS_FILE):
            return False
        
        # Salva times
        dados_times = {str(tid): time_to_dict(time) for tid, time in gt['times'].items()}
        if not salvar_json(dados_times, TIMES_FILE):
            return False
        
        # Salva tarefas
        dados_tarefas = {str(tid): tarefa_to_dict(tarefa) for tid, tarefa in gt['tarefas'].items()}
        if not salvar_json(dados_tarefas, TAREFAS_FILE):
            return False
        
        log_operacao("GerenciamentoTarefas", "Dados salvos", "Persistência realizada com sucesso")
        return True
        
    except Exception as e:
        log_operacao("GerenciamentoTarefas", "Erro ao salvar dados", str(e))
        return False

# Funções da interface pública (conforme especificação)

def gt_inicializar() -> Optional[Dict[str, Any]]:
    """
    Inicializa o sistema de gerenciamento de tarefas.
    
    Conforme especificação:
    Entrada: nenhuma
    Saída: Ponteiro para a struct GT
    
    Returns:
        Dict ou None: Sistema GT em formato dicionário ou None se erro
    """
    try:
        gt = criar_gt_dict()
        carregar_dados(gt)
        log_operacao("GerenciamentoTarefas", "Inicializado", "Sistema pronto")
        return gt
    except Exception as e:
        log_operacao("GerenciamentoTarefas", "Erro ao inicializar", str(e))
        return None

def gt_finalizar(gt: Dict[str, Any]) -> None:
    """
    Finaliza o sistema e libera recursos.
    
    Conforme especificação:
    Entrada: Ponteiro para a struct GT
    Saída: nenhuma (libera os recursos alocados)
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
    """
    if gt is None:
        log_operacao("GerenciamentoTarefas", "Erro ao finalizar", "Ponteiro nulo")
        return
    
    # Salva dados antes de finalizar
    salvar_dados(gt)
    
    # Limpa as estruturas
    gt['usuarios'].clear()
    gt['tags'].clear()
    gt['times'].clear()
    gt['tarefas'].clear()
    
    log_operacao("GerenciamentoTarefas", "Finalizado", "Sistema encerrado")

def gt_registrar_time(gt: Dict[str, Any], time: Dict[str, Any]) -> int:
    """
    Registra um time no sistema.
    
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
        time_id = time_get_id(time)
        if time_id is None:
            log_operacao("GerenciamentoTarefas", "Erro ao registrar time", "ID do time inválido")
            return ERRO
        
        # Verifica se o time já está registrado
        if time_id in gt['times']:
            log_operacao("GerenciamentoTarefas", "Erro ao registrar time", f"Time {time_id} já registrado")
            return ERRO
        
        # Registra o time
        gt['times'][time_id] = time
        log_operacao("GerenciamentoTarefas", "Time registrado", f"ID: {time_id}")
        return SUCESSO
        
    except Exception as e:
        log_operacao("GerenciamentoTarefas", "Erro ao registrar time", f"Falha: {str(e)}")
        return ERRO

def gt_criar_tarefa(gt: Dict[str, Any], time: Dict[str, Any], titulo: str, descricao: str, 
                   usuario: Dict[str, Any], tags: List, qtd_tags: int, prazo: datetime) -> Optional[Dict[str, Any]]:
    """
    Cria uma nova tarefa no sistema.
    
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
        if time_id is None or time_id not in gt['times']:
            log_operacao("GerenciamentoTarefas", "Erro ao criar tarefa", "Time não registrado")
            return None
        
        # Verifica se o usuário está registrado
        usuario_id = usuario_get_id(usuario)
        if usuario_id is None or usuario_id not in gt['usuarios']:
            log_operacao("GerenciamentoTarefas", "Erro ao criar tarefa", "Usuário não registrado")
            return None
        
        # Cria a tarefa
        tarefa = tarefa_criar(titulo, descricao, usuario, prazo)
        if tarefa is None:
            log_operacao("GerenciamentoTarefas", "Erro ao criar tarefa", "Falha na criação da tarefa")
            return None
        
        # Adiciona as tags à tarefa
        for i in range(min(qtd_tags, len(tags))):
            if tags[i] is not None:
                tag_id = tag_get_id(tags[i])
                if tag_id is not None and tag_id in gt['tags']:
                    from modules.tarefa import tarefa_add_tag
                    tarefa_add_tag(tarefa, tags[i])
        
        # Registra a tarefa no sistema
        tarefa_id = tarefa_get_id(tarefa)
        gt['tarefas'][tarefa_id] = tarefa
        
        log_operacao("GerenciamentoTarefas", "Tarefa criada", f"ID: {tarefa_id}, Título: {titulo}")
        return tarefa
        
    except Exception as e:
        log_operacao("GerenciamentoTarefas", "Erro ao criar tarefa", f"Falha: {str(e)}")
        return None

def gt_remover_tarefa(gt: Dict[str, Any], tarefa: Dict[str, Any]) -> int:
    """
    Remove uma tarefa do sistema.
    
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
        
        # Verifica se a tarefa está registrada
        if tarefa_id not in gt['tarefas']:
            log_operacao("GerenciamentoTarefas", "Erro ao remover tarefa", f"Tarefa {tarefa_id} não registrada")
            return ERRO
        
        # Remove a tarefa
        del gt['tarefas'][tarefa_id]
        from modules.tarefa import tarefa_destruir
        tarefa_destruir(tarefa)
        
        log_operacao("GerenciamentoTarefas", "Tarefa removida", f"ID: {tarefa_id}")
        return SUCESSO
        
    except Exception as e:
        log_operacao("GerenciamentoTarefas", "Erro ao remover tarefa", f"Falha: {str(e)}")
        return ERRO

def gt_listar_tarefas_time(gt: Dict[str, Any], time: Dict[str, Any], qtd_out: List[int]) -> Optional[List[Dict[str, Any]]]:
    """
    Lista todas as tarefas de um time específico.
    
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
        if time_id is None or time_id not in gt['times']:
            log_operacao("GerenciamentoTarefas", "Erro ao listar tarefas", "Time não registrado")
            return None
        
        # Filtra tarefas do time (assumindo que tarefas têm associação com time)
        tarefas_time = []
        for tarefa in gt['tarefas'].values():
            # Aqui você pode implementar a lógica específica de associação tarefa-time
            # Por enquanto, retornamos todas as tarefas
            tarefas_time.append(tarefa)
        
        qtd_out[0] = len(tarefas_time)
        log_operacao("GerenciamentoTarefas", "Tarefas listadas", f"Time ID: {time_id}, Qtd: {len(tarefas_time)}")
        return tarefas_time
        
    except Exception as e:
        log_operacao("GerenciamentoTarefas", "Erro ao listar tarefas", f"Falha: {str(e)}")
        return None

def gt_registrar_usuario(gt: Dict[str, Any], usuario: Dict[str, Any]) -> int:
    """
    Registra um usuário no sistema.
    
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
        usuario_id = usuario_get_id(usuario)
        if usuario_id is None:
            log_operacao("GerenciamentoTarefas", "Erro ao registrar usuário", "ID do usuário inválido")
            return ERRO
        
        # Verifica se o usuário já está registrado
        if usuario_id in gt['usuarios']:
            log_operacao("GerenciamentoTarefas", "Erro ao registrar usuário", f"Usuário {usuario_id} já registrado")
            return ERRO
        
        # Registra o usuário
        gt['usuarios'][usuario_id] = usuario
        log_operacao("GerenciamentoTarefas", "Usuário registrado", f"ID: {usuario_id}")
        return SUCESSO
        
    except Exception as e:
        log_operacao("GerenciamentoTarefas", "Erro ao registrar usuário", f"Falha: {str(e)}")
        return ERRO

def gt_registrar_tag(gt: Dict[str, Any], tag: Dict[str, Any]) -> int:
    """
    Registra uma tag no sistema.
    
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
        tag_id = tag_get_id(tag)
        if tag_id is None:
            log_operacao("GerenciamentoTarefas", "Erro ao registrar tag", "ID da tag inválido")
            return ERRO
        
        # Verifica se a tag já está registrada
        if tag_id in gt['tags']:
            log_operacao("GerenciamentoTarefas", "Erro ao registrar tag", f"Tag {tag_id} já registrada")
            return ERRO
        
        # Registra a tag
        gt['tags'][tag_id] = tag
        log_operacao("GerenciamentoTarefas", "Tag registrada", f"ID: {tag_id}")
        return SUCESSO
        
    except Exception as e:
        log_operacao("GerenciamentoTarefas", "Erro ao registrar tag", f"Falha: {str(e)}")
        return ERRO

def gt_listar_todas_tarefas(gt: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Lista todas as tarefas do sistema.
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
        
    Returns:
        List[Dict]: Lista de todas as tarefas em formato dicionário
    """
    if gt is None:
        return []
    
    return list(gt['tarefas'].values())

def gt_listar_todos_usuarios(gt: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Lista todos os usuários do sistema.
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
        
    Returns:
        List[Dict]: Lista de todos os usuários em formato dicionário
    """
    if gt is None:
        return []
    
    return list(gt['usuarios'].values())

def gt_listar_todas_tags(gt: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Lista todas as tags do sistema.
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
        
    Returns:
        List[Dict]: Lista de todas as tags em formato dicionário
    """
    if gt is None:
        return []
    
    return list(gt['tags'].values())

def gt_listar_todos_times(gt: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Lista todos os times do sistema.
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
        
    Returns:
        List[Dict]: Lista de todos os times em formato dicionário
    """
    if gt is None:
        return []
    
    return list(gt['times'].values())

def gt_exportar_tarefas_csv(gt: Dict[str, Any], nome_arquivo: str) -> bool:
    """
    Exporta as tarefas para um arquivo CSV.
    
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
        # Prepara os dados para exportação
        dados_exportacao = []
        for tarefa in gt['tarefas'].values():
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

def gt_salvar_dados(gt: Dict[str, Any]) -> bool:
    """
    Função pública para salvar dados.
    
    Args:
        gt (Dict): Sistema GT em formato dicionário
        
    Returns:
        bool: True se salvou com sucesso, False caso contrário
    """
    return salvar_dados(gt)

