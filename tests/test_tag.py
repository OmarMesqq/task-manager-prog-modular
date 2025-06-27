"""
Testes unitários para o módulo Tag

Este arquivo contém todos os testes especificados no documento para o módulo Tag.
Os testes seguem exatamente as especificações fornecidas.

Testes implementados (conforme especificação):
1. Criação de tag com nome e cor válidos
2. Criação com nome nulo
3. Criação com cor nula
4. Alteração de nome válida
5. Alteração de nome nula
6. Alteração de cor válida
7. Alteração de cor nula
8. Consulta de nome e cor após criação
9. Destruição da tag
"""

import unittest
import sys
import os

# Adiciona o diretório pai ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.tag import (
    tag_criar, tag_destruir, tag_set_nome, tag_set_cor,
    tag_get_nome, tag_get_cor
)

def test_01_criacao_tag_valida():
    """
    Teste 1: Criação de tag com nome e cor válidos
    
    Conforme especificação:
    Entrada: strings não nulas e não vazias para nome e cor hexadecimal
    Esperado: ponteiro não nulo; funções de acesso retornam os valores corretos
    """
    # Dados de teste
    nome = "Urgente"
    cor = "#FF0000"
    
    # Executa a operação
    tag = tag_criar(nome, cor)
    
    # Verificações
    assert tag is not None, "Tag deve ser criada com sucesso"
    assert tag_get_nome(tag) == nome, "Nome deve ser retornado corretamente"
    assert tag_get_cor(tag) == cor.upper(), "Cor deve ser retornada corretamente"
    
    # Limpeza
    tag_destruir(tag)

def test_02_criacao_nome_nulo():
    """
    Teste 2: Criação com nome nulo
    
    Conforme especificação:
    Entrada: nome nulo, cor válida
    Esperado: retorno NULL
    """
    # Dados de teste
    nome = None
    cor = "#FF0000"
    
    # Executa a operação
    tag = tag_criar(nome, cor)
    
    # Verificações
    assert tag is None, "Tag não deve ser criada com nome nulo"

def test_03_criacao_cor_nula():
    """
    Teste 3: Criação com cor nula
    
    Conforme especificação:
    Entrada: nome válido, cor nula
    Esperado: retorno NULL
    """
    # Dados de teste
    nome = "Urgente"
    cor = None
    
    # Executa a operação
    tag = tag_criar(nome, cor)
    
    # Verificações
    assert tag is None, "Tag não deve ser criada com cor nula"

def test_04_alteracao_nome_valida():
    """
    Teste 4: Alteração de nome válida
    
    Conforme especificação:
    Entrada: ponteiro para tag válida e novo nome não nulo
    Esperado: retorno 0; tag_get_nome retorna o novo nome
    """
    # Preparação
    nome_inicial = "Urgente"
    novo_nome = "Muito Urgente"
    cor = "#FF0000"
    
    tag = tag_criar(nome_inicial, cor)
    assert tag is not None, "Tag deve ser criada para o teste"
    
    # Executa a operação
    resultado = tag_set_nome(tag, novo_nome)
    
    # Verificações
    assert resultado == 0, "Alteração deve retornar sucesso (0)"
    assert tag_get_nome(tag) == novo_nome, "Nome deve ser atualizado"
    
    # Limpeza
    tag_destruir(tag)

def test_05_alteracao_nome_nula():
    """
    Teste 5: Alteração de nome nula
    
    Conforme especificação:
    Entrada: ponteiro para tag válida, novo nome nulo
    Esperado: retorno -1
    """
    # Preparação
    nome_inicial = "Urgente"
    novo_nome = None
    cor = "#FF0000"
    
    tag = tag_criar(nome_inicial, cor)
    assert tag is not None, "Tag deve ser criada para o teste"
    
    # Executa a operação
    resultado = tag_set_nome(tag, novo_nome)
    
    # Verificações
    assert resultado == -1, "Alteração deve retornar erro (-1)"
    assert tag_get_nome(tag) == nome_inicial, "Nome não deve ser alterado"
    
    # Limpeza
    tag_destruir(tag)

def test_06_alteracao_cor_valida():
    """
    Teste 6: Alteração de cor válida
    
    Conforme especificação:
    Entrada: ponteiro para tag válida e nova cor no formato "#RRGGBB"
    Esperado: retorno 0; tag_get_cor retorna a nova cor
    """
    # Preparação
    nome = "Urgente"
    cor_inicial = "#FF0000"
    nova_cor = "#00FF00"
    
    tag = tag_criar(nome, cor_inicial)
    assert tag is not None, "Tag deve ser criada para o teste"
    
    # Executa a operação
    resultado = tag_set_cor(tag, nova_cor)
    
    # Verificações
    assert resultado == 0, "Alteração deve retornar sucesso (0)"
    assert tag_get_cor(tag) == nova_cor.upper(), "Cor deve ser atualizada"
    
    # Limpeza
    tag_destruir(tag)

