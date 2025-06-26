#include "Principal.h"
#include <stdio.h>
#include <stdlib.h>

/**
 * TAD encapsulado ao módulo principal que gerencia as listas
 * de entidades do programa a interface com o gerenciador de tarefas
 */
typedef struct Principal {
    Time** listaTimes;
    size_t qtdTimes;
    
    Tag** listaTags;
    size_t qtdTags;
    
    Usuario** listaUsuarios;
    size_t qtdUsuarios;
} Principal;

/**
 * Inicializa o contexto global do app e configura o módulo Principal para que seja usado
 * @returns `NULL` em caso de erro ou `Principal*` em caso de sucesso
 */
Principal* principal_iniciar(void) {
    FILE* preferencias = fopen(ARQUIVO_PREFERENCIAS_TASK_MANAGER, "r");

    if (preferencias) {
        // Já existem dados persistidos    
    } else {
        // Instalação limpa: sem dados persistidos
    }
    Principal* contexto = malloc(sizeof(Principal));
    if (!contexto) {
        printf("Falha de alocação de memória ao alocar Principal!\n");
        return NULL;
    }

    return contexto;
}
