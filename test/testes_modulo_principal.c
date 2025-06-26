#include "../unity/unity.h"
#include "../src/Principal.h"
#include "testes_modulo_principal.h"

static void teste_inicializacao_do_sistema();

void roda_testes_modulo_principal() {
    RUN_TEST(teste_inicializacao_do_sistema);
}

static void teste_inicializacao_do_sistema() {
    Principal* p;
    p = principal_iniciar();
    TEST_ASSERT_NOT_NULL(p);
}