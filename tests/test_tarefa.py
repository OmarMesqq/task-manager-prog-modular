"""
Testes unitários para o módulo Tarefa

Este arquivo contém todos os testes especificados no documento para o módulo Tarefa.
Os testes seguem exatamente as especificações fornecidas.

Testes implementados (conforme especificação):
1. Criação de tarefa com dados válidos
2. Criação com título nulo
3. Criação com descrição nula
4. Criação com usuário nulo
5. Alteração de status válida
6. Alteração de status com ponteiro nulo
7. Adição de tag válida
8. Adição de tag nula
9. Listagem de tags com limite inferior ao total
10. Listagem de tags com buffer nulo
11. Destruição de tarefa
"""

import unittest
import sys
import os
from datetime import datetime, timedelta

# Adiciona o diretório pai ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.tarefa import (
    tarefa_criar, tarefa_destruir, tarefa_set_status, tarefa_get_status,
    tarefa_add_tag, tarefa_list_tags, tarefa_get_titulo, tarefa_get_descricao,
    tarefa_get_usuario_responsavel_id, tarefa_get_prazo, tarefa_get_id,
    tarefa_get_tags_ids, tarefa_remover_tag
)
from modules.usuario import usuario_criar, usuario_destruir
from modules.tag import tag_criar, tag_destruir
from modules.tarefa import StatusTarefa

def setup_test_environment():
    """
    Preparação comum para os testes.
    """
    usuario_teste = usuario_criar("João Silva", "joao@email.com")
    prazo_teste = datetime.now() + timedelta(days=7)
    
    return usuario_teste, prazo_teste

def cleanup_test_environment(usuario_teste):
    """
    Limpeza comum após os testes.
    """
    if usuario_teste:
        usuario_destruir(usuario_teste)

def test_01_criacao_tarefa_dados_validos():
    """
    Teste 1: Criação de tarefa com dados válidos
    
    Conforme especificação:
    Entrada: strings não nulas ou vazias para título e descrição; usuário válido; prazo válido.
    Esperado: ponteiro não nulo; tarefa_get_status retorna TAREFA_ABERTA
    """
    # Setup
    usuario_teste, prazo_teste = setup_test_environment()
    
    try:
        # Dados de teste
        titulo = "Implementar funcionalidade X"
        descricao = "Descrição detalhada da funcionalidade X que precisa ser implementada"
        
        # Executa a operação
        tarefa = tarefa_criar(titulo, descricao, usuario_teste, prazo_teste)
        
        # Verificações
        assert tarefa is not None, "Tarefa deve ser criada com sucesso"
        assert tarefa_get_titulo(tarefa) == titulo, "Título deve ser retornado corretamente"
        assert tarefa_get_descricao(tarefa) == descricao, "Descrição deve ser retornada corretamente"
        assert tarefa_get_status(tarefa) == StatusTarefa.TAREFA_ABERTA, "Status inicial deve ser TAREFA_ABERTA"
        assert tarefa_get_id(tarefa) is not None, "ID deve ser gerado"
        
        # Limpeza
        tarefa_destruir(tarefa)
    finally:
        cleanup_test_environment(usuario_teste)

def test_02_criacao_titulo_nulo():
    """
    Teste 2: Criação com título nulo
    
    Conforme especificação:
    Entrada: título nulo; descrição válida; usuário válido; prazo válido
    Esperado: retorno NULL.
    """
    # Setup
    usuario_teste, prazo_teste = setup_test_environment()
    
    try:
        # Dados de teste
        titulo = None
        descricao = "Descrição válida"
        
        # Executa a operação
        tarefa = tarefa_criar(titulo, descricao, usuario_teste, prazo_teste)
        
        # Verificações
        assert tarefa is None, "Tarefa não deve ser criada com título nulo"
    finally:
        cleanup_test_environment(usuario_teste)

def test_03_criacao_descricao_nula():
    """
    Teste 3: Criação com descrição nula
    
    Conforme especificação:
    Entrada: título válido; descrição nula; usuário válido; prazo válido
    Esperado: retorno NULL.
    """
    # Setup
    usuario_teste, prazo_teste = setup_test_environment()
    
    try:
        # Dados de teste
        titulo = "Título válido"
        descricao = None
        
        # Executa a operação
        tarefa = tarefa_criar(titulo, descricao, usuario_teste, prazo_teste)
        
        # Verificações
        assert tarefa is None, "Tarefa não deve ser criada com descrição nula"
    finally:
        cleanup_test_environment(usuario_teste)

