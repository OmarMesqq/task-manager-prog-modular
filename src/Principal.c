#include "Principal.h"
#include "Time.h"
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
 * @param void apenas inicializa estrutura
 * @return `NULL` em caso de erro ou `Principal*` em caso de sucesso
 */
Principal* principal_iniciar(void) {
    FILE* preferencias = fopen(ARQUIVO_PREFERENCIAS_TASK_MANAGER, "r");

    //TODO
    if (preferencias) {
        // Já existem dados persistidos    
    } else {
        // Instalação limpa: sem dados persistidos
    }
    Principal* contexto = malloc(sizeof(Principal));
    if (!contexto) {
        printf("Falha de alocação de memória ao criar Principal!\n");
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
 * @param p ponteiro para struct Principal
 * @return nenhum. Apenas libera memória
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

/**
 * Cria uma nova entidade `Time`
 * @param p ponteiro para struct Principal
 * @param nome do time a ser criado
 * @return `Time*` em caso de sucesso ou `NULL` em caso de erro
 */
Time* principal_criar_time(Principal* p, const char* nome) {
    if (!nome) {
        printf("Time deve ter um nome válido!");
        return NULL;
    }
    Time* novoTime = time_criar(nome);
    if (!novoTime) {
        printf("Falha de alocação de memória ao criar Time!\n");
        return NULL;
    }

    Time** nova_lista = realloc(p->listaTimes, (p->qtdTimes + 1) * sizeof(Time*));
    if (!nova_lista) {
        printf("Erro de realocação ao adicionar novo time.\n");
        free(novoTime);  // Libera o time alocado se realloc falhar
        return NULL;
    }

    nova_lista[p->qtdTimes] = novoTime;
    p->listaTimes = nova_lista;
    p->qtdTimes++;

    return novoTime;
}

/**
 * Cria uma nova entidade `Usuario`
 * @param p ponteiro para struct Principal
 * @param nome do usuário a ser criado
 * @param email do usuário a ser criado
 * @return `Usuario*` em caso de sucesso ou `NULL` em caso de erro
 */
Usuario* principal_criar_usuario(Principal *p, const char *nome, const char *email) {
    return NULL;
}

/**
 * Cria uma nova entidade `Usuario`
 * @param p ponteiro para struct Principal
 * @param nome da tag a ser criado
 * @param cor_hex da tag
 * @return `Tag*` em caso de sucesso ou `NULL` em caso de erro
 */
Tag* principal_criar_tag(Principal *p, const char *nome, const char* cor_hex) {
    return NULL;
}