def test_07_alteracao_cor_nula():
    """
    Teste 7: Alteração de cor nula
    
    Conforme especificação:
    Entrada: ponteiro para tag válida, nova cor nula
    Esperado: retorno -1
    """
    # Preparação
    nome = "Urgente"
    cor_inicial = "#FF0000"
    nova_cor = None
    
    tag = tag_criar(nome, cor_inicial)
    assert tag is not None, "Tag deve ser criada para o teste"
    
    # Executa a operação
    resultado = tag_set_cor(tag, nova_cor)
    
    # Verificações
    assert resultado == -1, "Alteração deve retornar erro (-1)"
    assert tag_get_cor(tag) == cor_inicial.upper(), "Cor não deve ser alterada"
    
    # Limpeza
    tag_destruir(tag)

def test_08_consulta_nome_cor_apos_criacao():
    """
    Teste 8: Consulta de nome e cor após criação
    
    Conforme especificação:
    Entrada: ponteiro para tag criada anteriormente
    Esperado: funções de acesso retornam os dados consistentes com os
    fornecidos na criação
    """
    # Dados de teste
    nome = "Importante"
    cor = "#00FF00"
    
    # Executa a operação
    tag = tag_criar(nome, cor)
    assert tag is not None, "Tag deve ser criada"
    
    # Verificações
    nome_retornado = tag_get_nome(tag)
    cor_retornada = tag_get_cor(tag)
    
    assert nome_retornado == nome, "Nome deve ser consistente"
    assert cor_retornada == cor.upper(), "Cor deve ser consistente"
    assert nome_retornado is not None, "Nome não deve ser nulo"
    assert cor_retornada is not None, "Cor não deve ser nula"
    
    # Limpeza
    tag_destruir(tag)

def test_09_destruicao_tag():
    """
    Teste 9: Destruição da tag
    
    Conforme especificação:
    Entrada: ponteiro para tag válida
    Esperado: memória liberada com sucesso; ponteiro não deve ser utilizado após
    a destruição
    """
    # Preparação
    nome = "Bug"
    cor = "#0000FF"
    
    tag = tag_criar(nome, cor)
    assert tag is not None, "Tag deve ser criada"
    
    # Executa a operação
    tag_destruir(tag)
    
    # Verificação: Em Python, não podemos verificar diretamente a liberação de memória,
    # mas podemos verificar que a função não gera exceções
    # O teste passa se chegou até aqui sem exceções
    assert True, "Destruição executada sem exceções"

def test_10_casos_limite_nome_vazio():
    """
    Teste 10: Casos limite - nome vazio
    """
    # Teste com nome vazio
    tag = tag_criar("", "#FF0000")
    assert tag is None, "Tag não deve ser criada com nome vazio"

def test_11_casos_limite_cor_invalida():
    """
    Teste 11: Casos limite - cor inválida
    """
    # Teste com cor inválida (sem #)
    tag = tag_criar("Urgente", "FF0000")
    assert tag is None, "Tag não deve ser criada com cor inválida"

def test_12_casos_limite_cor_formato_errado():
    """
    Teste 12: Casos limite - formato de cor errado
    """
    # Teste com formato de cor errado
    tag = tag_criar("Urgente", "#GG0000")
    assert tag is None, "Tag não deve ser criada com formato de cor errado"

def test_13_alteracao_tag_nula():
    """
    Teste 13: Alteração de nome com tag nula
    """
    # Executa a operação
    resultado = tag_set_nome(None, "Novo Nome")
    
    # Verificações
    assert resultado == -1, "Alteração deve retornar erro (-1) com tag nula"

def test_14_consulta_tag_nula():
    """
    Teste 14: Consulta de dados com tag nula
    """
    # Executa as operações
    nome = tag_get_nome(None)
    cor = tag_get_cor(None)
    
    # Verificações
    assert nome is None, "Nome deve ser None para tag nula"
    assert cor is None, "Cor deve ser None para tag nula"

def test_15_cores_hexadecimais_validas():
    """
    Teste 15: Testa diferentes cores hexadecimais válidas
    """
    cores_validas = [
        "#FF0000",  # Vermelho
        "#00FF00",  # Verde
        "#0000FF",  # Azul
        "#FFFF00",  # Amarelo
        "#FF00FF",  # Magenta
        "#00FFFF",  # Ciano
        "#000000",  # Preto
        "#FFFFFF"   # Branco
    ]
    
    for cor in cores_validas:
        tag = tag_criar(f"Tag {cor}", cor)
        assert tag is not None, f"Tag deve ser criada com cor {cor}"
        assert tag_get_cor(tag) == cor.upper(), f"Cor deve ser {cor.upper()}"
        tag_destruir(tag)

# Lista de todos os testes para execução
def run_all_tests():
    """
    Executa todos os testes do módulo
    """
    tests = [
        test_01_criacao_tag_valida,
        test_02_criacao_nome_nulo,
        test_03_criacao_cor_nula,
        test_04_alteracao_nome_valida,
        test_05_alteracao_nome_nula,
        test_06_alteracao_cor_valida,
        test_07_alteracao_cor_nula,
        test_08_consulta_nome_cor_apos_criacao,
        test_09_destruicao_tag,
        test_10_casos_limite_nome_vazio,
        test_11_casos_limite_cor_invalida,
        test_12_casos_limite_cor_formato_errado,
        test_13_alteracao_tag_nula,
        test_14_consulta_tag_nula,
        test_15_cores_hexadecimais_validas
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