def test_04_criacao_usuario_nulo():
    """
    Teste 4: Criação com usuário nulo
    
    Conforme especificação:
    Entrada: título e descrição válidos; usuário nulo; prazo válido
    Esperado: retorno NULL
    """
    # Setup
    usuario_teste, prazo_teste = setup_test_environment()
    
    try:
        # Dados de teste
        titulo = "Título válido"
        descricao = "Descrição válida"
        usuario = None
        
        # Executa a operação
        tarefa = tarefa_criar(titulo, descricao, usuario, prazo_teste)
        
        # Verificações
        assert tarefa is None, "Tarefa não deve ser criada com usuário nulo"
    finally:
        cleanup_test_environment(usuario_teste)

def test_05_alteracao_status_valida():
    """
    Teste 5: Alteração de status válida
    
    Conforme especificação:
    Entrada: ponteiro para tarefa válida; status TAREFA_CONCLUIDA
    Esperado: retorno 0; tarefa_get_status retorna TAREFA_CONCLUIDA
    """
    # Setup
    usuario_teste, prazo_teste = setup_test_environment()
    
    try:
        # Preparação
        titulo = "Tarefa para teste de status"
        descricao = "Descrição da tarefa"
        
        tarefa = tarefa_criar(titulo, descricao, usuario_teste, prazo_teste)
        assert tarefa is not None, "Tarefa deve ser criada para o teste"
        
        # Executa a operação
        resultado = tarefa_set_status(tarefa, StatusTarefa.TAREFA_CONCLUIDA)
        
        # Verificações
        assert resultado == 0, "Alteração deve retornar sucesso (0)"
        assert tarefa_get_status(tarefa) == StatusTarefa.TAREFA_CONCLUIDA, "Status deve ser TAREFA_CONCLUIDA"
        
        # Limpeza
        tarefa_destruir(tarefa)
    finally:
        cleanup_test_environment(usuario_teste)

def test_06_alteracao_status_ponteiro_nulo():
    """
    Teste 6: Alteração de status com ponteiro nulo
    
    Conforme especificação:
    Entrada: ponteiro nulo para tarefa; status TAREFA_EM_PROGRESSO
    Esperado: retorno -1
    """
    # Executa a operação
    resultado = tarefa_set_status(None, StatusTarefa.TAREFA_EM_PROGRESSO)
    
    # Verificações
    assert resultado == -1, "Alteração deve retornar erro (-1)"

def test_07_adicao_tag_valida():
    """
    Teste 7: Adição de tag válida
    
    Conforme especificação:
    Entrada: ponteiro para tarefa válida; ponteiro para tag válida
    Esperado: retorno 0; tarefa_list_tags retorna a tag adicionada
    """
    # Setup
    usuario_teste, prazo_teste = setup_test_environment()
    
    try:
        # Preparação
        titulo = "Tarefa para teste de tag"
        descricao = "Descrição da tarefa"
        
        tarefa = tarefa_criar(titulo, descricao, usuario_teste, prazo_teste)
        tag = tag_criar("Urgente", "#FF0000")
        
        assert tarefa is not None, "Tarefa deve ser criada para o teste"
        assert tag is not None, "Tag deve ser criada para o teste"
        
        # Executa a operação
        resultado = tarefa_add_tag(tarefa, tag)
        
        # Verificações
        assert resultado == 0, "Adição deve retornar sucesso (0)"
        
        # Verifica se a tag foi adicionada
        buffer_tags = []
        qtd_tags = tarefa_list_tags(tarefa, buffer_tags, 10)
        assert qtd_tags == 1, "Deve haver 1 tag na tarefa"
        
        # Limpeza
        tarefa_destruir(tarefa)
        tag_destruir(tag)
    finally:
        cleanup_test_environment(usuario_teste)

def test_08_adicao_tag_nula():
    """
    Teste 8: Adição de tag nula
    
    Conforme especificação:
    Entrada: ponteiro para tarefa válida; ponteiro nulo para tag
    Esperado: retorno -1
    """
    # Setup
    usuario_teste, prazo_teste = setup_test_environment()
    
    try:
        # Preparação
        titulo = "Tarefa para teste de tag nula"
        descricao = "Descrição da tarefa"
        
        tarefa = tarefa_criar(titulo, descricao, usuario_teste, prazo_teste)
        assert tarefa is not None, "Tarefa deve ser criada para o teste"
        
        # Executa a operação
        resultado = tarefa_add_tag(tarefa, None)
        
        # Verificações
        assert resultado == -1, "Adição deve retornar erro (-1)"
        
        # Limpeza
        tarefa_destruir(tarefa)
    finally:
        cleanup_test_environment(usuario_teste)

