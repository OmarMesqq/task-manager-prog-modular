"""
Rotas da API para gerenciamento de tarefas

Este módulo contém todas as rotas relacionadas ao CRUD de tarefas
e operações do sistema de gerenciamento.
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
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
        gt_criar_tarefa, gt_remover_tarefa, gt_listar_todas_tarefas,
        gt_listar_todos_usuarios, gt_listar_todas_tags, gt_listar_todos_times,
        gt_exportar_tarefas_csv
    )
    from modules.tarefa import (
        tarefa_criar, tarefa_destruir, tarefa_to_dict, tarefa_from_dict,
        tarefa_get_id, tarefa_get_titulo, tarefa_get_descricao, tarefa_get_status,
        tarefa_get_usuario_responsavel_id, tarefa_get_prazo, tarefa_get_tags_ids,
        tarefa_set_status, tarefa_add_tag, tarefa_remover_tag, tarefa_listar_todas,
        tarefa_set_titulo, tarefa_set_descricao, tarefa_set_prazo, StatusTarefa
    )
    from modules.usuario import usuario_listar_todos, usuario_get_id
    from modules.tag import tag_listar_todas, tag_get_id
    from modules.team import time_listar_todos, time_get_id
except ImportError as e:
    print(f"Erro ao importar módulos do Task Manager: {e}")

from src.utils import get_gt_system

task_bp = Blueprint('tasks', __name__)

def tarefa_to_dict(tarefa):
    """Converte uma tarefa para dicionário para JSON"""
    if not tarefa:
        return None
    
    return {
        'id': tarefa_get_id(tarefa),
        'titulo': tarefa_get_titulo(tarefa),
        'descricao': tarefa_get_descricao(tarefa),
        'status': tarefa_get_status(tarefa).value if tarefa_get_status(tarefa) else None,
        'usuario_responsavel_id': tarefa_get_usuario_responsavel_id(tarefa),
        'prazo': str(tarefa_get_prazo(tarefa)) if tarefa_get_prazo(tarefa) else None,
        'tags': tarefa_get_tags_ids(tarefa)
    }

@task_bp.route('/tasks', methods=['GET'])
def listar_tarefas():
    """Lista todas as tarefas"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Usa a função do módulo tarefa diretamente
        tarefas = tarefa_listar_todas()
        tarefas_dict = [tarefa_to_dict(tarefa) for tarefa in tarefas]
        
        return jsonify({
            'success': True,
            'data': tarefas_dict,
            'count': len(tarefas_dict)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/tasks', methods=['POST'])
def criar_tarefa():
    """Cria uma nova tarefa"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Validação dos campos obrigatórios
        required_fields = ['titulo', 'descricao', 'usuario_responsavel_id', 'prazo']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Busca o usuário responsável
        usuarios = usuario_listar_todos()
        usuario = next((u for u in usuarios if usuario_get_id(u) == data['usuario_responsavel_id']), None)
        
        if not usuario:
            return jsonify({'error': 'Usuário responsável não encontrado'}), 404
        
        # Converte o prazo
        try:
            prazo = datetime.fromisoformat(data['prazo'].replace('Z', '+00:00'))
        except:
            return jsonify({'error': 'Formato de prazo inválido. Use ISO 8601'}), 400
        
        # Busca o time (opcional)
        time = None
        if 'time_id' in data:
            times = time_listar_todos()
            time = next((t for t in times if time_get_id(t) == data['time_id']), None)
            if not time:
                return jsonify({'error': 'Time não encontrado'}), 404
        
        # Busca as tags (opcional)
        tags = []
        if 'tags' in data and isinstance(data['tags'], list):
            todas_tags = tag_listar_todas()
            for tag_id in data['tags']:
                tag = next((t for t in todas_tags if tag_get_id(t) == tag_id), None)
                if tag:
                    tags.append(tag)
        
        # Cria a tarefa
        tarefa = gt_criar_tarefa(gt, time, data['titulo'], data['descricao'], 
                                usuario, tags, len(tags), prazo)
        
        if not tarefa:
            return jsonify({'error': 'Falha ao criar tarefa'}), 500
        
        return jsonify({
            'success': True,
            'data': tarefa_to_dict(tarefa),
            'message': 'Tarefa criada com sucesso'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def obter_tarefa(task_id):
    """Obtém uma tarefa específica"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Usa a função do módulo tarefa diretamente
        tarefas = tarefa_listar_todas()
        tarefa = next((t for t in tarefas if tarefa_get_id(t) == task_id), None)
        
        if not tarefa:
            return jsonify({'error': 'Tarefa não encontrada'}), 404
        
        return jsonify({
            'success': True,
            'data': tarefa_to_dict(tarefa)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def atualizar_tarefa(task_id):
    """Atualiza uma tarefa existente"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Busca a tarefa
        tarefas = tarefa_listar_todas()
        tarefa = next((t for t in tarefas if tarefa_get_id(t) == task_id), None)
        
        if not tarefa:
            return jsonify({'error': 'Tarefa não encontrada'}), 404
        
        # Atualiza os campos fornecidos
        if 'titulo' in data:
            resultado = tarefa_set_titulo(tarefa, data['titulo'])
            if resultado != 0:
                return jsonify({'error': 'Falha ao atualizar título'}), 500
        
        if 'descricao' in data:
            resultado = tarefa_set_descricao(tarefa, data['descricao'])
            if resultado != 0:
                return jsonify({'error': 'Falha ao atualizar descrição'}), 500
        
        if 'prazo' in data:
            try:
                prazo = datetime.fromisoformat(data['prazo'].replace('Z', '+00:00'))
                resultado = tarefa_set_prazo(tarefa, prazo)
                if resultado != 0:
                    return jsonify({'error': 'Falha ao atualizar prazo'}), 500
            except:
                return jsonify({'error': 'Formato de prazo inválido. Use ISO 8601'}), 400
        
        if 'status' in data:
            try:
                status = StatusTarefa(data['status'])
                resultado = tarefa_set_status(tarefa, status)
                if resultado != 0:
                    return jsonify({'error': 'Falha ao atualizar status'}), 500
            except:
                return jsonify({'error': 'Status inválido'}), 400
        
        return jsonify({
            'success': True,
            'data': tarefa_to_dict(tarefa),
            'message': 'Tarefa atualizada com sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def deletar_tarefa(task_id):
    """Deleta uma tarefa"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Busca a tarefa
        tarefas = tarefa_listar_todas()
        tarefa = next((t for t in tarefas if tarefa_get_id(t) == task_id), None)
        
        if not tarefa:
            return jsonify({'error': 'Tarefa não encontrada'}), 404
        
        # Remove a tarefa
        resultado = gt_remover_tarefa(gt, tarefa)
        if resultado != 0:
            return jsonify({'error': 'Falha ao remover tarefa'}), 500
        
        return jsonify({
            'success': True,
            'message': 'Tarefa deletada com sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/tasks/<int:task_id>/tags', methods=['POST'])
def adicionar_tag_tarefa(task_id):
    """Adiciona uma tag a uma tarefa"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        if 'tag_id' not in data:
            return jsonify({'error': 'Campo obrigatório: tag_id'}), 400
        
        # Busca a tarefa
        tarefas = tarefa_listar_todas()
        tarefa = next((t for t in tarefas if tarefa_get_id(t) == task_id), None)
        
        if not tarefa:
            return jsonify({'error': 'Tarefa não encontrada'}), 404
        
        # Busca a tag
        tags = tag_listar_todas()
        tag = next((t for t in tags if tag_get_id(t) == data['tag_id']), None)
        
        if not tag:
            return jsonify({'error': 'Tag não encontrada'}), 404
        
        # Adiciona a tag à tarefa
        resultado = tarefa_add_tag(tarefa, tag)
        if resultado != 0:
            return jsonify({'error': 'Falha ao adicionar tag à tarefa'}), 500
        
        return jsonify({
            'success': True,
            'data': tarefa_to_dict(tarefa),
            'message': 'Tag adicionada à tarefa com sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/tasks/<int:task_id>/tags/<int:tag_id>', methods=['DELETE'])
def remover_tag_tarefa(task_id, tag_id):
    """Remove uma tag de uma tarefa"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Busca a tarefa
        tarefas = tarefa_listar_todas()
        tarefa = next((t for t in tarefas if tarefa_get_id(t) == task_id), None)
        
        if not tarefa:
            return jsonify({'error': 'Tarefa não encontrada'}), 404
        
        # Busca a tag
        tags = tag_listar_todas()
        tag = next((t for t in tags if tag_get_id(t) == tag_id), None)
        
        if not tag:
            return jsonify({'error': 'Tag não encontrada'}), 404
        
        # Remove a tag da tarefa
        resultado = tarefa_remover_tag(tarefa, tag)
        if resultado != 0:
            return jsonify({'error': 'Falha ao remover tag da tarefa'}), 500
        
        return jsonify({
            'success': True,
            'data': tarefa_to_dict(tarefa),
            'message': 'Tag removida da tarefa com sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/tasks/status/<status>', methods=['GET'])
def listar_tarefas_por_status(status):
    """Lista todas as tarefas com um status específico"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Valida o status
        try:
            status_enum = StatusTarefa(status)
        except:
            return jsonify({'error': 'Status inválido'}), 400
        
        # Lista todas as tarefas e filtra por status
        tarefas = tarefa_listar_todas()
        tarefas_status = [
            tarefa for tarefa in tarefas 
            if tarefa_get_status(tarefa) == status_enum
        ]
        
        tarefas_dict = [tarefa_to_dict(tarefa) for tarefa in tarefas_status]
        
        return jsonify({
            'success': True,
            'data': tarefas_dict,
            'count': len(tarefas_dict)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/tasks/export', methods=['POST'])
def exportar_tarefas():
    """Exporta tarefas para CSV"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        nome_arquivo = data.get('nome_arquivo', f'tarefas_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
        
        # Exporta para CSV
        if gt_exportar_tarefas_csv(gt, nome_arquivo):
            return jsonify({
                'success': True,
                'message': 'Tarefas exportadas com sucesso',
                'arquivo': nome_arquivo
            })
        else:
            return jsonify({'error': 'Falha ao exportar tarefas'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/tasks/stats', methods=['GET'])
def estatisticas_tarefas():
    """Retorna estatísticas das tarefas"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        tarefas = gt_listar_todas_tarefas(gt)
        
        # Conta por status
        stats = {
            'total': len(tarefas),
            'aberta': 0,
            'em_progresso': 0,
            'concluida': 0,
            'cancelada': 0
        }
        
        for tarefa in tarefas:
            status = tarefa_get_status(tarefa)
            if status:
                status_value = status.value
                if status_value in stats:
                    stats[status_value] += 1
        
        return jsonify({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

