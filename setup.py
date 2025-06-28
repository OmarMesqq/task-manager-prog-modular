#!/usr/bin/env python3
"""
Script de inicialização do Task Manager

Este script configura o ambiente e inicializa o sistema de gerenciamento de tarefas.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_banner():
    """Exibe o banner do Task Manager"""
    print("=" * 60)
    print("🚀 TASK MANAGER - SISTEMA DE GERENCIAMENTO DE TAREFAS")
    print("=" * 60)
    print()

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 ou superior é necessário")
        print(f"   Versão atual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True

def create_directories():
    """Cria os diretórios necessários"""
    directories = [
        'data',
        'logs',
        'exports',
        'docs'
    ]
    
    print("📁 Criando diretórios necessários...")
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✓ {directory}/")
    
    return True

def create_data_files():
    """Cria os arquivos de dados iniciais"""
    data_files = {
        'data/usuarios.json': [],
        'data/tags.json': [],
        'data/times.json': [],
        'data/tarefas.json': []
    }
    
    print("📄 Criando arquivos de dados iniciais...")
    for file_path, initial_data in data_files.items():
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, indent=2, ensure_ascii=False)
            print(f"   ✓ {file_path}")
        else:
            print(f"   - {file_path} (já existe)")
    
    return True

def install_dependencies():
    """Instala as dependências do projeto"""
    if not os.path.exists('requirements.txt'):
        print("⚠️  Arquivo requirements.txt não encontrado")
        return True
    
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("   ✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError:
        print("   ❌ Erro ao instalar dependências")
        print("   💡 Execute manualmente: pip install -r requirements.txt")
        return False

def run_tests():
    """Executa os testes básicos do sistema"""
    print("🧪 Executando testes básicos...")
    
    try:
        # Tenta importar os módulos principais
        sys.path.insert(0, os.getcwd())
        
        from modules.usuario import usuario_criar, usuario_get_nome, usuario_destruir
        from modules.tag import tag_criar, tag_get_nome, tag_destruir
        from modules.team import time_criar, time_get_nome, time_destruir
        
        # Teste básico do módulo Usuario
        usuario = usuario_criar("Teste", "teste@email.com")
        if usuario and usuario_get_nome(usuario) == "Teste":
            print("   ✅ Módulo Usuario funcionando")
            usuario_destruir(usuario)
        else:
            print("   ❌ Módulo Usuario com problemas")
            return False
        
        # Teste básico do módulo Tag
        tag = tag_criar("Teste", "#FF0000")
        if tag and tag_get_nome(tag) == "Teste":
            print("   ✅ Módulo Tag funcionando")
            tag_destruir(tag)
        else:
            print("   ❌ Módulo Tag com problemas")
            return False
        
        # Teste básico do módulo Time
        time = time_criar("Teste")
        if time and time_get_nome(time) == "Teste":
            print("   ✅ Módulo Time funcionando")
            time_destruir(time)
        else:
            print("   ❌ Módulo Time com problemas")
            return False
        
        print("   🎉 Todos os módulos básicos funcionando!")
        return True
        
    except ImportError as e:
        print(f"   ❌ Erro ao importar módulos: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Erro nos testes: {e}")
        return False

def show_next_steps():
    """Mostra os próximos passos para o usuário"""
    print()
    print("🎯 PRÓXIMOS PASSOS:")
    print()
    print("1. 🌐 Para executar a interface web:")
    print("   cd web/task_manager_web")
    print("   source venv/bin/activate")
    print("   python src/main.py")
    print()
    print("2. 🧪 Para executar todos os testes:")
    print("   python tests/run_tests.py")
    print()
    print("3. 📖 Para ver a documentação:")
    print("   Abra o arquivo README.md")
    print()
    print("4. 🔗 Acesse a aplicação em:")
    print("   http://localhost:5001")
    print()

def main():
    """Função principal do script de inicialização"""
    print_banner()
    
    # Verificações e configurações
    steps = [
        ("Verificando versão do Python", check_python_version),
        ("Criando estrutura de diretórios", create_directories),
        ("Criando arquivos de dados", create_data_files),
        ("Instalando dependências", install_dependencies),
        ("Executando testes básicos", run_tests)
    ]
    
    success = True
    for step_name, step_function in steps:
        print(f"⚙️  {step_name}...")
        if not step_function():
            success = False
            break
        print()
    
    if success:
        print("🎉 INICIALIZAÇÃO CONCLUÍDA COM SUCESSO!")
        show_next_steps()
    else:
        print("❌ INICIALIZAÇÃO FALHOU")
        print("   Verifique os erros acima e tente novamente")
        sys.exit(1)

if __name__ == "__main__":
    main()

