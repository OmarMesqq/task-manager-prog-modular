#!/usr/bin/env python3
"""
Script para executar todos os testes do Task Manager

Este script executa todos os testes unitários dos módulos do sistema
e gera um relatório completo dos resultados.
"""

import sys
import os
import importlib
import shutil
import json
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa configurações
from config import DATA_DIR, BACKUP_DIR, USUARIOS_FILE, TAGS_FILE, TIMES_FILE, TAREFAS_FILE

def fazer_backup_dados():
    """
    Faz backup dos dados originais antes dos testes.
    
    Returns:
        str: Timestamp do backup criado
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"backup_teste_{timestamp}")
    
    try:
        # Cria diretório de backup
        os.makedirs(backup_path, exist_ok=True)
        
        # Lista de arquivos para fazer backup
        arquivos_dados = [
            (USUARIOS_FILE, "usuarios.json"),
            (TAGS_FILE, "tags.json"),
            (TIMES_FILE, "times.json"),
            (TAREFAS_FILE, "tarefas.json")
        ]
        
        for arquivo_origem, nome_backup in arquivos_dados:
            caminho_origem = os.path.join(DATA_DIR, arquivo_origem)
            caminho_backup = os.path.join(backup_path, nome_backup)
            
            if os.path.exists(caminho_origem):
                shutil.copy2(caminho_origem, caminho_backup)
                print(f"✅ Backup criado: {nome_backup}")
            else:
                # Cria arquivo vazio se não existir
                with open(caminho_backup, 'w') as f:
                    json.dump({}, f)
                print(f"✅ Arquivo vazio criado: {nome_backup}")
        
        print(f"📦 Backup completo criado em: {backup_path}")
        return timestamp
        
    except Exception as e:
        print(f"❌ Erro ao criar backup: {e}")
        return None

def restaurar_dados(timestamp):
    """
    Restaura os dados originais após os testes.
    
    Args:
        timestamp (str): Timestamp do backup a ser restaurado
    """
    if not timestamp:
        print("⚠️  Nenhum backup para restaurar")
        return
    
    backup_path = os.path.join(BACKUP_DIR, f"backup_teste_{timestamp}")
    
    try:
        if not os.path.exists(backup_path):
            print(f"❌ Diretório de backup não encontrado: {backup_path}")
            return
        
        # Lista de arquivos para restaurar
        arquivos_dados = [
            ("usuarios.json", USUARIOS_FILE),
            ("tags.json", TAGS_FILE),
            ("times.json", TIMES_FILE),
            ("tarefas.json", TAREFAS_FILE)
        ]
        
        for nome_backup, arquivo_destino in arquivos_dados:
            caminho_backup = os.path.join(backup_path, nome_backup)
            caminho_destino = os.path.join(DATA_DIR, arquivo_destino)
            
            if os.path.exists(caminho_backup):
                shutil.copy2(caminho_backup, caminho_destino)
                print(f"✅ Dados restaurados: {arquivo_destino}")
            else:
                print(f"⚠️  Arquivo de backup não encontrado: {nome_backup}")
        
        # Remove o diretório de backup
        shutil.rmtree(backup_path)
        print(f"🗑️  Backup removido: {backup_path}")
        
    except Exception as e:
        print(f"❌ Erro ao restaurar dados: {e}")

def limpar_dados_teste():
    """
    Limpa todos os dados de teste, deixando apenas estruturas vazias.
    """
    try:
        # Lista de arquivos para limpar
        arquivos_dados = [USUARIOS_FILE, TAGS_FILE, TIMES_FILE, TAREFAS_FILE]
        
        for arquivo in arquivos_dados:
            caminho_arquivo = os.path.join(DATA_DIR, arquivo)
            
            # Cria estrutura vazia
            with open(caminho_arquivo, 'w') as f:
                json.dump({}, f)
            
            print(f"🧹 Dados limpos: {arquivo}")
        
    except Exception as e:
        print(f"❌ Erro ao limpar dados: {e}")

def executar_todos_testes():
    """
    Executa todos os testes unitários do sistema.
    
    Returns:
        bool: True se todos os testes passaram, False caso contrário
    """
    print("=" * 80)
    print("EXECUTANDO TODOS OS TESTES DO TASK MANAGER")
    print("=" * 80)
    
    # Faz backup dos dados originais
    print("\n📦 FAZENDO BACKUP DOS DADOS ORIGINAIS...")
    timestamp_backup = fazer_backup_dados()
    
    if not timestamp_backup:
        print("❌ Falha ao criar backup. Abortando testes.")
        return False
    
    try:
        # Lista de módulos de teste
        modulos_teste = [
            'test_gerenciamento_tarefas',
            'test_tarefa', 
            'test_usuario',
            'test_tag',
            'test_time'
        ]
        
        total_passed = 0
        total_failed = 0
        resultados = {}
        
        # Executa os testes de cada módulo
        for modulo in modulos_teste:
            print(f"\n{'='*60}")
            print(f"EXECUTANDO TESTES: {modulo.upper()}")
            print(f"{'='*60}")
            
            try:
                # Importa o módulo de teste
                test_module = importlib.import_module(modulo)
                
                # Executa os testes do módulo
                if hasattr(test_module, 'run_all_tests'):
                    sucesso = test_module.run_all_tests()
                    resultados[modulo] = sucesso
                    
                    if sucesso:
                        total_passed += 1
                        print(f"✅ {modulo}: TODOS OS TESTES PASSARAM")
                    else:
                        total_failed += 1
                        print(f"❌ {modulo}: ALGUNS TESTES FALHARAM")
                else:
                    print(f"⚠️  {modulo}: Módulo não possui função run_all_tests()")
                    total_failed += 1
                    resultados[modulo] = False
                    
            except ImportError as e:
                print(f"❌ {modulo}: Erro ao importar - {e}")
                total_failed += 1
                resultados[modulo] = False
            except Exception as e:
                print(f"❌ {modulo}: Erro durante execução - {e}")
                total_failed += 1
                resultados[modulo] = False
        
        # Resumo dos resultados
        print("\n" + "=" * 80)
        print("RESUMO DOS RESULTADOS")
        print("=" * 80)
        print(f"Módulos executados: {len(modulos_teste)}")
        print(f"Módulos com sucesso: {total_passed}")
        print(f"Módulos com falhas: {total_failed}")
        
        print("\nDETALHES POR MÓDULO:")
        for modulo, sucesso in resultados.items():
            status = "✅ PASSOU" if sucesso else "❌ FALHOU"
            print(f"  {modulo}: {status}")
        
        # Determina se todos os testes passaram
        sucesso_geral = total_failed == 0
        
        if sucesso_geral:
            print("\n🎉 TODOS OS MÓDULOS PASSARAM NOS TESTES!")
        else:
            print(f"\n⚠️  {total_failed} MÓDULO(S) FALHARAM NOS TESTES!")
        
        print("=" * 80)
        
        return sucesso_geral
        
    finally:
        # Sempre restaura os dados originais, independente do resultado dos testes
        print("\n🔄 RESTAURANDO DADOS ORIGINAIS...")
        restaurar_dados(timestamp_backup)
        print("✅ Dados restaurados com sucesso!")

def executar_testes_modulo(nome_modulo):
    """
    Executa testes de um módulo específico.
    
    Args:
        nome_modulo (str): Nome do módulo (ex: 'usuario', 'tag', etc.)
    """
    print(f"Executando testes do módulo: {nome_modulo}")
    print("-" * 50)
    
    # Faz backup dos dados originais
    print("\n📦 FAZENDO BACKUP DOS DADOS ORIGINAIS...")
    timestamp_backup = fazer_backup_dados()
    
    if not timestamp_backup:
        print("❌ Falha ao criar backup. Abortando testes.")
        return False
    
    try:
        # Importa o módulo de teste específico
        test_module = importlib.import_module(f'test_{nome_modulo}')
        
        # Executa os testes
        if hasattr(test_module, 'run_all_tests'):
            sucesso = test_module.run_all_tests()
            return sucesso
        else:
            print(f"Erro: Módulo {nome_modulo} não possui função run_all_tests()")
            return False
            
    except ImportError as e:
        print(f"Erro ao importar testes do módulo {nome_modulo}: {e}")
        return False
    except Exception as e:
        print(f"Erro durante execução dos testes do módulo {nome_modulo}: {e}")
        return False
    finally:
        # Sempre restaura os dados originais
        print("\n🔄 RESTAURANDO DADOS ORIGINAIS...")
        restaurar_dados(timestamp_backup)
        print("✅ Dados restaurados com sucesso!")

def main():
    """
    Função principal do script.
    """
    if len(sys.argv) > 1:
        # Executa testes de um módulo específico
        nome_modulo = sys.argv[1]
        sucesso = executar_testes_modulo(nome_modulo)
    else:
        # Executa todos os testes
        sucesso = executar_todos_testes()
    
    # Retorna código de saída apropriado
    sys.exit(0 if sucesso else 1)

if __name__ == '__main__':
    main()

