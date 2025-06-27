"""
Utilitários comuns do Task Manager

Este módulo contém funções utilitárias que são utilizadas
por múltiplos módulos do sistema.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

# Adiciona o diretório atual ao path se não estiver lá
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from config import DATE_FORMAT, DATA_DIR, criar_diretorios

def gerar_id_unico() -> int:
    """
    Gera um ID único baseado no timestamp atual.
    
    Returns:
        int: ID único baseado no timestamp
    """
    return int(datetime.now().timestamp() * 1000000)

def formatar_data(data) -> str:
    """
    Formata uma data para string no formato padrão.
    
    Args:
        data: Data a ser formatada (datetime ou string)
        
    Returns:
        str: Data formatada como string
    """
    if data is None:
        return None
    
    if isinstance(data, str):
        # Se já é string, tenta converter para datetime e formatar
        try:
            return parse_data(data).strftime(DATE_FORMAT)
        except:
            return data
    
    if isinstance(data, datetime):
        return data.strftime(DATE_FORMAT)
    
    # Se não for datetime nem string, converte para string
    return str(data)

def parse_data(data_str: str) -> datetime:
    """
    Converte string de data para objeto datetime.
    
    Args:
        data_str (str): String da data no formato padrão
        
    Returns:
        datetime: Objeto datetime correspondente
    """
    if not data_str:
        return None
    
    if isinstance(data_str, datetime):
        return data_str
    
    try:
        return datetime.strptime(data_str, DATE_FORMAT)
    except ValueError:
        # Tenta outros formatos comuns
        try:
            return datetime.fromisoformat(data_str.replace('Z', '+00:00'))
        except ValueError:
            try:
                return datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    return datetime.strptime(data_str, '%Y-%m-%d')
                except ValueError:
                    print(f"Erro ao parsear data: {data_str}")
                    return None

def salvar_json(dados: Dict[str, Any], nome_arquivo: str) -> bool:
    """
    Salva dados em arquivo JSON.
    
    Args:
        dados (Dict): Dados a serem salvos
        nome_arquivo (str): Nome do arquivo (sem caminho)
        
    Returns:
        bool: True se salvou com sucesso, False caso contrário
    """
    try:
        criar_diretorios()
        caminho_completo = os.path.join(DATA_DIR, nome_arquivo)
        with open(caminho_completo, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=2, ensure_ascii=False, default=str)
        return True
    except Exception as e:
        print(f"Erro ao salvar arquivo {nome_arquivo}: {e}")
        return False

def carregar_json(nome_arquivo: str) -> Optional[Dict[str, Any]]:
    """
    Carrega dados de arquivo JSON.
    
    Args:
        nome_arquivo (str): Nome do arquivo (sem caminho)
        
    Returns:
        Dict ou None: Dados carregados ou None se erro
    """
    try:
        caminho_completo = os.path.join(DATA_DIR, nome_arquivo)
        if not os.path.exists(caminho_completo):
            return {}
        
        with open(caminho_completo, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except Exception as e:
        print(f"Erro ao carregar arquivo {nome_arquivo}: {e}")
        return None

def validar_string_nao_vazia(valor: str, nome_campo: str) -> bool:
    """
    Valida se uma string não é nula nem vazia.
    
    Args:
        valor (str): Valor a ser validado
        nome_campo (str): Nome do campo para mensagens de erro
        
    Returns:
        bool: True se válida, False caso contrário
    """
    if valor is None:
        print(f"Erro: {nome_campo} não pode ser nulo")
        return False
    
    if not isinstance(valor, str):
        print(f"Erro: {nome_campo} deve ser uma string")
        return False
        
    if len(valor.strip()) == 0:
        print(f"Erro: {nome_campo} não pode ser vazio")
        return False
        
    return True

def log_operacao(modulo: str, operacao: str, detalhes: str = "") -> None:
    """
    Registra uma operação no log do sistema.
    
    Args:
        modulo (str): Nome do módulo que executou a operação
        operacao (str): Tipo de operação realizada
        detalhes (str): Detalhes adicionais da operação
    """
    timestamp = datetime.now().strftime(DATE_FORMAT)
    mensagem = f"[{timestamp}] {modulo}: {operacao}"
    if detalhes:
        mensagem += f" - {detalhes}"
    
    # Por enquanto apenas print, futuramente pode ser arquivo de log
    print(mensagem)

def exportar_para_csv(dados: List[Dict[str, Any]], nome_arquivo: str, cabecalhos: List[str]) -> bool:
    """
    Exporta dados para arquivo CSV.
    
    Args:
        dados (List[Dict]): Lista de dicionários com os dados
        nome_arquivo (str): Nome do arquivo CSV
        cabecalhos (List[str]): Lista com os nomes das colunas
        
    Returns:
        bool: True se exportou com sucesso, False caso contrário
    """
    try:
        import csv
        criar_diretorios()
        caminho_completo = os.path.join("exports", nome_arquivo)
        
        with open(caminho_completo, 'w', newline='', encoding='utf-8') as arquivo:
            writer = csv.DictWriter(arquivo, fieldnames=cabecalhos)
            writer.writeheader()
            writer.writerows(dados)
        
        return True
    except Exception as e:
        print(f"Erro ao exportar CSV {nome_arquivo}: {e}")
        return False

