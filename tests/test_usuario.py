"""
Testes unitários para o módulo Usuario

Este arquivo contém todos os testes especificados no documento para o módulo Usuario.
Os testes seguem exatamente as especificações fornecidas.

Testes implementados (conforme especificação):
1. Criação de usuário com nome e e-mail válidos
2. Criação com e-mail nulo
3. Criação com nome nulo
4. Modificação de e-mail válida
5. Modificação com e-mail nulo
6. Consulta de nome e e-mail após criação
7. Destruição de usuário
"""

import unittest
import sys
import os

# Adiciona o diretório pai ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.usuario import (
    usuario_criar, usuario_destruir, usuario_set_email,
    usuario_get_nome, usuario_get_email
)

def test_01_criacao_usuario_valido():
    """
    Teste 1: Criação de usuário com nome e e-mail válidos
    
    Conforme especificação:
    Entrada: strings não nulas ou vazias para nome e e-mail
    Esperado: ponteiro não nulo; funções de acesso (usuario_get_nome,
    usuario_get_email) retornam os valores corretos
    """
    # Dados de teste
    nome = "João Silva"
    email = "joao.silva@email.com"
    
    # Executa a operação
    usuario = usuario_criar(nome, email)
    
    # Verificações
    assert usuario is not None, "Usuario deve ser criado com sucesso"
    assert usuario_get_nome(usuario) == nome, "Nome deve ser retornado corretamente"
    assert usuario_get_email(usuario) == email.lower(), "Email deve ser retornado corretamente"
    
    # Limpeza
    usuario_destruir(usuario)

def test_02_criacao_email_nulo():
    """
    Teste 2: Criação com e-mail nulo
    
    Conforme especificação:
    Entrada: nome válido; e-mail nulo
    Esperado: retorno NULL
    """
    # Dados de teste
    nome = "João Silva"
    email = None
    
    # Executa a operação
    usuario = usuario_criar(nome, email)
    
    # Verificações
    assert usuario is None, "Usuario não deve ser criado com email nulo"

def test_03_criacao_nome_nulo():
    """
    Teste 3: Criação com nome nulo
    
    Conforme especificação:
    Entrada: nome nulo; e-mail válido
    Esperado: retorno NULL
    """
    # Dados de teste
    nome = None
    email = "joao.silva@email.com"
    
    # Executa a operação
    usuario = usuario_criar(nome, email)
    
    # Verificações
    assert usuario is None, "Usuario não deve ser criado com nome nulo"

def test_04_modificacao_email_valida():
    """
    Teste 4: Modificação de e-mail válida
    
    Conforme especificação:
    Entrada: ponteiro para usuário válido; string não nula para novo e-mail
    Esperado: retorno 0; usuario_get_email retorna o novo e-mail
    """
    # Preparação
    nome = "João Silva"
    email_inicial = "joao.silva@email.com"
    novo_email = "joao.novo@email.com"
    
    usuario = usuario_criar(nome, email_inicial)
    assert usuario is not None, "Usuario deve ser criado para o teste"
    
    # Executa a operação
    resultado = usuario_set_email(usuario, novo_email)
    
    # Verificações
    assert resultado == 0, "Modificação deve retornar sucesso (0)"
    assert usuario_get_email(usuario) == novo_email.lower(), "Email deve ser atualizado"
    
    # Limpeza
    usuario_destruir(usuario)

def test_05_modificacao_email_nulo():
    """
    Teste 5: Modificação com e-mail nulo
    
    Conforme especificação:
    Entrada: ponteiro para usuário válido; novo e-mail nulo
    Esperado: retorno -1
    """
    # Preparação
    nome = "João Silva"
    email_inicial = "joao.silva@email.com"
    novo_email = None
    
    usuario = usuario_criar(nome, email_inicial)
    assert usuario is not None, "Usuario deve ser criado para o teste"
    
    # Executa a operação
    resultado = usuario_set_email(usuario, novo_email)
    
    # Verificações
    assert resultado == -1, "Modificação deve retornar erro (-1)"
    assert usuario_get_email(usuario) == email_inicial.lower(), "Email não deve ser alterado"
    
    # Limpeza
    usuario_destruir(usuario)

