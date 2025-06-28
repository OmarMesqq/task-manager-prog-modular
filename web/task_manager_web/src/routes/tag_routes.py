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
        gt_registrar_tag, gt_listar_todas_tags, gt_salvar_dados
    )
    from modules.tag import (
        tag_criar, tag_destruir, tag_set_nome, tag_set_cor,
        tag_get_id, tag_get_nome, tag_get_cor
    )
except ImportError as e:
    print(f"Erro ao importar módulos do Task Manager: {e}")

tag_bp = Blueprint('tags', __name__)

def get_gt_system():
    """Obtém o sistema GT da configuração da aplicação"""
    return current_app.config.get('GT_SYSTEM')

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
    """Lista todas as tags do sistema"""
    try:
        gt = get_gt_system()
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        tags = gt_listar_todas_tags(gt)
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
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Validação dos campos obrigatórios
        if 'nome' not in data or 'cor' not in data:
            return jsonify({'error': 'Campos obrigatórios: nome, cor'}), 400
        
        # Verifica se já existe tag com o mesmo nome
        tags_existentes = gt_listar_todas_tags(gt)
        for tag_existente in tags_existentes:
            if tag_get_nome(tag_existente).lower() == data['nome'].lower():
                return jsonify({'error': 'Já existe uma tag com este nome'}), 409
        
        # Cria a tag
        tag = tag_criar(data['nome'], data['cor'])
        if not tag:
            return jsonify({'error': 'Falha ao criar tag'}), 500
        
        # Registra no sistema GT
        resultado = gt_registrar_tag(gt, tag)
        if resultado != 0:
            tag_destruir(tag)
            return jsonify({'error': 'Falha ao registrar tag no sistema'}), 500
        
        # Salva os dados após criar a tag
        gt_salvar_dados(gt)
        
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
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        tags = gt_listar_todas_tags(gt)
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
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Busca a tag
        tags = gt_listar_todas_tags(gt)
        tag = next((t for t in tags if tag_get_id(t) == tag_id), None)
        
        if not tag:
            return jsonify({'error': 'Tag não encontrada'}), 404
        
        # Atualiza nome se fornecido
        if 'nome' in data:
            # Verifica se já existe outra tag com o mesmo nome
            for tag_existente in tags:
                if (tag_get_id(tag_existente) != tag_id and 
                    tag_get_nome(tag_existente).lower() == data['nome'].lower()):
                    return jsonify({'error': 'Já existe uma tag com este nome'}), 409
            
            resultado = tag_set_nome(tag, data['nome'])
            if resultado != 0:
                return jsonify({'error': 'Falha ao atualizar nome'}), 500
        
        # Atualiza cor se fornecida
        if 'cor' in data:
            resultado = tag_set_cor(tag, data['cor'])
            if resultado != 0:
                return jsonify({'error': 'Falha ao atualizar cor'}), 500
        
        # Salva os dados após atualizar
        if 'nome' in data or 'cor' in data:
            gt_salvar_dados(gt)
        
        return jsonify({
            'success': True,
            'data': tag_to_dict(tag),
            'message': 'Tag atualizada com sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tag_bp.route('/tags/<int:tag_id>', methods=['DELETE'])
def deletar_tag(tag_id):
    """Remove uma tag (não implementado por segurança)"""
    return jsonify({
        'error': 'Remoção de tags não permitida por questões de integridade dos dados'
    }), 405

@tag_bp.route('/tags/<int:tag_id>/tasks', methods=['GET'])
def listar_tarefas_tag(tag_id):
    """Lista todas as tarefas que possuem uma tag específica"""
    try:
        gt = get_gt_system()
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Verifica se a tag existe
        tags = gt_listar_todas_tags(gt)
        tag = next((t for t in tags if tag_get_id(t) == tag_id), None)
        
        if not tag:
            return jsonify({'error': 'Tag não encontrada'}), 404
        
        # Busca tarefas que possuem esta tag
        from modules.gerenciamento_tarefas import gt_listar_todas_tarefas
        from modules.tarefa import tarefa_get_tags_ids
        
        todas_tarefas = gt_listar_todas_tarefas(gt)
        tarefas_tag = [t for t in todas_tarefas if tag_id in tarefa_get_tags_ids(t)]
        
        # Converte para dict
        from .task_routes import tarefa_to_dict
        tarefas_dict = [tarefa_to_dict(tarefa) for tarefa in tarefas_tag]
        
        return jsonify({
            'success': True,
            'data': tarefas_dict,
            'count': len(tarefas_dict),
            'tag': tag_to_dict(tag)
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

