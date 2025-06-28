#!/usr/bin/env python3
"""
Script de teste simples para verificar funcionamento dos módulos
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def teste_modulo_usuario():
    """Testa o módulo Usuario"""
    print("Testando módulo Usuario...")
    
    try:
        from modules.usuario import usuario_criar, usuario_get_nome, usuario_get_email, usuario_destruir
        
        # Teste básico
        usuario = usuario_criar("João Silva", "joao@email.com")
        if usuario is None:
            print("❌ Falha ao criar usuário")
            return False
        
        nome = usuario_get_nome(usuario)
        email = usuario_get_email(usuario)
        
        if nome != "João Silva":
            print(f"❌ Nome incorreto: esperado 'João Silva', obtido '{nome}'")
            return False
        
        if email != "joao@email.com":
            print(f"❌ Email incorreto: esperado 'joao@email.com', obtido '{email}'")
            return False
        
        usuario_destruir(usuario)
        print("✅ Módulo Usuario funcionando corretamente")
        return True
        
    except Exception as e:
        print(f"❌ Erro no módulo Usuario: {e}")
        return False

def teste_modulo_tag():
    """Testa o módulo Tag"""
    print("Testando módulo Tag...")
    
    try:
        from modules.tag import tag_criar, tag_get_nome, tag_get_cor, tag_destruir
        
        # Teste básico
        tag = tag_criar("Urgente", "#FF0000")
        if tag is None:
            print("❌ Falha ao criar tag")
            return False
        
        nome = tag_get_nome(tag)
        cor = tag_get_cor(tag)
        
        if nome != "Urgente":
            print(f"❌ Nome incorreto: esperado 'Urgente', obtido '{nome}'")
            return False
        
        if cor != "#FF0000":
            print(f"❌ Cor incorreta: esperado '#FF0000', obtido '{cor}'")
            return False
        
        tag_destruir(tag)
        print("✅ Módulo Tag funcionando corretamente")
        return True
        
    except Exception as e:
        print(f"❌ Erro no módulo Tag: {e}")
        return False

def teste_modulo_time():
    """Testa o módulo Time"""
    print("Testando módulo Time...")
    
    try:
        from modules.team import time_criar, time_get_nome, time_qtd_membros, time_destruir
        
        # Teste básico
        time = time_criar("Equipe Dev")
        if time is None:
            print("❌ Falha ao criar time")
            return False
        
        nome = time_get_nome(time)
        qtd = time_qtd_membros(time)
        
        if nome != "Equipe Dev":
            print(f"❌ Nome incorreto: esperado 'Equipe Dev', obtido '{nome}'")
            return False
        
        if qtd != 0:
            print(f"❌ Quantidade incorreta: esperado 0, obtido {qtd}")
            return False
        
        time_destruir(time)
        print("✅ Módulo Time funcionando corretamente")
        return True
        
    except Exception as e:
        print(f"❌ Erro no módulo Time: {e}")
        return False

def teste_modulo_tarefa():
    """Testa o módulo Tarefa"""
    print("Testando módulo Tarefa...")
    
    try:
        from modules.tarefa import tarefa_criar, tarefa_get_titulo, tarefa_get_status, tarefa_destruir
        from modules.usuario import usuario_criar, usuario_destruir
        from config import StatusTarefa
        from datetime import datetime, timedelta
        
        # Cria usuário para o teste
        usuario = usuario_criar("Test User", "test@email.com")
        if usuario is None:
            print("❌ Falha ao criar usuário para teste")
            return False
        
        # Teste básico
        prazo = datetime.now() + timedelta(days=7)
        tarefa = tarefa_criar("Tarefa Teste", "Descrição teste", usuario, prazo)
        if tarefa is None:
            print("❌ Falha ao criar tarefa")
            return False
        
        titulo = tarefa_get_titulo(tarefa)
        status = tarefa_get_status(tarefa)
        
        if titulo != "Tarefa Teste":
            print(f"❌ Título incorreto: esperado 'Tarefa Teste', obtido '{titulo}'")
            return False
        
        if status != StatusTarefa.TAREFA_ABERTA:
            print(f"❌ Status incorreto: esperado TAREFA_ABERTA, obtido {status}")
            return False
        
        tarefa_destruir(tarefa)
        usuario_destruir(usuario)
        print("✅ Módulo Tarefa funcionando corretamente")
        return True
        
    except Exception as e:
        print(f"❌ Erro no módulo Tarefa: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("TESTE SIMPLES DOS MÓDULOS DO TASK MANAGER")
    print("=" * 60)
    
    testes = [
        teste_modulo_usuario,
        teste_modulo_tag,
        teste_modulo_time,
        teste_modulo_tarefa
    ]
    
    sucessos = 0
    total = len(testes)
    
    for teste in testes:
        if teste():
            sucessos += 1
        print()
    
    print("=" * 60)
    print(f"RESULTADO: {sucessos}/{total} módulos funcionando corretamente")
    
    if sucessos == total:
        print("🎉 TODOS OS MÓDULOS ESTÃO FUNCIONANDO!")
    else:
        print("⚠️  ALGUNS MÓDULOS PRECISAM DE CORREÇÃO")
    
    print("=" * 60)
    return sucessos == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

