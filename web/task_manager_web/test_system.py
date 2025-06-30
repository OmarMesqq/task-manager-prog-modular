#!/usr/bin/env python3
"""
Script de teste para verificar se o sistema GT está funcionando
"""

import sys
import os

# Adiciona o diretório raiz ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
task_manager_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, task_manager_root)

# Adiciona o diretório modules ao path
modules_dir = os.path.join(task_manager_root, 'modules')
sys.path.insert(0, modules_dir)

def test_system():
    """Testa se o sistema GT está funcionando"""
    try:
        print("🔍 Testando sistema GT...")
        
        # Testa importação dos módulos
        from modules.gerenciamento_tarefas import gt_inicializar, gt_finalizar
        from modules.team import time_listar_todos
        from modules.usuario import usuario_listar_todos
        from modules.tag import tag_listar_todas
        from modules.tarefa import tarefa_listar_todas
        
        print("✅ Módulos importados com sucesso")
        
        # Testa inicialização
        gt = gt_inicializar()
        if gt is None:
            print("❌ Falha ao inicializar sistema GT")
            return False
        
        print("✅ Sistema GT inicializado")
        
        # Testa listagem de times
        times = time_listar_todos()
        print(f"✅ Times encontrados: {len(times)}")
        
        # Testa listagem de usuários
        usuarios = usuario_listar_todos()
        print(f"✅ Usuários encontrados: {len(usuarios)}")
        
        # Testa listagem de tags
        tags = tag_listar_todas()
        print(f"✅ Tags encontradas: {len(tags)}")
        
        # Testa listagem de tarefas
        tarefas = tarefa_listar_todas()
        print(f"✅ Tarefas encontradas: {len(tarefas)}")
        
        # Finaliza o sistema
        gt_finalizar(gt)
        print("✅ Sistema GT finalizado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_system()
    sys.exit(0 if success else 1) 