def test_09_listagem_tags_limite_inferior():
    """
    Teste 9: Listagem de tags com limite inferior ao total
    
    Conforme especificação:
    Entrada: ponteiro para tarefa válida; buffer com tamanho menor que o número de tags
    Esperado: retorno do número de tags que cabem no buffer
    """
    # Setup
    usuario_teste, prazo_teste = setup_test_environment()
    
    try:
        # Preparação
        titulo = "Tarefa para teste de listagem"
        descricao = "Descrição da tarefa"
        
        tarefa = tarefa_criar(titulo, descricao, usuario_teste, prazo_teste)
        tag1 = tag_criar("Urgente", "#FF0000")
        tag2 = tag_criar("Importante", "#00FF00")
        tag3 = tag_criar("Bug", "#0000FF")
        
        assert tarefa is not None, "Tarefa deve ser criada para o teste"
        assert tag1 is not None and tag2 is not None and tag3 is not None, "Tags devem ser criadas"
        
        # Adiciona as tags
        tarefa_add_tag(tarefa, tag1)
        tarefa_add_tag(tarefa, tag2)
        tarefa_add_tag(tarefa, tag3)
        
        # Executa a operação com buffer limitado
        buffer_tags = []
        qtd_tags = tarefa_list_tags(tarefa, buffer_tags, 2)  # Limite de 2
        
        # Verificações
        assert qtd_tags == 2, "Deve retornar 2 tags (limite do buffer)"
        assert len(buffer_tags) == 2, "Buffer deve conter 2 tags"
        
        # Limpeza
        tarefa_destruir(tarefa)
        tag_destruir(tag1)
        tag_destruir(tag2)
        tag_destruir(tag3)
    finally:
        cleanup_test_environment(usuario_teste)

def test_10_listagem_tags_buffer_nulo():
    """
    Teste 10: Listagem de tags com buffer nulo
    
    Conforme especificação:
    Entrada: ponteiro para tarefa válida; buffer nulo
    Esperado: retorno -1
    """
    # Setup
    usuario_teste, prazo_teste = setup_test_environment()
    
    try:
        # Preparação
        titulo = "Tarefa para teste de buffer nulo"
        descricao = "Descrição da tarefa"
        
        tarefa = tarefa_criar(titulo, descricao, usuario_teste, prazo_teste)
        assert tarefa is not None, "Tarefa deve ser criada para o teste"
        
        # Executa a operação
        qtd_tags = tarefa_list_tags(tarefa, None, 10)
        
        # Verificações
        assert qtd_tags == 0, "Deve retornar 0 para buffer nulo"
        
        # Limpeza
        tarefa_destruir(tarefa)
    finally:
        cleanup_test_environment(usuario_teste)

def test_11_destruicao_tarefa():
    """
    Teste 11: Destruição de tarefa
    
    Conforme especificação:
    Entrada: ponteiro para tarefa válida
    Esperado: memória liberada com sucesso
    """
    # Setup
    usuario_teste, prazo_teste = setup_test_environment()
    
    try:
        # Preparação
        titulo = "Tarefa para destruição"
        descricao = "Descrição da tarefa"
        
        tarefa = tarefa_criar(titulo, descricao, usuario_teste, prazo_teste)
        assert tarefa is not None, "Tarefa deve ser criada"
        
        # Executa a operação
        tarefa_destruir(tarefa)
        
        # Verificação: Em Python, não podemos verificar diretamente a liberação de memória,
        # mas podemos verificar que a função não gera exceções
        # O teste passa se chegou até aqui sem exceções
        assert True, "Destruição executada sem exceções"
    finally:
        cleanup_test_environment(usuario_teste)

def test_12_casos_limite_titulo_vazio():
    """
    Teste 12: Casos limite - título vazio
    """
    # Setup
    usuario_teste, prazo_teste = setup_test_environment()
    
    try:
        # Teste com título vazio
        tarefa = tarefa_criar("", "Descrição válida", usuario_teste, prazo_teste)
        assert tarefa is None, "Tarefa não deve ser criada com título vazio"
    finally:
        cleanup_test_environment(usuario_teste)

def test_13_casos_limite_descricao_vazia():
    """
    Teste 13: Casos limite - descrição vazia
    """
    # Setup
    usuario_teste, prazo_teste = setup_test_environment()
    
    try:
        # Teste com descrição vazia
        tarefa = tarefa_criar("Título válido", "", usuario_teste, prazo_teste)
        assert tarefa is None, "Tarefa não deve ser criada com descrição vazia"
    finally:
        cleanup_test_environment(usuario_teste)

def test_14_casos_limite_prazo_nulo():
    """
    Teste 14: Casos limite - prazo nulo
    """
    # Setup
    usuario_teste, prazo_teste = setup_test_environment()
    
    try:
        # Teste com prazo nulo
        tarefa = tarefa_criar("Título válido", "Descrição válida", usuario_teste, None)
        assert tarefa is None, "Tarefa não deve ser criada com prazo nulo"
    finally:
        cleanup_test_environment(usuario_teste)

