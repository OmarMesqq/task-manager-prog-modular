"""
Rotas da API para gerenciamento de times

Este módulo contém todas as rotas relacionadas ao CRUD de times.
"""

from flask import Blueprint, request, jsonify, current_app
import sys
import os

# Adiciona o path do Task Manager
task_manager_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))
sys.path.insert(0, task_manager_path)

# Adiciona o diretório modules ao path
modules_path = os.path.join(task_manager_path, 'modules')
sys.path.insert(0, modules_path)

try:
    from modules.gerenciamento_tarefas import (
        gt_registrar_time, gt_listar_todos_times
    )
    from modules.team import (
        time_criar, time_destruir, time_to_dict, time_from_dict,
        time_get_id, time_get_nome, time_get_membros, time_qtd_membros,
        time_set_nome, time_adicionar_usuario, time_remover_usuario, time_listar_todos
    )
    from modules.usuario import usuario_listar_todos, usuario_get_id
except ImportError as e:
    print(f"Erro ao importar módulos do Task Manager: {e}")

from src.utils import get_gt_system

team_bp = Blueprint('teams', __name__)

def time_to_dict(time):
    """Converte um time para dicionário para JSON"""
    if not time:
        return None
    
    return {
        'id': time_get_id(time),
        'nome': time_get_nome(time),
        'membros': time_get_membros(time),
        'qtd_membros': time_qtd_membros(time)
    }

@team_bp.route('/teams', methods=['GET'])
def listar_times():
    """Lista todos os times"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Usa a função do módulo team diretamente
        times = time_listar_todos()
        times_dict = [time_to_dict(time) for time in times]
        
        return jsonify({
            'success': True,
            'data': times_dict,
            'count': len(times_dict)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@team_bp.route('/teams', methods=['POST'])
def criar_time():
    """Cria um novo time"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Validação dos campos obrigatórios
        if 'nome' not in data:
            return jsonify({'error': 'Campo obrigatório: nome'}), 400
        
        # Cria o time
        time = time_criar(data['nome'])
        if not time:
            return jsonify({'error': 'Falha ao criar time'}), 500
        
        # Registra no sistema GT
        resultado = gt_registrar_time(gt, time)
        if resultado != 0:
            time_destruir(time)
            return jsonify({'error': 'Falha ao registrar time no sistema'}), 500
        
        return jsonify({
            'success': True,
            'data': time_to_dict(time),
            'message': 'Time criado com sucesso'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@team_bp.route('/teams/<int:team_id>', methods=['GET'])
def obter_time(team_id):
    """Obtém um time específico"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Usa a função do módulo team diretamente
        times = time_listar_todos()
        time = next((t for t in times if time_get_id(t) == team_id), None)
        
        if not time:
            return jsonify({'error': 'Time não encontrado'}), 404
        
        return jsonify({
            'success': True,
            'data': time_to_dict(time)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@team_bp.route('/teams/<int:team_id>', methods=['PUT'])
def atualizar_time(team_id):
    """Atualiza um time existente"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Busca o time
        times = time_listar_todos()
        time = next((t for t in times if time_get_id(t) == team_id), None)
        
        if not time:
            return jsonify({'error': 'Time não encontrado'}), 404
        
        # Atualiza nome se fornecido
        if 'nome' in data:
            resultado = time_set_nome(time, data['nome'])
            if resultado != 0:
                return jsonify({'error': 'Falha ao atualizar nome'}), 500
        
        return jsonify({
            'success': True,
            'data': time_to_dict(time),
            'message': 'Time atualizado com sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@team_bp.route('/teams/<int:team_id>', methods=['DELETE'])
def deletar_time(team_id):
    """Deleta um time"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Busca o time
        times = time_listar_todos()
        time = next((t for t in times if time_get_id(t) == team_id), None)
        
        if not time:
            return jsonify({'error': 'Time não encontrado'}), 404
        
        # Remove o time (destrói a instância)
        time_destruir(time)
        
        return jsonify({
            'success': True,
            'message': 'Time deletado com sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@team_bp.route('/teams/<int:team_id>/users', methods=['POST'])
def adicionar_usuario_time(team_id):
    """Adiciona um usuário a um time"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        if 'user_id' not in data:
            return jsonify({'error': 'Campo obrigatório: user_id'}), 400
        
        # Busca o time
        times = time_listar_todos()
        time = next((t for t in times if time_get_id(t) == team_id), None)
        
        if not time:
            return jsonify({'error': 'Time não encontrado'}), 404
        
        # Busca o usuário
        usuarios = usuario_listar_todos()
        usuario = next((u for u in usuarios if usuario_get_id(u) == data['user_id']), None)
        
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Adiciona o usuário ao time
        resultado = time_adicionar_usuario(time, usuario)
        if resultado != 0:
            return jsonify({'error': 'Falha ao adicionar usuário ao time'}), 500
        
        return jsonify({
            'success': True,
            'data': time_to_dict(time),
            'message': 'Usuário adicionado ao time com sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@team_bp.route('/teams/<int:team_id>/users/<int:user_id>', methods=['DELETE'])
def remover_usuario_time(team_id, user_id):
    """Remove um usuário de um time"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Busca o time
        times = time_listar_todos()
        time = next((t for t in times if time_get_id(t) == team_id), None)
        
        if not time:
            return jsonify({'error': 'Time não encontrado'}), 404
        
        # Busca o usuário
        usuarios = usuario_listar_todos()
        usuario = next((u for u in usuarios if usuario_get_id(u) == user_id), None)
        
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Remove o usuário do time
        resultado = time_remover_usuario(time, usuario)
        if resultado != 0:
            return jsonify({'error': 'Falha ao remover usuário do time'}), 500
        
        return jsonify({
            'success': True,
            'data': time_to_dict(time),
            'message': 'Usuário removido do time com sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@team_bp.route('/teams/<int:team_id>/users', methods=['GET'])
def listar_usuarios_time(team_id):
    """Lista todos os usuários de um time"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Busca o time
        times = time_listar_todos()
        time = next((t for t in times if time_get_id(t) == team_id), None)
        
        if not time:
            return jsonify({'error': 'Time não encontrado'}), 404
        
        # Obtém os membros do time
        membros_ids = time_get_membros(time)
        
        # Busca os usuários correspondentes
        usuarios = usuario_listar_todos()
        usuarios_time = [
            usuario for usuario in usuarios 
            if usuario_get_id(usuario) in membros_ids
        ]
        
        # Converte para formato JSON
        from .user_routes import usuario_to_dict
        usuarios_dict = [usuario_to_dict(usuario) for usuario in usuarios_time]
        
        return jsonify({
            'success': True,
            'data': usuarios_dict,
            'count': len(usuarios_dict)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