def test_06_consulta_nome_email_apos_criacao():
    """
    Teste 6: Consulta de nome e e-mail após criação
    
    Conforme especificação:
    Entrada: ponteiro para usuário criado anteriormente
    Esperado: funções de acesso retornam os dados consistentes com os
    fornecidos na criação
    """
    # Dados de teste
    nome = "Maria Santos"
    email = "maria.santos@email.com"
    
    # Executa a operação
    usuario = usuario_criar(nome, email)
    assert usuario is not None, "Usuario deve ser criado"
    
    # Verificações
    nome_retornado = usuario_get_nome(usuario)
    email_retornado = usuario_get_email(usuario)
    
    assert nome_retornado == nome, "Nome deve ser consistente"
    assert email_retornado == email.lower(), "Email deve ser consistente"
    assert nome_retornado is not None, "Nome não deve ser nulo"
    assert email_retornado is not None, "Email não deve ser nulo"
    
    # Limpeza
    usuario_destruir(usuario)

def test_07_destruicao_usuario():
    """
    Teste 7: Destruição de usuário
    
    Conforme especificação:
    Entrada: ponteiro para usuário válido
    Esperado: memória liberada com sucesso; ponteiro não deve ser utilizado após
    a destruição
    """
    # Preparação
    nome = "Carlos Oliveira"
    email = "carlos.oliveira@email.com"
    
    usuario = usuario_criar(nome, email)
    assert usuario is not None, "Usuario deve ser criado"
    
    # Executa a operação
    usuario_destruir(usuario)
    
    # Verificação: Em Python, não podemos verificar diretamente a liberação de memória,
    # mas podemos verificar que a função não gera exceções
    # O teste passa se chegou até aqui sem exceções
    assert True, "Destruição executada sem exceções"

def test_08_casos_limite_nome_vazio():
    """
    Teste 8: Casos limite - nome vazio
    """
    # Teste com nome vazio
    usuario = usuario_criar("", "teste@email.com")
    assert usuario is None, "Usuario não deve ser criado com nome vazio"

def test_09_casos_limite_email_vazio():
    """
    Teste 9: Casos limite - email vazio
    """
    # Teste com email vazio
    usuario = usuario_criar("João Silva", "")
    assert usuario is None, "Usuario não deve ser criado com email vazio"

def test_10_casos_limite_email_invalido():
    """
    Teste 10: Casos limite - email inválido
    """
    # Teste com email inválido (sem @)
    usuario = usuario_criar("João Silva", "emailinvalido")
    assert usuario is None, "Usuario não deve ser criado com email inválido"

def test_11_modificacao_usuario_nulo():
    """
    Teste 11: Modificação de email com usuário nulo
    """
    # Executa a operação
    resultado = usuario_set_email(None, "novo@email.com")
    
    # Verificações
    assert resultado == -1, "Modificação deve retornar erro (-1) com usuário nulo"

def test_12_consulta_usuario_nulo():
    """
    Teste 12: Consulta de dados com usuário nulo
    """
    # Executa as operações
    nome = usuario_get_nome(None)
    email = usuario_get_email(None)
    
    # Verificações
    assert nome is None, "Nome deve ser None para usuário nulo"
    assert email is None, "Email deve ser None para usuário nulo"

# Lista de todos os testes para execução
def run_all_tests():
    """
    Executa todos os testes do módulo
    """
    tests = [
        test_01_criacao_usuario_valido,
        test_02_criacao_email_nulo,
        test_03_criacao_nome_nulo,
        test_04_modificacao_email_valida,
        test_05_modificacao_email_nulo,
        test_06_consulta_nome_email_apos_criacao,
        test_07_destruicao_usuario,
        test_08_casos_limite_nome_vazio,
        test_09_casos_limite_email_vazio,
        test_10_casos_limite_email_invalido,
        test_11_modificacao_usuario_nulo,
        test_12_consulta_usuario_nulo
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__}: PASSED")
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: FAILED - {str(e)}")
            failed += 1
    
    print(f"\n📊 RESULTADOS: {passed} passed, {failed} failed")
    return failed == 0

if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)

