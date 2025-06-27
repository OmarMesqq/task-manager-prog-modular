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
        gt_registrar_usuario, gt_listar_todos_usuarios, gt_salvar_dados
    )
    from modules.usuario import (
        usuario_criar, usuario_destruir, usuario_set_email,
        usuario_get_id, usuario_get_nome, usuario_get_email
    )
except ImportError as e:
    print(f"Erro ao importar módulos do Task Manager: {e}")

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
    """Lista todos os usuários do sistema"""
    try:
        gt = get_gt_system()
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        usuarios = gt_listar_todos_usuarios(gt)
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
        
        # Salva os dados após criar o usuário
        gt_salvar_dados(gt)
        
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
        
        usuarios = gt_listar_todos_usuarios(gt)
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
        usuarios = gt_listar_todos_usuarios(gt)
        usuario = next((u for u in usuarios if usuario_get_id(u) == user_id), None)
        
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Atualiza email se fornecido
        if 'email' in data:
            resultado = usuario_set_email(usuario, data['email'])
            if resultado != 0:
                return jsonify({'error': 'Falha ao atualizar email'}), 500
            
            # Salva os dados após atualizar
            gt_salvar_dados(gt)
        
        return jsonify({
            'success': True,
            'data': usuario_to_dict(usuario),
            'message': 'Usuário atualizado com sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def deletar_usuario(user_id):
    """Remove um usuário (não implementado por segurança)"""
    return jsonify({
        'error': 'Remoção de usuários não permitida por questões de integridade dos dados'
    }), 405

@user_bp.route('/users/<int:user_id>/tasks', methods=['GET'])
def listar_tarefas_usuario(user_id):
    """Lista todas as tarefas de um usuário específico"""
    try:
        gt = get_gt_system()
        if not gt:
            return jsonify({'error': 'Sistema não inicializado'}), 500
        
        # Verifica se o usuário existe
        usuarios = gt_listar_todos_usuarios(gt)
        usuario = next((u for u in usuarios if usuario_get_id(u) == user_id), None)
        
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Busca tarefas do usuário
        from modules.gerenciamento_tarefas import gt_listar_todas_tarefas
        from modules.tarefa import tarefa_get_usuario_responsavel_id
        
        todas_tarefas = gt_listar_todas_tarefas(gt)
        tarefas_usuario = [t for t in todas_tarefas if tarefa_get_usuario_responsavel_id(t) == user_id]
        
        # Converte para dict
        from .task_routes import tarefa_to_dict
        tarefas_dict = [tarefa_to_dict(tarefa) for tarefa in tarefas_usuario]
        
        return jsonify({
            'success': True,
            'data': tarefas_dict,
            'count': len(tarefas_dict),
            'user': usuario_to_dict(usuario)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

