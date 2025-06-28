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
        gt_exportar_tarefas_csv, gt_salvar_dados
    )
    from modules.tarefa import (
        tarefa_get_id, tarefa_get_titulo, tarefa_get_descricao,
        tarefa_get_status, tarefa_get_usuario_responsavel_id,
        tarefa_get_prazo, tarefa_get_tags_ids, tarefa_set_status, StatusTarefa
    )
    from modules.usuario import usuario_get_id, usuario_get_nome
    from modules.tag import tag_get_id, tag_get_nome
    from modules.team import time_get_id, time_get_nome
except ImportError as e:
    print(f"Erro ao importar módulos do Task Manager: {e}")
    # Fallback imports ou tratamento de erro

task_bp = Blueprint('tasks', __name__)

def get_gt_system():
    """Obtém o sistema GT da configuração da aplicação"""
    return current_app.config.get('GT_SYSTEM')

def tarefa_to_dict(tarefa):
    """Converte uma tarefa para dicionário para JSON"""
    if not tarefa:
        return None
    
    try:
        prazo = tarefa_get_prazo(tarefa)
        if prazo:
            if isinstance(prazo, str):
                prazo_str = prazo
            else:
                prazo_str = prazo.isoformat()
        else:
            prazo_str = None
        
        status = tarefa_get_status(tarefa)
        status_value = status.value if status else None
        
        return {
            'id': tarefa_get_id(tarefa),
            'titulo': tarefa_get_titulo(tarefa),
            'descricao': tarefa_get_descricao(tarefa),
            'status': status_value,
            'usuario_responsavel_id': tarefa_get_usuario_responsavel_id(tarefa),
            'prazo': prazo_str,
            'tags_ids': tarefa_get_tags_ids(tarefa)
        }
    except Exception as e:
        print(f"Erro ao converter tarefa para dict: {e}")
        return None

@task_bp.route('/tasks', methods=['GET'])
def listar_tarefas():
    """Lista todas as tarefas do sistema"""
    try:
        gt = get_gt_system()
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        tarefas = gt_listar_todas_tarefas(gt)
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
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Validação dos campos obrigatórios
        required_fields = ['titulo', 'descricao', 'usuario_id', 'time_id', 'prazo']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Busca entidades necessárias
        usuarios = gt_listar_todos_usuarios(gt)
        times = gt_listar_todos_times(gt)
        
        usuario = next((u for u in usuarios if usuario_get_id(u) == data['usuario_id']), None)
        time = next((t for t in times if time_get_id(t) == data['time_id']), None)
        
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        if not time:
            return jsonify({'error': 'Time não encontrado'}), 404
        
        # Processa tags se fornecidas
        tags = []
        if 'tags_ids' in data and data['tags_ids']:
            todas_tags = gt_listar_todas_tags(gt)
            for tag_id in data['tags_ids']:
                tag = next((t for t in todas_tags if tag_get_id(t) == tag_id), None)
                if tag:
                    tags.append(tag)
        
        # Converte prazo
        try:
            prazo = datetime.fromisoformat(data['prazo'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Formato de prazo inválido (use ISO 8601)'}), 400
        
        # Cria a tarefa
        tarefa = gt_criar_tarefa(
            gt, time, data['titulo'], data['descricao'],
            usuario, tags, len(tags), prazo
        )
        
        if not tarefa:
            return jsonify({'error': 'Falha ao criar tarefa'}), 500
        
        # Salva os dados após criar a tarefa
        gt_salvar_dados(gt)
        
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
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        tarefas = gt_listar_todas_tarefas(gt)
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
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        print(f"Atualizando tarefa {task_id} com dados: {data}")
        
        # Busca a tarefa
        tarefas = gt_listar_todas_tarefas(gt)
        tarefa = next((t for t in tarefas if tarefa_get_id(t) == task_id), None)
        
        if not tarefa:
            return jsonify({'error': 'Tarefa não encontrada'}), 404
        
        # Atualiza status se fornecido
        if 'status' in data:
            print(f"Status atual: {tarefa_get_status(tarefa)}")
            print(f"Novo status solicitado: {data['status']}")
            
            # Mapeia string para enum
            status_mapping = {
                'aberta': StatusTarefa.TAREFA_ABERTA,
                'em_progresso': StatusTarefa.TAREFA_EM_PROGRESSO,
                'concluida': StatusTarefa.TAREFA_CONCLUIDA,
                'cancelada': StatusTarefa.TAREFA_CANCELADA
            }
            
            novo_status = status_mapping.get(data['status'])
            if novo_status:
                print(f"Status enum criado: {novo_status}")
                resultado = tarefa_set_status(tarefa, novo_status)
                print(f"Resultado da atualização: {resultado}")
                if resultado == 0:
                    print(f"Status atualizado com sucesso para: {novo_status}")
                    # Salva os dados após atualizar
                    gt_salvar_dados(gt)
                else:
                    print(f"Erro ao atualizar status: {resultado}")
            else:
                print(f"Status inválido: {data['status']}")
        
        return jsonify({
            'success': True,
            'data': tarefa_to_dict(tarefa),
            'message': 'Tarefa atualizada com sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def deletar_tarefa(task_id):
    """Remove uma tarefa do sistema"""
    try:
        gt = get_gt_system()
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Busca a tarefa
        tarefas = gt_listar_todas_tarefas(gt)
        tarefa = next((t for t in tarefas if tarefa_get_id(t) == task_id), None)
        
        if not tarefa:
            return jsonify({'error': 'Tarefa não encontrada'}), 404
        
        # Remove a tarefa
        resultado = gt_remover_tarefa(gt, tarefa)
        if resultado != 0:
            return jsonify({'error': 'Falha ao remover tarefa'}), 500
        
        # Salva os dados após remover
        gt_salvar_dados(gt)
        
        return jsonify({
            'success': True,
            'message': 'Tarefa removida com sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/tasks/export', methods=['GET'])
def exportar_tarefas():
    """Exporta todas as tarefas para CSV"""
    try:
        gt = get_gt_system()
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        nome_arquivo = f"tarefas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        caminho_arquivo = os.path.join('exports', nome_arquivo)
        
        if gt_exportar_tarefas_csv(gt, caminho_arquivo):
            return jsonify({
                'success': True,
                'message': 'Tarefas exportadas com sucesso',
                'file': nome_arquivo
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
        if not gt:
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

