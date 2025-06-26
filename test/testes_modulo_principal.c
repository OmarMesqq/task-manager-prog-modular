#include "../unity/unity.h"
#include "../src/Principal.h"
#include "testes_modulo_principal.h"

static void teste_inicializacao_do_sistema();
static void teste_encerramento_do_sistema();
static void teste_criacao_de_entidades();

void roda_testes_modulo_principal() {
    RUN_TEST(teste_inicializacao_do_sistema);
    RUN_TEST(teste_encerramento_do_sistema);
    RUN_TEST(teste_criacao_de_entidades);
}

static void teste_inicializacao_do_sistema() {
    Principal* p;
    p = principal_iniciar();

    // Estrutura deve ser acessível
    TEST_ASSERT_NOT_NULL(p);

    principal_encerrar(p);
}

static void teste_encerramento_do_sistema() {
    Principal* p;
    p = principal_iniciar();
    TEST_ASSERT_NOT_NULL(p);

    principal_encerrar(p);

    // Se chegou até aqui, o free foi executado com sucesso
    TEST_PASS();

    //TODO: testar persistência
}

static void teste_criacao_de_entidades() {
    Principal* p;
    p = principal_iniciar();
    TEST_ASSERT_NOT_NULL(p);

    Time* t = principal_criar_time(p, "Time de Prog Modular");
    TEST_ASSERT_NOT_NULL(t);

    Usuario* u = principal_criar_usuario(p, "Omar", "omar@email.com");
    TEST_ASSERT_NOT_NULL(u);

    Tag* tag = principal_criar_tag(p, "URGENTE", "ff0000");
    TEST_ASSERT_NOT_NULL(tag);
}