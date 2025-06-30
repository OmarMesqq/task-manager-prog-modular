"""
Rotas da API para gerenciamento de usuários

Este módulo contém todas as rotas relacionadas ao CRUD de usuários.
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
        gt_registrar_usuario, gt_listar_todos_usuarios
    )
    from modules.usuario import (
        usuario_criar, usuario_destruir, usuario_to_dict, usuario_from_dict,
        usuario_get_id, usuario_get_nome, usuario_get_email,
        usuario_set_nome, usuario_set_email, usuario_listar_todos
    )
except ImportError as e:
    print(f"Erro ao importar módulos do Task Manager: {e}")

from src.utils import get_gt_system

user_bp = Blueprint('users', __name__)

def get_gt_system():
    """Obtém o sistema GT da configuração da aplicação"""
    return current_app.config.get('GT_SYSTEM')

def usuario_to_dict(usuario):
    """Converte um usuário para dicionário para JSON"""
    if not usuario:
        return None
    
    return {
        'id': usuario_get_id(usuario),
        'nome': usuario_get_nome(usuario),
        'email': usuario_get_email(usuario)
    }

@user_bp.route('/users', methods=['GET'])
def listar_usuarios():
    """Lista todos os usuários"""
    try:
        gt = get_gt_system()
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Usa a função do módulo usuario diretamente
        usuarios = usuario_listar_todos()
        usuarios_dict = [usuario_to_dict(usuario) for usuario in usuarios]
        
        return jsonify({
            'success': True,
            'data': usuarios_dict,
            'count': len(usuarios_dict)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users', methods=['POST'])
def criar_usuario():
    """Cria um novo usuário"""
    try:
        gt = get_gt_system()
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Validação dos campos obrigatórios
        if 'nome' not in data or 'email' not in data:
            return jsonify({'error': 'Campos obrigatórios: nome, email'}), 400
        
        # Cria o usuário
        usuario = usuario_criar(data['nome'], data['email'])
        if not usuario:
            return jsonify({'error': 'Falha ao criar usuário'}), 500
        
        # Registra no sistema GT
        resultado = gt_registrar_usuario(gt, usuario)
        if resultado != 0:
            usuario_destruir(usuario)
            return jsonify({'error': 'Falha ao registrar usuário no sistema'}), 500
        
        return jsonify({
            'success': True,
            'data': usuario_to_dict(usuario),
            'message': 'Usuário criado com sucesso'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def obter_usuario(user_id):
    """Obtém um usuário específico"""
    try:
        gt = get_gt_system()
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Usa a função do módulo usuario diretamente
        usuarios = usuario_listar_todos()
        usuario = next((u for u in usuarios if usuario_get_id(u) == user_id), None)
        
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        return jsonify({
            'success': True,
            'data': usuario_to_dict(usuario)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def atualizar_usuario(user_id):
    """Atualiza um usuário existente"""
    try:
        gt = get_gt_system()
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Busca o usuário
        usuarios = usuario_listar_todos()
        usuario = next((u for u in usuarios if usuario_get_id(u) == user_id), None)
        
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        atualizado = False
        # Atualiza nome se fornecido
        if 'nome' in data:
            resultado_nome = usuario_set_nome(usuario, data['nome'])
            if resultado_nome != 0:
                return jsonify({'error': 'Falha ao atualizar nome'}), 500
            atualizado = True
        # Atualiza email se fornecido
        if 'email' in data:
            resultado = usuario_set_email(usuario, data['email'])
            if resultado != 0:
                return jsonify({'error': 'Falha ao atualizar email'}), 500
            atualizado = True
        
        return jsonify({
            'success': True,
            'data': usuario_to_dict(usuario),
            'message': 'Usuário atualizado com sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def deletar_usuario(user_id):
    """Deleta um usuário"""
    try:
        gt = get_gt_system()
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Busca o usuário
        usuarios = usuario_listar_todos()
        usuario = next((u for u in usuarios if usuario_get_id(u) == user_id), None)
        
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Remove o usuário (destrói a instância)
        usuario_destruir(usuario)
        
        return jsonify({
            'success': True,
            'message': 'Usuário deletado com sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>/tasks', methods=['GET'])
def listar_tarefas_usuario(user_id):
    """Lista todas as tarefas de um usuário específico"""
    try:
        gt = get_gt_system()
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Busca o usuário
        usuarios = usuario_listar_todos()
        usuario = next((u for u in usuarios if usuario_get_id(u) == user_id), None)
        
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Lista todas as tarefas e filtra por usuário responsável
        from modules.tarefa import tarefa_listar_todas
        todas_tarefas = tarefa_listar_todas()
        tarefas_usuario = [
            tarefa for tarefa in todas_tarefas 
            if tarefa['usuario_responsavel_id'] == user_id
        ]
        
        # Converte para formato JSON
        tarefas_dict = []
        for tarefa in tarefas_usuario:
            tarefas_dict.append({
                'id': tarefa['id'],
                'titulo': tarefa['titulo'],
                'descricao': tarefa['descricao'],
                'status': tarefa['status'].value if hasattr(tarefa['status'], 'value') else str(tarefa['status']),
                'prazo': str(tarefa['prazo']),
                'tags': tarefa['tags']
            })
        
        return jsonify({
            'success': True,
            'data': tarefas_dict,
            'count': len(tarefas_dict)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

