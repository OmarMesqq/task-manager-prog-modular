"""
Rotas da API para gerenciamento de tags

Este módulo contém todas as rotas relacionadas ao CRUD de tags.
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
        gt_registrar_tag, gt_listar_todas_tags
    )
    from modules.tag import (
        tag_criar, tag_destruir, tag_to_dict, tag_from_dict,
        tag_get_id, tag_get_nome, tag_get_cor,
        tag_set_nome, tag_set_cor, tag_listar_todas
    )
except ImportError as e:
    print(f"Erro ao importar módulos do Task Manager: {e}")

from src.utils import get_gt_system

tag_bp = Blueprint('tags', __name__)

def tag_to_dict(tag):
    """Converte uma tag para dicionário para JSON"""
    if not tag:
        return None
    
    return {
        'id': tag_get_id(tag),
        'nome': tag_get_nome(tag),
        'cor': tag_get_cor(tag)
    }

@tag_bp.route('/tags', methods=['GET'])
def listar_tags():
    """Lista todas as tags"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Usa a função do módulo tag diretamente
        tags = tag_listar_todas()
        tags_dict = [tag_to_dict(tag) for tag in tags]
        
        return jsonify({
            'success': True,
            'data': tags_dict,
            'count': len(tags_dict)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tag_bp.route('/tags', methods=['POST'])
def criar_tag():
    """Cria uma nova tag"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Validação dos campos obrigatórios
        if 'nome' not in data or 'cor' not in data:
            return jsonify({'error': 'Campos obrigatórios: nome, cor'}), 400
        
        # Cria a tag
        tag = tag_criar(data['nome'], data['cor'])
        if not tag:
            return jsonify({'error': 'Falha ao criar tag'}), 500
        
        # Registra no sistema GT
        resultado = gt_registrar_tag(gt, tag)
        if resultado != 0:
            tag_destruir(tag)
            return jsonify({'error': 'Falha ao registrar tag no sistema'}), 500
        
        return jsonify({
            'success': True,
            'data': tag_to_dict(tag),
            'message': 'Tag criada com sucesso'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tag_bp.route('/tags/<int:tag_id>', methods=['GET'])
def obter_tag(tag_id):
    """Obtém uma tag específica"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Usa a função do módulo tag diretamente
        tags = tag_listar_todas()
        tag = next((t for t in tags if tag_get_id(t) == tag_id), None)
        
        if not tag:
            return jsonify({'error': 'Tag não encontrada'}), 404
        
        return jsonify({
            'success': True,
            'data': tag_to_dict(tag)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tag_bp.route('/tags/<int:tag_id>', methods=['PUT'])
def atualizar_tag(tag_id):
    """Atualiza uma tag existente"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Busca a tag
        tags = tag_listar_todas()
        tag = next((t for t in tags if tag_get_id(t) == tag_id), None)
        
        if not tag:
            return jsonify({'error': 'Tag não encontrada'}), 404
        
        atualizado = False
        # Atualiza nome se fornecido
        if 'nome' in data:
            resultado_nome = tag_set_nome(tag, data['nome'])
            if resultado_nome != 0:
                return jsonify({'error': 'Falha ao atualizar nome'}), 500
            atualizado = True
        # Atualiza cor se fornecida
        if 'cor' in data:
            resultado = tag_set_cor(tag, data['cor'])
            if resultado != 0:
                return jsonify({'error': 'Falha ao atualizar cor'}), 500
            atualizado = True
        
        return jsonify({
            'success': True,
            'data': tag_to_dict(tag),
            'message': 'Tag atualizada com sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tag_bp.route('/tags/<int:tag_id>', methods=['DELETE'])
def deletar_tag(tag_id):
    """Deleta uma tag"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Busca a tag
        tags = tag_listar_todas()
        tag = next((t for t in tags if tag_get_id(t) == tag_id), None)
        
        if not tag:
            return jsonify({'error': 'Tag não encontrada'}), 404
        
        # Remove a tag (destrói a instância)
        tag_destruir(tag)
        
        return jsonify({
            'success': True,
            'message': 'Tag deletada com sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tag_bp.route('/tags/<int:tag_id>/tasks', methods=['GET'])
def listar_tarefas_tag(tag_id):
    """Lista todas as tarefas que usam uma tag específica"""
    try:
        gt = get_gt_system()
        if gt is None:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Busca a tag
        tags = tag_listar_todas()
        tag = next((t for t in tags if tag_get_id(t) == tag_id), None)
        
        if not tag:
            return jsonify({'error': 'Tag não encontrada'}), 404
        
        # Lista todas as tarefas e filtra por tag
        from modules.tarefa import tarefa_listar_todas
        todas_tarefas = tarefa_listar_todas()
        tarefas_tag = [
            tarefa for tarefa in todas_tarefas 
            if tag_id in tarefa['tags']
        ]
        
        # Converte para formato JSON
        tarefas_dict = []
        for tarefa in tarefas_tag:
            tarefas_dict.append({
                'id': tarefa['id'],
                'titulo': tarefa['titulo'],
                'descricao': tarefa['descricao'],
                'status': tarefa['status'].value if hasattr(tarefa['status'], 'value') else str(tarefa['status']),
                'prazo': str(tarefa['prazo']),
                'usuario_responsavel_id': tarefa['usuario_responsavel_id']
            })
        
        return jsonify({
            'success': True,
            'data': tarefas_dict,
            'count': len(tarefas_dict)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tag_bp.route('/tags/colors', methods=['GET'])
def cores_sugeridas():
    """Retorna uma lista de cores sugeridas para tags"""
    cores = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
        '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9',
        '#F8C471', '#82E0AA', '#F1948A', '#85C1E9', '#D7BDE2'
    ]
    
    return jsonify({
        'success': True,
        'data': cores
    })