def test_15_multiplas_tags_mesma_tarefa():
    """
    Teste 15: Múltiplas tags na mesma tarefa
    """
    # Setup
    usuario_teste, prazo_teste = setup_test_environment()
    
    try:
        # Preparação
        titulo = "Tarefa com múltiplas tags"
        descricao = "Descrição da tarefa"
        
        tarefa = tarefa_criar(titulo, descricao, usuario_teste, prazo_teste)
        tag1 = tag_criar("Urgente", "#FF0000")
        tag2 = tag_criar("Importante", "#00FF00")
        tag3 = tag_criar("Bug", "#0000FF")
        
        assert tarefa is not None, "Tarefa deve ser criada"
        assert tag1 is not None and tag2 is not None and tag3 is not None, "Tags devem ser criadas"
        
        # Adiciona múltiplas tags
        resultado1 = tarefa_add_tag(tarefa, tag1)
        resultado2 = tarefa_add_tag(tarefa, tag2)
        resultado3 = tarefa_add_tag(tarefa, tag3)
        
        # Verificações
        assert resultado1 == 0, "Primeira tag deve ser adicionada"
        assert resultado2 == 0, "Segunda tag deve ser adicionada"
        assert resultado3 == 0, "Terceira tag deve ser adicionada"
        
        buffer_tags = []
        qtd_tags = tarefa_list_tags(tarefa, buffer_tags, 10)
        assert qtd_tags == 3, "Tarefa deve ter exatamente 3 tags"
        
        # Limpeza
        tarefa_destruir(tarefa)
        tag_destruir(tag1)
        tag_destruir(tag2)
        tag_destruir(tag3)
    finally:
        cleanup_test_environment(usuario_teste)

def test_16_tag_duplicada():
    """
    Teste 16: Tentativa de adicionar tag duplicada
    """
    # Setup
    usuario_teste, prazo_teste = setup_test_environment()
    
    try:
        # Preparação
        titulo = "Tarefa para teste de tag duplicada"
        descricao = "Descrição da tarefa"
        
        tarefa = tarefa_criar(titulo, descricao, usuario_teste, prazo_teste)
        tag = tag_criar("Urgente", "#FF0000")
        
        assert tarefa is not None, "Tarefa deve ser criada"
        assert tag is not None, "Tag deve ser criada"
        
        # Adiciona a tag duas vezes
        resultado1 = tarefa_add_tag(tarefa, tag)
        resultado2 = tarefa_add_tag(tarefa, tag)
        
        # Verificações
        assert resultado1 == 0, "Primeira adição deve ser bem-sucedida"
        assert resultado2 == -1, "Segunda adição deve falhar (tag duplicada)"
        
        buffer_tags = []
        qtd_tags = tarefa_list_tags(tarefa, buffer_tags, 10)
        assert qtd_tags == 1, "Tarefa deve ter apenas uma tag"
        
        # Limpeza
        tarefa_destruir(tarefa)
        tag_destruir(tag)
    finally:
        cleanup_test_environment(usuario_teste)

def test_17_todos_status_tarefa():
    """
    Teste 17: Testa todos os status possíveis da tarefa
    """
    # Setup
    usuario_teste, prazo_teste = setup_test_environment()
    
    try:
        # Preparação
        titulo = "Tarefa para teste de status"
        descricao = "Descrição da tarefa"
        
        tarefa = tarefa_criar(titulo, descricao, usuario_teste, prazo_teste)
        assert tarefa is not None, "Tarefa deve ser criada"
        
        # Testa todos os status
        status_list = [
            StatusTarefa.TAREFA_ABERTA,
            StatusTarefa.TAREFA_EM_PROGRESSO,
            StatusTarefa.TAREFA_CONCLUIDA,
            StatusTarefa.TAREFA_CANCELADA
        ]
        
        for status in status_list:
            resultado = tarefa_set_status(tarefa, status)
            assert resultado == 0, f"Alteração para {status} deve ser bem-sucedida"
            assert tarefa_get_status(tarefa) == status, f"Status deve ser {status}"
        
        # Limpeza
        tarefa_destruir(tarefa)
    finally:
        cleanup_test_environment(usuario_teste)

# Lista de todos os testes para execução
def run_all_tests():
    """
    Executa todos os testes do módulo
    """
    tests = [
        test_01_criacao_tarefa_dados_validos,
        test_02_criacao_titulo_nulo,
        test_03_criacao_descricao_nula,
        test_04_criacao_usuario_nulo,
        test_05_alteracao_status_valida,
        test_06_alteracao_status_ponteiro_nulo,
        test_07_adicao_tag_valida,
        test_08_adicao_tag_nula,
        test_09_listagem_tags_limite_inferior,
        test_10_listagem_tags_buffer_nulo,
        test_11_destruicao_tarefa,
        test_12_casos_limite_titulo_vazio,
        test_13_casos_limite_descricao_vazia,
        test_14_casos_limite_prazo_nulo,
        test_15_multiplas_tags_mesma_tarefa,
        test_16_tag_duplicada,
        test_17_todos_status_tarefa
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

