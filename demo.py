#!/usr/bin/env python3
"""
Demonstração do Task Manager

Este script demonstra as funcionalidades principais do sistema
sem depender de imports relativos complexos.
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from enum import Enum

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurações básicas
SUCESSO = 0
ERRO = -1
MAX_NOME_LENGTH = 100
MAX_EMAIL_LENGTH = 150

class StatusTarefa(Enum):
    TAREFA_ABERTA = "TAREFA_ABERTA"
    TAREFA_EM_PROGRESSO = "TAREFA_EM_PROGRESSO"
    TAREFA_CONCLUIDA = "TAREFA_CONCLUIDA"

# Classe Usuario simplificada
class Usuario:
    def __init__(self, nome: str, email: str):
        self.id = id(self)
        self.nome = nome
        self.email = email
        self.data_criacao = datetime.now()

# Classe Tag simplificada
class Tag:
    def __init__(self, nome: str, cor: str):
        self.id = id(self)
        self.nome = nome
        self.cor = cor
        self.data_criacao = datetime.now()

# Classe Time simplificada
class Time:
    def __init__(self, nome: str):
        self.id = id(self)
        self.nome = nome
        self.membros = []
        self.data_criacao = datetime.now()

# Classe Tarefa simplificada
class Tarefa:
    def __init__(self, titulo: str, descricao: str, usuario: Usuario, prazo: datetime):
        self.id = id(self)
        self.titulo = titulo
        self.descricao = descricao
        self.usuario = usuario
        self.prazo = prazo
        self.status = StatusTarefa.TAREFA_ABERTA
        self.tags = []
        self.data_criacao = datetime.now()

def demonstrar_sistema():
    """Demonstra as funcionalidades do sistema"""
    print("=" * 60)
    print("🚀 DEMONSTRAÇÃO DO TASK MANAGER")
    print("=" * 60)
    print()
    
    # 1. Criar usuários
    print("👥 1. CRIANDO USUÁRIOS")
    print("-" * 30)
    
    usuarios = [
        Usuario("João Silva", "joao@empresa.com"),
        Usuario("Maria Santos", "maria@empresa.com"),
        Usuario("Pedro Oliveira", "pedro@empresa.com")
    ]
    
    for usuario in usuarios:
        print(f"✅ Usuário criado: {usuario.nome} ({usuario.email})")
    
    print()
    
    # 2. Criar tags
    print("🏷️  2. CRIANDO TAGS")
    print("-" * 30)
    
    tags = [
        Tag("Urgente", "#FF0000"),
        Tag("Bug", "#FFA500"),
        Tag("Feature", "#00FF00"),
        Tag("Documentação", "#0000FF")
    ]
    
    for tag in tags:
        print(f"✅ Tag criada: {tag.nome} ({tag.cor})")
    
    print()
    
    # 3. Criar times
    print("👥 3. CRIANDO TIMES")
    print("-" * 30)
    
    times = [
        Time("Desenvolvimento Frontend"),
        Time("Desenvolvimento Backend"),
        Time("QA e Testes")
    ]
    
    # Adicionar membros aos times
    times[0].membros.append(usuarios[0])  # João no Frontend
    times[1].membros.append(usuarios[1])  # Maria no Backend
    times[2].membros.append(usuarios[2])  # Pedro no QA
    
    for time in times:
        print(f"✅ Time criado: {time.nome} ({len(time.membros)} membros)")
    
    print()
    
    # 4. Criar tarefas
    print("📋 4. CRIANDO TAREFAS")
    print("-" * 30)
    
    tarefas = [
        Tarefa(
            "Implementar tela de login",
            "Criar interface de login responsiva com validação",
            usuarios[0],
            datetime.now() + timedelta(days=3)
        ),
        Tarefa(
            "Criar API de usuários",
            "Desenvolver endpoints REST para gerenciamento de usuários",
            usuarios[1],
            datetime.now() + timedelta(days=5)
        ),
        Tarefa(
            "Testes de integração",
            "Implementar testes automatizados para os módulos principais",
            usuarios[2],
            datetime.now() + timedelta(days=7)
        )
    ]
    
    # Adicionar tags às tarefas
    tarefas[0].tags.extend([tags[2], tags[0]])  # Feature + Urgente
    tarefas[1].tags.append(tags[2])             # Feature
    tarefas[2].tags.append(tags[3])             # Documentação
    
    for tarefa in tarefas:
        print(f"✅ Tarefa criada: {tarefa.titulo}")
        print(f"   Responsável: {tarefa.usuario.nome}")
        print(f"   Prazo: {tarefa.prazo.strftime('%d/%m/%Y %H:%M')}")
        print(f"   Tags: {', '.join([tag.nome for tag in tarefa.tags])}")
        print()
    
    # 5. Simular alterações de status
    print("🔄 5. ALTERANDO STATUS DAS TAREFAS")
    print("-" * 30)
    
    tarefas[0].status = StatusTarefa.TAREFA_EM_PROGRESSO
    tarefas[1].status = StatusTarefa.TAREFA_CONCLUIDA
    
    for i, tarefa in enumerate(tarefas):
        status_texto = {
            StatusTarefa.TAREFA_ABERTA: "Aberta",
            StatusTarefa.TAREFA_EM_PROGRESSO: "Em Progresso",
            StatusTarefa.TAREFA_CONCLUIDA: "Concluída"
        }[tarefa.status]
        
        print(f"📌 {tarefa.titulo}: {status_texto}")
    
    print()
    
    # 6. Relatório final
    print("📊 6. RELATÓRIO FINAL")
    print("-" * 30)
    
    print(f"👥 Total de usuários: {len(usuarios)}")
    print(f"🏷️  Total de tags: {len(tags)}")
    print(f"👥 Total de times: {len(times)}")
    print(f"📋 Total de tarefas: {len(tarefas)}")
    
    print()
    print("Status das tarefas:")
    status_count = {}
    for tarefa in tarefas:
        status = tarefa.status.value
        status_count[status] = status_count.get(status, 0) + 1
    
    for status, count in status_count.items():
        status_nome = {
            "TAREFA_ABERTA": "Abertas",
            "TAREFA_EM_PROGRESSO": "Em Progresso",
            "TAREFA_CONCLUIDA": "Concluídas"
        }.get(status, status)
        print(f"  • {status_nome}: {count}")
    
    print()
    
    # 7. Salvar dados (simulação)
    print("💾 7. SALVANDO DADOS")
    print("-" * 30)
    
    # Criar estrutura de dados para salvar
    dados = {
        "usuarios": [
            {
                "id": u.id,
                "nome": u.nome,
                "email": u.email,
                "data_criacao": u.data_criacao.isoformat()
            } for u in usuarios
        ],
        "tags": [
            {
                "id": t.id,
                "nome": t.nome,
                "cor": t.cor,
                "data_criacao": t.data_criacao.isoformat()
            } for t in tags
        ],
        "times": [
            {
                "id": t.id,
                "nome": t.nome,
                "membros": [m.id for m in t.membros],
                "data_criacao": t.data_criacao.isoformat()
            } for t in times
        ],
        "tarefas": [
            {
                "id": t.id,
                "titulo": t.titulo,
                "descricao": t.descricao,
                "usuario_id": t.usuario.id,
                "prazo": t.prazo.isoformat(),
                "status": t.status.value,
                "tags": [tag.id for tag in t.tags],
                "data_criacao": t.data_criacao.isoformat()
            } for t in tarefas
        ]
    }
    
    # Salvar em arquivos JSON
    os.makedirs("data", exist_ok=True)
    
    for categoria, items in dados.items():
        arquivo = f"data/{categoria}.json"
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
        print(f"✅ Dados salvos em {arquivo}")
    
    print()
    print("🎉 DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
    print()
    print("📁 Arquivos criados:")
    print("  • data/usuarios.json")
    print("  • data/tags.json")
    print("  • data/times.json")
    print("  • data/tarefas.json")
    print()
    print("🌐 Para executar a interface web:")
    print("  cd web/task_manager_web")
    print("  source venv/bin/activate")
    print("  python src/main.py")
    print()
    print("🔗 Acesse: http://localhost:5000")
    print("=" * 60)

if __name__ == "__main__":
    demonstrar_sistema()

