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

    contexto->listaTags = NULL;
    contexto->qtdTags = 0;
    contexto->listaTimes = NULL;
    contexto->qtdTimes = 0;
    contexto->listaUsuarios = NULL;
    contexto->qtdUsuarios = 0;    

    return contexto;
}

/**
 * Libera memória utilizada pelo app e persiste prefências
 */
void principal_encerrar(Principal* p) {
    //TODO: persistência 

    // Libera tags
    for (size_t i = 0; i < p->qtdTags; i++) {
        free(p->listaTags[i]);
    }

    // Libera usuários
    for (size_t i = 0; i < p->qtdUsuarios; i++) {
        free(p->listaUsuarios[i]);
    }

    // Libera times
    for (size_t i = 0; i < p->qtdTimes; i++) {
        free(p->listaTimes[i]);
    }
}