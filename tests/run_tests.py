#!/usr/bin/env python3
"""
Script para executar todos os testes do Task Manager

Este script executa todos os testes unitários dos módulos do sistema
e gera um relatório completo dos resultados.
"""

import sys
import os
import importlib

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def executar_todos_testes():
    """
    Executa todos os testes unitários do sistema.
    
    Returns:
        bool: True se todos os testes passaram, False caso contrário
    """
    print("=" * 80)
    print("EXECUTANDO TODOS OS TESTES DO TASK MANAGER")
    print("=" * 80)
    
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

def executar_testes_modulo(nome_modulo):
    """
    Executa testes de um módulo específico.
    
    Args:
        nome_modulo (str): Nome do módulo (ex: 'usuario', 'tag', etc.)
    """
    print(f"Executando testes do módulo: {nome_modulo}")
    print("-" * 50)
    
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

