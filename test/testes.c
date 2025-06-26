#include "../unity/unity.h"
#include "testes_modulo_principal.h"

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

int main() {
    UNITY_BEGIN();

    roda_testes_modulo_principal();
    
    return UNITY_END();
}
