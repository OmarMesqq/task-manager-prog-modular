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
        gt_registrar_time, gt_listar_todos_times, gt_listar_todos_usuarios, gt_salvar_dados
    )
    from modules.team import (
        time_criar, time_destruir, time_adicionar_usuario, time_remover_usuario,
        time_get_id, time_get_nome, time_qtd_membros, time_get_membros, time_set_nome
    )
    from modules.usuario import usuario_get_id
except ImportError as e:
    print(f"Erro ao importar módulos do Task Manager: {e}")

team_bp = Blueprint('teams', __name__)

def get_gt_system():
    """Obtém o sistema GT da configuração da aplicação"""
    return current_app.config.get('GT_SYSTEM')

def time_to_dict(time):
    """Converte um time para dicionário para JSON"""
    if not time:
        return None
    
    return {
        'id': time_get_id(time),
        'nome': time_get_nome(time),
        'qtd_membros': time_qtd_membros(time),
        'membros_ids': time_get_membros(time)
    }

@team_bp.route('/teams', methods=['GET'])
def listar_times():
    """Lista todos os times do sistema"""
    try:
        gt = get_gt_system()
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        times = gt_listar_todos_times(gt)
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
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Validação dos campos obrigatórios
        if 'nome' not in data:
            return jsonify({'error': 'Campo obrigatório: nome'}), 400
        
        # Verifica se já existe time com o mesmo nome
        times_existentes = gt_listar_todos_times(gt)
        for time_existente in times_existentes:
            if time_get_nome(time_existente).lower() == data['nome'].lower():
                return jsonify({'error': 'Já existe um time com este nome'}), 409
        
        # Cria o time
        time = time_criar(data['nome'])
        if not time:
            return jsonify({'error': 'Falha ao criar time'}), 500
        
        # Registra no sistema GT
        resultado = gt_registrar_time(gt, time)
        if resultado != 0:
            time_destruir(time)
            return jsonify({'error': 'Falha ao registrar time no sistema'}), 500
        
        # Salva os dados após criar o time
        gt_salvar_dados(gt)
        
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
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        times = gt_listar_todos_times(gt)
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
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Busca o time
        times = gt_listar_todos_times(gt)
        time = next((t for t in times if time_get_id(t) == team_id), None)
        
        if not time:
            return jsonify({'error': 'Time não encontrado'}), 404
        
        # Atualiza nome se fornecido
        if 'nome' in data:
            # Verifica se já existe outro time com o mesmo nome
            for time_existente in times:
                if (time_get_id(time_existente) != team_id and 
                    time_get_nome(time_existente).lower() == data['nome'].lower()):
                    return jsonify({'error': 'Já existe um time com este nome'}), 409
            
            resultado = time_set_nome(time, data['nome'])
            if resultado != 0:
                return jsonify({'error': 'Falha ao atualizar nome'}), 500
            
            # Salva os dados após atualizar
            gt_salvar_dados(gt)
        
        return jsonify({
            'success': True,
            'data': time_to_dict(time),
            'message': 'Time atualizado com sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@team_bp.route('/teams/<int:team_id>', methods=['DELETE'])
def deletar_time(team_id):
    """Remove um time (não implementado por segurança)"""
    return jsonify({
        'error': 'Remoção de times não permitida por questões de integridade dos dados'
    }), 405

@team_bp.route('/teams/<int:team_id>/members', methods=['GET'])
def listar_membros_time(team_id):
    """Lista todos os membros de um time"""
    try:
        gt = get_gt_system()
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Busca o time
        times = gt_listar_todos_times(gt)
        time = next((t for t in times if time_get_id(t) == team_id), None)
        
        if not time:
            return jsonify({'error': 'Time não encontrado'}), 404
        
        # Busca informações dos membros
        membros_ids = time_get_membros(time)
        usuarios = gt_listar_todos_usuarios(gt)
        
        membros = []
        for membro_id in membros_ids:
            usuario = next((u for u in usuarios if usuario_get_id(u) == membro_id), None)
            if usuario:
                from .user_routes import usuario_to_dict
                membros.append(usuario_to_dict(usuario))
        
        return jsonify({
            'success': True,
            'data': membros,
            'count': len(membros),
            'team': time_to_dict(time)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@team_bp.route('/teams/<int:team_id>/members/<int:user_id>', methods=['POST'])
def adicionar_membro_time(team_id, user_id):
    """Adiciona um usuário ao time"""
    try:
        gt = get_gt_system()
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Busca o time
        times = gt_listar_todos_times(gt)
        time = next((t for t in times if time_get_id(t) == team_id), None)
        
        if not time:
            return jsonify({'error': 'Time não encontrado'}), 404
        
        # Busca o usuário
        usuarios = gt_listar_todos_usuarios(gt)
        usuario = next((u for u in usuarios if usuario_get_id(u) == user_id), None)
        
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Adiciona o usuário ao time
        resultado = time_adicionar_usuario(time, usuario)
        if resultado != 0:
            return jsonify({'error': 'Falha ao adicionar usuário ao time'}), 500
        
        # Salva os dados após adicionar membro
        gt_salvar_dados(gt)
        
        return jsonify({
            'success': True,
            'message': 'Usuário adicionado ao time com sucesso',
            'team': time_to_dict(time)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@team_bp.route('/teams/<int:team_id>/members/<int:user_id>', methods=['DELETE'])
def remover_membro_time(team_id, user_id):
    """Remove um usuário do time"""
    try:
        gt = get_gt_system()
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Busca o time
        times = gt_listar_todos_times(gt)
        time = next((t for t in times if time_get_id(t) == team_id), None)
        
        if not time:
            return jsonify({'error': 'Time não encontrado'}), 404
        
        # Busca o usuário
        usuarios = gt_listar_todos_usuarios(gt)
        usuario = next((u for u in usuarios if usuario_get_id(u) == user_id), None)
        
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Remove o usuário do time
        resultado = time_remover_usuario(time, usuario)
        if resultado != 0:
            return jsonify({'error': 'Falha ao remover usuário do time'}), 500
        
        # Salva os dados após remover membro
        gt_salvar_dados(gt)
        
        return jsonify({
            'success': True,
            'message': 'Usuário removido do time com sucesso',
            'team': time_to_dict(time)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@team_bp.route('/teams/<int:team_id>/tasks', methods=['GET'])
def listar_tarefas_time(team_id):
    """Lista todas as tarefas de um time específico"""
    try:
        gt = get_gt_system()
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Busca o time
        times = gt_listar_todos_times(gt)
        time = next((t for t in times if time_get_id(t) == team_id), None)
        
        if not time:
            return jsonify({'error': 'Time não encontrado'}), 404
        
        # Busca tarefas do time
        from modules.gerenciamento_tarefas import gt_listar_tarefas_time
        
        qtd_out = [0]
        tarefas = gt_listar_tarefas_time(gt, time, qtd_out)
        
        if tarefas is None:
            return jsonify({'error': 'Falha ao listar tarefas do time'}), 500
        
        # Converte para dict
        from .task_routes import tarefa_to_dict
        tarefas_dict = [tarefa_to_dict(tarefa) for tarefa in tarefas]
        
        return jsonify({
            'success': True,
            'data': tarefas_dict,
            'count': len(tarefas_dict),
            'team': time_to_dict(time)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

