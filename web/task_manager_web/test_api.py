#!/usr/bin/env python3
"""
Script para testar a API do Flask
"""

import requests
import time

def test_api():
    """Testa a API do Flask"""
    base_url = "http://localhost:5001"
    
    print("🔍 Testando API do Task Manager...")
    
    # Testa health check
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        print(f"✅ Health Check: {response.status_code}")
        print(f"📄 Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health Check falhou: {e}")
        return False
    
    # Testa listagem de times
    try:
        response = requests.get(f"{base_url}/api/teams", timeout=5)
        print(f"✅ Teams API: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📄 Teams encontrados: {data.get('count', 0)}")
        else:
            print(f"📄 Error: {response.json()}")
    except Exception as e:
        print(f"❌ Teams API falhou: {e}")
    
    # Testa listagem de usuários
    try:
        response = requests.get(f"{base_url}/api/users", timeout=5)
        print(f"✅ Users API: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📄 Users encontrados: {data.get('count', 0)}")
        else:
            print(f"📄 Error: {response.json()}")
    except Exception as e:
        print(f"❌ Users API falhou: {e}")
    
    # Testa listagem de tarefas
    try:
        response = requests.get(f"{base_url}/api/tasks", timeout=5)
        print(f"✅ Tasks API: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📄 Tasks encontradas: {data.get('count', 0)}")
        else:
            print(f"📄 Error: {response.json()}")
    except Exception as e:
        print(f"❌ Tasks API falhou: {e}")
    
    return True

if __name__ == "__main__":
    # Aguarda um pouco para o servidor inicializar
    print("⏳ Aguardando servidor inicializar...")
    time.sleep(3)
    
    test_api() 