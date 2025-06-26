#include "../unity/unity.h"


/**
 * Para saídas claras ao rodar testes
 */
#define VERMELHO "\033[31m"
#define RESETAR_COR "\033[0m"
#define VERDE "\033[0;32m"

/**
 * Funções que rodam antes e depois da suite de testes
 */
void setUp(void) {}
void tearDown(void) {}

/**
 * Rotinas dos testes individuais de cada módulo
 */
static void roda_testes_modulo_principal();

int main() {
    UNITY_BEGIN();

    RUN_TEST(roda_testes_modulo_principal);
    
    return UNITY_END();
}

static void roda_testes_modulo_principal() {
    int a = 1;
    
    TEST_ASSERT( a == 1 );
    printf(VERDE "Testes do módulo principal passaram!\n" RESETAR_COR);
}
