#!/usr/bin/env python3
"""
Script para iniciar o servidor e executar testes automaticamente
"""

import subprocess
import time
import sys
import signal
import os

def main():
    print("🚀 INICIANDO TASK MANAGER COM TESTES")
    print("=" * 60)
    
    # Inicia o servidor em background
    print("📡 Iniciando servidor Flask...")
    server_process = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Aguarda o servidor inicializar
    print("⏳ Aguardando servidor inicializar...")
    time.sleep(5)
    
    # Verifica se o servidor está rodando
    if server_process.poll() is not None:
        print("❌ Servidor falhou ao iniciar")
        stdout, stderr = server_process.communicate()
        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")
        return 1
    
    print("✅ Servidor iniciado com sucesso")
    
    # Executa os testes
    print("\n🧪 Executando testes da API...")
    try:
        test_result = subprocess.run(
            [sys.executable, "test_api.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print("📋 Resultado dos testes:")
        print(test_result.stdout)
        if test_result.stderr:
            print("⚠️  Erros dos testes:")
            print(test_result.stderr)
        
        test_success = test_result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("⏰ Testes expiraram")
        test_success = False
    except Exception as e:
        print(f"❌ Erro ao executar testes: {e}")
        test_success = False
    
    # Para o servidor
    print("\n🛑 Parando servidor...")
    server_process.terminate()
    
    try:
        server_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        print("⚠️  Servidor não parou graciosamente, forçando...")
        server_process.kill()
    
    print("\n" + "=" * 60)
    if test_success:
        print("🎉 TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Interrompido pelo usuário")
        sys.exit(1) 